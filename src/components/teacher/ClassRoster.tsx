import { useEffect, useState } from 'react';

type PATier = 'NOT_STARTED' | 'CRITICAL' | 'NEEDS_WORK' | 'ON_TRACK' | 'MASTERED';

type CertReadiness = {
  certId: string;
  certName: string;
  readiness: number;
  paTier: PATier;
};

type Student = {
  username: string;
  displayName: string;
  period: string;
  certs: CertReadiness[];
  totalActiveMinutes: number;
  lastActive: string | null;
};

type GapItem = {
  studentUsername: string;
  displayName: string;
  certId: string;
  domainCode: string;
  domainName: string;
  readiness: number;
  deficitMinutes: number;
  priority: 'CRITICAL' | 'NEEDS_WORK';
};

type ClassData = {
  students: Student[];
};

const TIER_COLOR: Record<string, string> = {
  NOT_STARTED: '#3D3D3D',
  CRITICAL:    '#E24B4A',
  NEEDS_WORK:  '#EF9F27',
  ON_TRACK:    '#378ADD',
  MASTERED:    '#00FF41',
};

const TIER_LABEL: Record<string, string> = {
  NOT_STARTED: 'Not Started',
  CRITICAL:    'Critical',
  NEEDS_WORK:  'Needs Work',
  ON_TRACK:    'On Track',
  MASTERED:    'Mastered',
};

function ReadinessGauge({ value, tier }: { value?: number; tier?: string }) {
  const normTier = (tier?.toUpperCase?.() || 'NOT_STARTED');
  const color = TIER_COLOR[normTier] || '#3D3D3D';
  const label = TIER_LABEL[normTier] || 'Not Started';
  const pct = Math.min(100, Math.max(0, Math.round(Number(value) || 0)));

  return (
    <div className="readiness-gauge" title={`${pct}% — ${label}`}>
      <div className="readiness-gauge__bar">
        <div
          className="readiness-gauge__fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
      <span className="readiness-gauge__label" style={{ color }}>
        {pct}%
      </span>
    </div>
  );
}

type Props = {
  apiUrl: string;
};

export default function ClassRoster({ apiUrl }: Props) {
  const baseApiUrl = apiUrl || 'https://api.beattietech.local';
  const [data, setData] = useState<unknown>(null);
  const [gaps, setGaps] = useState<unknown>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [certFilter, setCertFilter] = useState('');
  const [activeTab, setActiveTab] = useState<'roster' | 'gaps'>('roster');
  useEffect(() => {
    // 1. Load class roster (from /api/cis/students)
    fetch(`${baseApiUrl}/api/cis/students`, { credentials: 'include' })
      .then((r) => {
        if (!r.ok) throw new Error(`Class API ${r.status}`);
        return r.json();
      })
      .then((classData) => {
        setData(classData);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load class data');
        setLoading(false);
      });

    // 2. Load gaps non-blockingly (fallback gracefully if not yet implemented on API)
    fetch(`${baseApiUrl}/api/cis/students?bucket=CRITICAL`, { credentials: 'include' })
      .then((r) => (r.ok ? r.json() : []))
      .then((gapData) => setGaps(gapData || []))
      .catch(() => setGaps([]));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [baseApiUrl]);

  if (loading) {
    return <div className="class-roster__loading">Loading class data…</div>;
  }
  if (error) {
    return <p className="callout callout--warn">{error}</p>;
  }

  // Universal student adapter: normalizes /api/cis/students response
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawData: any = data;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawList = rawData?.students || rawData?.data?.students || rawData?.data || (Array.isArray(rawData) ? rawData : []);
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const students: Student[] = (Array.isArray(rawList) ? rawList : []).map((s: any) => {
    const rawCerts = s?.certTracks || s?.certs || s?.certifications || [];
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const certs = (Array.isArray(rawCerts) ? rawCerts : []).map((c: any) => ({
      certId: c?.certTrackId || c?.certId || c?.cert_id || 'unknown',
      certName: c?.title || c?.certTrackId || c?.certName || c?.name || 'Certification',
      readiness: Number(c?.averageCombinedScore ?? c?.readiness ?? c?.score ?? 0),
      paTier: String(c?.readinessBucket || c?.paTier || c?.pa_tier || 'NOT_STARTED').toUpperCase() as PATier,
    }));

    return {
      username: s?.username || s?.student_username || s?.studentId || s?.id || 'unknown',
      displayName: s?.displayName || s?.display_name || s?.name || s?.username || 'Student',
      period: s?.period != null ? `Period ${s.period}` : '—',
      certs,
      totalActiveMinutes: Number(s?.totalActiveMinutes ?? s?.total_active_minutes ?? s?.activeMinutes ?? 0),
      lastActive: s?.lastActive || s?.last_active || null,
    };
  });


  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawGaps: any = gaps;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawGapList = rawGaps?.data?.gaps || rawGaps?.data || rawGaps?.gaps || (Array.isArray(rawGaps) ? rawGaps : []);
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const safeGaps: GapItem[] = (Array.isArray(rawGapList) ? rawGapList : []).map((g: any) => ({
    studentUsername: g?.studentUsername || g?.student_username || g?.username || '',
    displayName: g?.displayName || g?.display_name || g?.name || g?.studentUsername || 'Student',
    certId: g?.certId || g?.cert_id || '',
    domainCode: g?.domainCode || g?.domain_code || '',
    domainName: g?.domainName || g?.domain_name || '',
    readiness: Number(g?.readiness ?? 0),
    deficitMinutes: Number(g?.deficitMinutes ?? g?.deficit_minutes ?? 0),
    priority: String(g?.priority || 'NEEDS_WORK').toUpperCase() as 'CRITICAL' | 'NEEDS_WORK',
  }));


  const allCerts = useMemo(() => {
    const certIds = new Set<string>();
    for (const s of students) {
      if (Array.isArray(s?.certs)) {
        for (const c of s.certs) {
          if (c?.certId) certIds.add(c.certId);
        }
      }
    }
    return Array.from(certIds);
  }, [students]);

  const filtered = useMemo(() => {
    if (!certFilter) return students;
    return students.map((s) => ({
      ...s,
      certs: Array.isArray(s?.certs) ? s.certs.filter((c) => c?.certId === certFilter) : [],
    }));
  }, [students, certFilter]);

  const criticalCount = safeGaps.filter((g) => g?.priority === 'CRITICAL').length;
  const needsWorkCount = safeGaps.filter((g) => g?.priority === 'NEEDS_WORK').length;

  return (
    <div className="class-roster">
      {/* Summary bar */}
      <div className="class-roster__summary">
        <div className="class-roster__stat">
          <span className="class-roster__stat-num">{students.length}</span>
          <span className="class-roster__stat-label">Students</span>
        </div>
        <div className="class-roster__stat">
          <span className="class-roster__stat-num" style={{ color: '#E24B4A' }}>
            {criticalCount}
          </span>
          <span className="class-roster__stat-label">Critical gaps</span>
        </div>
        <div className="class-roster__stat">
          <span className="class-roster__stat-num" style={{ color: '#EF9F27' }}>
            {needsWorkCount}
          </span>
          <span className="class-roster__stat-label">Needs work</span>
        </div>
        <div className="class-roster__actions">
          <a
            href={`${apiUrl}/api/teacher/competency/export`}
            className="btn btn--secondary btn--sm"
            target="_blank"
            rel="noreferrer"
          >
            Export CSV
          </a>
        </div>
      </div>

      {/* Tabs */}
      <div className="class-roster__tabs">
        <button
          className={`class-roster__tab${activeTab === 'roster' ? ' class-roster__tab--active' : ''}`}
          onClick={() => setActiveTab('roster')}
          type="button"
        >
          Class Roster
        </button>
        <button
          className={`class-roster__tab${activeTab === 'gaps' ? ' class-roster__tab--active' : ''}`}
          onClick={() => setActiveTab('gaps')}
          type="button"
        >
          Gap Alerts {criticalCount + needsWorkCount > 0 && (
            <span className="class-roster__badge">{criticalCount + needsWorkCount}</span>
          )}
        </button>
      </div>

      {activeTab === 'roster' && (
        <>
          {allCerts.length > 1 && (
            <div className="class-roster__filters">
              <label className="class-roster__filter-label">Filter by cert:</label>
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
            </div>
          )}

          {students.length === 0 ? (
            <p className="class-roster__no-gaps">No students found in class data.</p>
          ) : (
            <table className="class-roster__table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Period</th>
                  {allCerts.map((certId) => (
                    <th key={certId}>{certId}</th>
                  ))}
                  <th>Active (7d)</th>
                  <th>Last Active</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((student) => {
                  const studentCerts = Array.isArray(student?.certs) ? student.certs : [];
                  const certMap = new Map(studentCerts.map((c) => [c.certId, c]));

                  return (
                    <tr key={student.username || Math.random()}>
                      <td>
                        <a href={`/admin/student/${student.username}`} className="class-roster__student-link">
                          {student.displayName || student.username}
                        </a>
                      </td>
                      <td>{student.period || '—'}</td>
                      {allCerts.map((certId) => {
                        const c = certMap.get(certId);
                        return (
                          <td key={certId}>
                            {c ? (
                              <ReadinessGauge value={c.readiness ?? 0} tier={c.paTier ?? 'NOT_STARTED'} />
                            ) : (
                              <span style={{ color: 'var(--color-text-muted)', fontSize: 'var(--text-xs)' }}>—</span>
                            )}
                          </td>
                        );
                      })}
                      <td>{student.totalActiveMinutes ?? 0}m</td>
                      <td>
                        {student.lastActive
                          ? new Date(student.lastActive).toLocaleDateString()
                          : '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </>
      )}

      {activeTab === 'gaps' && (
        <div className="class-roster__gaps">
          {safeGaps.length === 0 ? (
            <p className="class-roster__no-gaps">No critical gaps detected. Great work!</p>
          ) : (
            <table className="class-roster__table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Cert</th>
                  <th>Domain</th>
                  <th>Readiness</th>
                  <th>Priority</th>
                  <th>Deficit (min)</th>
                </tr>
              </thead>
              <tbody>
                {safeGaps.map((gap, i) => (
                  <tr key={i}>
                    <td>
                      <a href={`/admin/student/${gap.studentUsername}`} className="class-roster__student-link">
                        {gap.displayName || gap.studentUsername}
                      </a>
                    </td>
                    <td>{gap.certId}</td>
                    <td>{gap.domainName}</td>
                    <td>
                      <ReadinessGauge
                        value={gap.readiness ?? 0}
                        tier={gap.priority === 'CRITICAL' ? 'CRITICAL' : 'NEEDS_WORK'}
                      />
                    </td>
                    <td>
                      <span
                        className="badge"
                        style={{
                          background: gap.priority === 'CRITICAL' ? 'rgba(226,75,74,0.15)' : 'rgba(239,159,39,0.15)',
                          color: gap.priority === 'CRITICAL' ? '#E24B4A' : '#EF9F27',
                          border: `1px solid ${gap.priority === 'CRITICAL' ? '#E24B4A' : '#EF9F27'}`,
                        }}
                      >
                        {gap.priority === 'CRITICAL' ? 'Critical' : 'Needs Work'}
                      </span>
                    </td>
                    <td>{gap.deficitMinutes ?? 0}m</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );

}
