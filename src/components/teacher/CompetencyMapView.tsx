import { useEffect, useMemo, useState } from 'react';

type MapEntry = {
  id: number;
  contentType: string;
  contentId: string;
  contentTitle: string;
  certId: string;
  domainCode: string;
  domainName: string;
  weightPct: number;
  expectedMinutes: number;
  active: boolean;
  addedBy: string;
};

type GroupedEntry = {
  certId: string;
  domains: {
    domainCode: string;
    domainName: string;
    entries: MapEntry[];
  }[];
};

type Props = {
  apiUrl?: string;
};

const CONTENT_TYPE_LABELS: Record<string, string> = {
  lab: 'Lab',
  quiz: 'Quiz',
  quest: 'Quest',
  journal: 'Journal',
  game: 'Game',
  entrance_exam: 'Exam',
};

export default function CompetencyMapView({ apiUrl }: Props) {
  const [entries, setEntries] = useState<MapEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [certFilter, setCertFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch(`/api/cis/domains`, { credentials: 'include' })
      .then((r) => {
        if (!r.ok) throw new Error(`API ${r.status}`);
        return r.json();
      })
      .then((raw) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const rawList = raw?.domains || (Array.isArray(raw) ? raw : []);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const mapped: MapEntry[] = rawList.map((d: any, idx: number) => ({
          id: d.id || idx,
          contentType: d.contentType || 'lab',
          contentId: d.contentId || d.id || '',
          contentTitle: d.contentTitle || d.name || d.id || '',
          certId: d.certTrackId || d.certId || '',
          domainCode: d.id || d.domainCode || '',
          domainName: d.name || d.domainName || '',
          weightPct: Number(d.weightPct ?? 20),
          expectedMinutes: Number(d.expectedMinutes ?? 120),
          active: Boolean(d.active ?? true),
          addedBy: d.addedBy || 'system',
        }));
        setEntries(mapped);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load map');
        setLoading(false);
      });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  const allCerts = useMemo(() => [...new Set(entries.map((e) => e.certId))].sort(), [entries]);
  const allTypes = useMemo(() => [...new Set(entries.map((e) => e.contentType))].sort(), [entries]);

  const filtered = useMemo(() => {
    let res = entries;
    if (certFilter) res = res.filter((e) => e.certId === certFilter);
    if (typeFilter) res = res.filter((e) => e.contentType === typeFilter);
    if (search) {
      const q = search.toLowerCase();
      res = res.filter(
        (e) =>
          e.contentTitle.toLowerCase().includes(q) ||
          e.contentId.toLowerCase().includes(q) ||
          e.domainName.toLowerCase().includes(q)
      );
    }
    return res;
  }, [entries, certFilter, typeFilter, search]);

  const grouped: GroupedEntry[] = useMemo(() => {
    const certMap = new Map<string, Map<string, { domainName: string; entries: MapEntry[] }>>();

    for (const entry of filtered) {
      if (!certMap.has(entry.certId)) certMap.set(entry.certId, new Map());
      const domainMap = certMap.get(entry.certId)!;
      if (!domainMap.has(entry.domainCode)) {
        domainMap.set(entry.domainCode, { domainName: entry.domainName, entries: [] });
      }
      domainMap.get(entry.domainCode)!.entries.push(entry);
    }

    return [...certMap.entries()].map(([certId, domainMap]) => ({
      certId,
      domains: [...domainMap.entries()].map(([domainCode, { domainName, entries: ents }]) => ({
        domainCode,
        domainName,
        entries: ents,
      })),
    }));
  }, [filtered]);

  // Totals
  const totalEntries = filtered.length;
  const totalMinutes = filtered.reduce((s, e) => s + e.expectedMinutes, 0);

  if (loading) return <div className="comp-map__loading">Loading competency map…</div>;
  if (error) return <p className="callout callout--warn">{error}</p>;

  return (
    <div className="comp-map">
      {/* Filters */}
      <div className="comp-map__toolbar">
        <input
          className="input"
          type="search"
          placeholder="Search by title or domain…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="select"
          value={certFilter}
          onChange={(e) => setCertFilter(e.target.value)}
        >
          <option value="">All certs</option>
          {allCerts.map((id) => (
            <option key={id} value={id}>{id}</option>
          ))}
        </select>
        <select
          className="select"
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
        >
          <option value="">All types</option>
          {allTypes.map((t) => (
            <option key={t} value={t}>{CONTENT_TYPE_LABELS[t] ?? t}</option>
          ))}
        </select>
        <span className="comp-map__count">
          {totalEntries} mapping{totalEntries !== 1 ? 's' : ''} · {totalMinutes}m expected
        </span>
      </div>

      {grouped.length === 0 && (
        <p className="comp-map__empty">No entries match your filters.</p>
      )}

      {grouped.map((cert) => (
        <div key={cert.certId} className="comp-map__cert">
          <h3 className="comp-map__cert-id">{cert.certId}</h3>

          {cert.domains.map((domain) => (
            <div key={domain.domainCode} className="comp-map__domain">
              <div className="comp-map__domain-header">
                <span className="comp-map__domain-code">{domain.domainCode}</span>
                <span className="comp-map__domain-name">{domain.domainName}</span>
                <span className="comp-map__domain-count">
                  {domain.entries.length} item{domain.entries.length !== 1 ? 's' : ''}
                </span>
              </div>

              <table className="comp-map__table">
                <thead>
                  <tr>
                    <th>Content</th>
                    <th>Type</th>
                    <th>Weight</th>
                    <th>Expected</th>
                    <th>Added by</th>
                  </tr>
                </thead>
                <tbody>
                  {domain.entries.map((entry) => (
                    <tr key={entry.id}>
                      <td>
                        <div className="comp-map__content-title">{entry.contentTitle}</div>
                        <div className="comp-map__content-id">{entry.contentId}</div>
                      </td>
                      <td>
                        <span className="pill pill--sm">
                          {CONTENT_TYPE_LABELS[entry.contentType] ?? entry.contentType}
                        </span>
                      </td>
                      <td>{entry.weightPct}%</td>
                      <td>{entry.expectedMinutes}m</td>
                      <td className="comp-map__added-by">{entry.addedBy}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
