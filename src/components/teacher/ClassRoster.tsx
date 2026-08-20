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

const TIER_COLOR: Record<PATier, string> = {
  NOT_STARTED: '#3D3D3D',
  CRITICAL:    '#E24B4A',
  NEEDS_WORK:  '#EF9F27',
  ON_TRACK:    '#378ADD',
  MASTERED:    '#00FF41',
};

const TIER_LABEL: Record<PATier, string> = {
  NOT_STARTED: 'Not Started',
  CRITICAL:    'Critical',
  NEEDS_WORK:  'Needs Work',
  ON_TRACK:    'On Track',
  MASTERED:    'Mastered',
};

function ReadinessGauge({ value, tier }: { value: number; tier: PATier }) {
  const color = TIER_COLOR[tier];
  const pct = Math.round(value);
  return (
    <div className="readiness-gauge" title={`${pct}% — ${TIER_LABEL[tier]}`}>
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
  const [data, setData] = useState<ClassData | null>(null);
  const [gaps, setGaps] = useState<GapItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [certFilter, setCertFilter] = useState('');
  const [activeTab, setActiveTab] = useState<'roster' | 'gaps'>('roster');

  useEffect(() => {
    // 1. Load class roster (primary data)
    fetch(`${apiUrl}/api/teacher/competency/class`, { credentials: 'include' })
      .then((r) => {
        if (!r.ok) throw new Error(`Class API ${r.status}`);
        return r.json() as Promise<ClassData>;
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
    fetch(`${apiUrl}/api/teacher/competency/gaps`, { credentials: 'include' })
      .then((r) => (r.ok ? (r.json() as Promise<GapItem[]>) : Promise.resolve([])))
      .then((gapData) => setGaps(gapData || []))
      .catch(() => setGaps([]));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  if (loading) {
    return <div className="class-roster__loading">Loading class data…</div>;
  }
  if (error) {
    return <p className="callout callout--warn">{error}</p>;
  }

  const students = data?.students ?? [];
  const allCerts = [...new Set(students.flatMap((s) => s.certs.map((c) => c.certId)))];
  const filtered = certFilter
    ? students.map((s) => ({ ...s, certs: s.certs.filter((c) => c.certId === certFilter) }))
    : students;

  const criticalCount = gaps.filter((g) => g.priority === 'CRITICAL').length;
  const needsWorkCount = gaps.filter((g) => g.priority === 'NEEDS_WORK').length;

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

          <table className="class-roster__table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Period</th>
                {filtered[0]?.certs.map((c) => (
                  <th key={c.certId}>{c.certName}</th>
                ))}
                <th>Active (7d)</th>
                <th>Last Active</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((student) => (
                <tr key={student.username}>
                  <td>
                    <a href={`/admin/student/${student.username}`} className="class-roster__student-link">
                      {student.displayName}
                    </a>
                  </td>
                  <td>{student.period}</td>
                  {student.certs.map((c) => (
                    <td key={c.certId}>
                      <ReadinessGauge value={c.readiness} tier={c.paTier} />
                    </td>
                  ))}
                  <td>{student.totalActiveMinutes}m</td>
                  <td>
                    {student.lastActive
                      ? new Date(student.lastActive).toLocaleDateString()
                      : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      {activeTab === 'gaps' && (
        <div className="class-roster__gaps">
          {gaps.length === 0 ? (
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
                {gaps.map((gap, i) => (
                  <tr key={i}>
                    <td>
                      <a href={`/admin/student/${gap.studentUsername}`} className="class-roster__student-link">
                        {gap.displayName}
                      </a>
                    </td>
                    <td>{gap.certId}</td>
                    <td>{gap.domainName}</td>
                    <td>
                      <ReadinessGauge
                        value={gap.readiness}
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
                    <td>{gap.deficitMinutes}m</td>
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
