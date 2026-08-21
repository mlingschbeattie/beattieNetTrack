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
  student: { id?: string; username: string; displayName: string; currentYear: string };
  certs: CertData[];
  allTimeMinutes: number;
  currentYearMinutes: number;
  entranceExam: EntranceExam | null;
};

function MasteryBar({ value, tier }: { value: number; tier: PATier }) {
  const color = TIER_COLOR[tier];
  return (
    <div className="mastery-bar" title={`${Math.round(value)}% — ${TIER_LABEL[tier]}`}>
      <div className="mastery-bar__track">
        <div
          className="mastery-bar__fill"
          style={{ width: `${Math.round(value)}%`, background: color }}
        />
      </div>
      <span className="mastery-bar__pct" style={{ color }}>
        {Math.round(value)}%
      </span>
    </div>
  );
}

type OverrideModalProps = {
  studentId?: string;
  studentUsername: string;
  certId: string;
  domainCode: string;
  apiUrl: string;
  onClose: () => void;
  onSaved: () => void;
};

function OverrideModal({
  studentId, studentUsername, certId, domainCode, apiUrl, onClose, onSaved,
}: OverrideModalProps) {
  const [score, setScore] = useState('');
  const [reason, setReason] = useState('');
  const [status, setStatus] = useState<'idle' | 'saving' | 'error'>('idle');

  const handleSave = async () => {
    const num = Number.parseFloat(score);
    if (isNaN(num) || num < 0 || num > 100) return;
    setStatus('saving');
    try {
      const res = await fetch(`${apiUrl}/api/cis/scores/override`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          studentId: studentId || studentUsername,
          domainId: domainCode,
          score: num,
          reason: reason.trim() || undefined,
        }),
      });
      if (!res.ok) throw new Error(`Override failed: ${res.status}`);
      setStatus('idle');
      onSaved();
    } catch {
      setStatus('error');
    }
  };

  return (
    <div className="override-modal-backdrop" onClick={onClose}>
      <div className="override-modal" onClick={(e) => e.stopPropagation()}>
        <h3>Manual Score Override</h3>
        <p className="override-modal__meta">
          {studentUsername} · {certId} · {domainCode}
        </p>
        <label className="override-modal__label">
          Override Score (0–100)
          <input
            className="input"
            type="number"
            min={0}
            max={100}
            value={score}
            onChange={(e) => setScore(e.target.value)}
          />
        </label>
        <label className="override-modal__label">
          Reason (optional)
          <textarea
            className="input"
            rows={3}
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          />
        </label>
        {status === 'error' && (
          <p className="override-modal__error">Save failed. Check the score and try again.</p>
        )}
        <div className="override-modal__actions">
          <button className="btn btn--secondary" onClick={onClose} type="button">Cancel</button>
          <button
            className="btn btn--primary"
            onClick={handleSave}
            disabled={status === 'saving'}
            type="button"
          >
            {status === 'saving' ? 'Saving…' : 'Save Override'}
          </button>
        </div>
      </div>
    </div>
  );
}

type Props = {
  username: string;
  apiUrl: string;
  isTeacher?: boolean;
};

export default function StudentProfile({ username, apiUrl, isTeacher = false }: Props) {
  const baseApiUrl = 'https://api.beattietech.local';
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [override, setOverride] = useState<{
    certId: string; domainCode: string;
  } | null>(null);

  const loadProfile = () => {
    setLoading(true);
    fetch(`${baseApiUrl}/api/cis/students/${username}`, { credentials: 'include' })
      .then((r) => {
        if (!r.ok) throw new Error(`API ${r.status}`);
        return r.json();
      })
      .then((raw) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const rawCerts = raw?.certTracks || raw?.certs || [];
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const certs: CertData[] = rawCerts.map((ct: any) => {
          const doms = ct?.domains || [];
          const avgScore = doms.length
            ? Math.round(doms.reduce((a: number, b: any) => a + (Number(b.effectiveScore ?? b.combinedScore ?? 0)), 0) / doms.length)
            : 0;
          return {
            certId: ct?.certTrackId || ct?.certId || 'cert',
            certName: ct?.title || ct?.certName || ct?.certTrackId || 'Certification',
            readiness: avgScore,
            paTier: (doms[0]?.readinessBucket || 'NOT_STARTED').toUpperCase() as PATier,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
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
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load profile');
        setLoading(false);
      });
  };

  useEffect(() => { loadProfile(); }, [username, baseApiUrl]);

  if (loading) return <div className="student-profile__loading">Loading profile…</div>;
  if (error) return <p className="callout callout--warn">{error}</p>;
  if (!profile) return null;

  return (
    <div className="student-profile">
      {/* Header */}
      <div className="student-profile__header">
        <div>
          <h2 className="student-profile__name">{profile?.student?.displayName || username}</h2>
          <p className="student-profile__meta">
            {profile?.student?.currentYear || 'Academic Year'} · {profile?.currentYearMinutes ?? 0}m this year
            · {profile?.allTimeMinutes ?? 0}m all-time
          </p>
        </div>
        {profile?.entranceExam && (
          <div className="student-profile__exam-badge">
            <span>Placement: </span>
            <strong>{profile.entranceExam.placementTier || 'Assigned'}</strong>
            <span> ({Math.round(profile.entranceExam.totalScore ?? 0)}%)</span>
          </div>
        )}
      </div>

      {/* Cert cards */}
      {(profile?.certs || []).map((cert: CertData) => (
        <div key={cert.certId} className="student-profile__cert">
          <div className="student-profile__cert-header">
            <h3 className="student-profile__cert-name">{cert.certName || cert.certId}</h3>
            <MasteryBar value={cert.readiness ?? 0} tier={cert.paTier ?? 'NOT_STARTED'} />
          </div>

          <table className="student-profile__domains">
            <thead>
              <tr>
                <th>Domain</th>
                <th>Weight</th>
                <th>Mastery</th>
                <th>Time</th>
                <th>Attempts</th>
                {isTeacher && <th></th>}
              </tr>
            </thead>
            <tbody>
              {(cert?.domains || []).map((d: DomainData) => (
                <tr key={d.domainCode}>
                  <td>
                    <span className="student-profile__domain-code">{d.domainCode}</span>{' '}
                    {d.domainName || d.domainCode}
                  </td>
                  <td>{d.weightPct ?? 0}%</td>
                  <td>
                    <MasteryBar value={d.masteryScore ?? 0} tier={d.paTier ?? 'NOT_STARTED'} />
                  </td>
                  <td>
                    {d.activeMinutes ?? 0}m / {d.expectedMinutes ?? 0}m
                  </td>
                  <td>{d.attemptCount ?? 0}</td>
                  {isTeacher && (
                    <td>
                      <button
                        className="btn btn--ghost btn--sm"
                        type="button"
                        onClick={() =>
                          setOverride({ certId: cert.certId, domainCode: d.domainCode })
                        }
                      >
                        Override
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}


      {override && (
        <OverrideModal
          studentId={profile?.student?.id || username}
          studentUsername={username}
          certId={override.certId}
          domainCode={override.domainCode}
          apiUrl={apiUrl}
          onClose={() => setOverride(null)}
          onSaved={() => { setOverride(null); loadProfile(); }}
        />
      )}
    </div>
  );
}
