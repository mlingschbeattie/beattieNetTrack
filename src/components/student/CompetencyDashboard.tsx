import { useEffect, useState } from 'react';

type PATier = 'NOT_STARTED' | 'CRITICAL' | 'NEEDS_WORK' | 'ON_TRACK' | 'MASTERED';

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

type DomainData = {
  domainCode: string;
  domainName: string;
  weightPct: number;
  masteryScore: number;
  timeCoverageScore: number;
  activeMinutes: number;
  expectedMinutes: number;
  readiness: number;
  paTier: PATier;
  attemptCount: number;
};

type CertData = {
  certId: string;
  certName: string;
  readiness: number;
  paTier: PATier;
  domains: DomainData[];
};

type EntranceExam = {
  takenAt: string;
  totalScore: number;
  placementTier: string;
  recommendedTrack: string;
};

type Profile = {
  student: { username: string; displayName: string; currentYear: string };
  certs: CertData[];
  allTimeMinutes: number;
  currentYearMinutes: number;
  entranceExam: EntranceExam | null;
};

type GapItem = {
  certId: string;
  domainCode: string;
  domainName: string;
  readiness: number;
  priority: string;
  suggestedAction: string;
  resourceTitle?: string;
  resourceUrl?: string;
};

const TIER_BG: Record<PATier, string> = {
  NOT_STARTED: 'rgba(61,61,61,0.15)',
  CRITICAL:    'rgba(226,75,74,0.12)',
  NEEDS_WORK:  'rgba(239,159,39,0.12)',
  ON_TRACK:    'rgba(55,138,221,0.12)',
  MASTERED:    'rgba(0,255,65,0.1)',
};

function RadialGauge({ value, tier, size = 120 }: { value: number; tier: PATier; size?: number }) {
  const color = TIER_COLOR[tier];
  const r = (size / 2) - 10;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(100, Math.max(0, value));
  const dash = (pct / 100) * circ;

  return (
    <div className="radial-gauge" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="rgba(148,163,184,0.2)"
          strokeWidth={8}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={8}
          strokeDasharray={`${dash} ${circ - dash}`}
          strokeDashoffset={circ / 4}
          strokeLinecap="round"
          style={{ transition: 'stroke-dasharray 0.6s ease' }}
        />
      </svg>
      <div className="radial-gauge__center">
        <span className="radial-gauge__pct" style={{ color }}>{Math.round(pct)}%</span>
        <span className="radial-gauge__tier" style={{ color }}>{TIER_LABEL[tier]}</span>
      </div>
    </div>
  );
}

type Props = {
  username: string;
  apiUrl?: string;
};

export default function CompetencyDashboard({ username, apiUrl }: Props) {
  const [profile, setProfile] = useState<any>(null);
  const [recs, setRecs] = useState<GapItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch(`/api/cis/students/${username}`, { credentials: 'include' }).then((r) => {
        if (!r.ok) throw new Error(`Profile API ${r.status}`);
        return r.json();
      }),
      fetch(`/api/cis/me/recommendations`, { credentials: 'include' }).then(
        (r) => (r.ok ? r.json() : Promise.resolve([]))
      ),
    ])
      .then(([raw, recData]) => {
        // Map raw profile just like StudentProfile
        const rawCerts = raw?.certTracks || raw?.certs || [];
        const certs = rawCerts.map((ct: any) => {
          const doms = ct?.domains || [];
          const avgScore = doms.length
            ? Math.round(doms.reduce((a: number, b: any) => a + (Number(b.effectiveScore ?? b.combinedScore ?? 0)), 0) / doms.length)
            : 0;
          return {
            certId: ct?.certTrackId || ct?.certId || 'cert',
            certName: ct?.title || ct?.certName || ct?.certTrackId || 'Certification',
            readiness: avgScore,
            paTier: (doms[0]?.readinessBucket || 'NOT_STARTED').toUpperCase() as PATier,
            domains: doms.map((d: any) => ({
              domainCode: d.domainId,
              domainName: d.domainName || d.domainId,
              weightPct: d.weightPct ?? 20,
              masteryScore: Number(d.masteryScore ?? 0),
              timeCoverageScore: Number(d.timeCoverage ?? 0),
              activeMinutes: Number(d.timeMinutes ?? d.activeMinutes ?? 0),
              expectedMinutes: Number(d.expectedMinutes ?? 120),
              readiness: Number(d.effectiveScore ?? d.combinedScore ?? 0),
              paTier: String(d.readinessBucket || 'NOT_STARTED').toUpperCase() as PATier,
              attemptCount: Number(d.attemptCount ?? 0),
            })),
          };
        });

        setProfile({
          student: raw?.student || { username, displayName: username, currentYear: raw?.academicYear || '2025-2026' },
          certs,
          allTimeMinutes: raw?.allTimeMinutes ?? 0,
          currentYearMinutes: raw?.currentYearMinutes ?? 0,
          entranceExam: raw?.entranceExam || null,
        });

        // Map recData properly if needed, fallback to array if wrapped
        const rawRecs = recData?.data || recData?.recommendations || recData;
        setRecs(Array.isArray(rawRecs) ? rawRecs : []);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load profile');
        setLoading(false);
      });
  // eslint-disable-next-line react-hooks/exhaustive-deps

  }, [username]);

  if (loading) return <div className="competency-dash__loading">Loading your profile…</div>;
  if (error) return <p className="callout callout--warn">{error}</p>;
  if (!profile) return null;

  const student = profile?.student;
  const certs = Array.isArray(profile?.certs) ? profile.certs : [];
  const allTimeMinutes = profile?.allTimeMinutes ?? 0;
  const currentYearMinutes = profile?.currentYearMinutes ?? 0;
  const entranceExam = profile?.entranceExam;
  const safeRecs = Array.isArray(recs) ? recs : [];

  return (
    <div className="competency-dash">
      {/* Hero stats */}
      <div className="competency-dash__stats">
        <div className="competency-dash__stat-card">
          <span className="competency-dash__stat-num">{currentYearMinutes}</span>
          <span className="competency-dash__stat-label">Minutes this year</span>
        </div>
        <div className="competency-dash__stat-card">
          <span className="competency-dash__stat-num">{allTimeMinutes}</span>
          <span className="competency-dash__stat-label">Total minutes</span>
        </div>
        {entranceExam && (
          <div className="competency-dash__stat-card">
            <span className="competency-dash__stat-num">{Math.round(entranceExam.totalScore ?? 0)}%</span>
            <span className="competency-dash__stat-label">Placement score</span>
          </div>
        )}
        {!entranceExam && (
          <div className="competency-dash__exam-cta">
            <p>You haven&apos;t taken the placement exam yet.</p>
            <a href="/entrance-exam" className="btn btn--primary btn--sm">
              Take Placement Exam
            </a>
          </div>
        )}
      </div>

      {/* Cert readiness gauges */}
      <div className="competency-dash__certs">
        {certs.map((cert) => (
          <div
            key={cert.certId}
            className="competency-dash__cert-card"
            style={{ background: TIER_BG[cert.paTier ?? 'NOT_STARTED'], borderColor: TIER_COLOR[cert.paTier ?? 'NOT_STARTED'] }}
          >
            <div className="competency-dash__cert-top">
              <div>
                <h3 className="competency-dash__cert-name">{cert.certName || cert.certId}</h3>
                <p className="competency-dash__cert-id">{cert.certId}</p>
              </div>
              <RadialGauge value={cert.readiness ?? 0} tier={cert.paTier ?? 'NOT_STARTED'} size={96} />
            </div>

            <div className="competency-dash__domains">
              {(cert?.domains || []).map((d) => (
                <div
                  key={d.domainCode}
                  className="competency-dash__domain-row"
                  title={`${d.domainName}: ${Math.round(d.masteryScore ?? 0)}% mastery, ${d.activeMinutes ?? 0}/${d.expectedMinutes ?? 0}m time`}
                >
                  <span className="competency-dash__domain-code">{d.domainCode}</span>
                  <div className="competency-dash__domain-bar-track">
                    <div
                      className="competency-dash__domain-bar-fill"
                      style={{
                        width: `${d.readiness ?? 0}%`,
                        background: TIER_COLOR[d.paTier ?? 'NOT_STARTED'],
                      }}
                    />
                  </div>
                  <span
                    className="competency-dash__domain-pct"
                    style={{ color: TIER_COLOR[d.paTier ?? 'NOT_STARTED'] }}
                  >
                    {Math.round(d.readiness ?? 0)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Recommendations */}
      {safeRecs.length > 0 && (
        <section className="competency-dash__recs">
          <h2 className="competency-dash__recs-title">Recommended Next Steps</h2>
          <div className="competency-dash__recs-list">
            {safeRecs.map((rec, i) => (
              <div key={i} className="competency-dash__rec-card">

                <div className="competency-dash__rec-header">
                  <span
                    className="competency-dash__rec-priority"
                    style={{
                      color: rec.priority === 'CRITICAL' ? '#E24B4A' : '#EF9F27',
                    }}
                  >
                    {rec.priority === 'CRITICAL' ? '⚠ Critical' : '↑ Improve'}
                  </span>
                  <span className="competency-dash__rec-domain">{rec.domainName}</span>
                </div>
                <p className="competency-dash__rec-action">{rec.suggestedAction}</p>
                {rec.resourceTitle && rec.resourceUrl && (
                  <a
                    href={rec.resourceUrl}
                    className="competency-dash__rec-link"
                    target="_blank"
                    rel="noreferrer"
                  >
                    {rec.resourceTitle} →
                  </a>
                )}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
