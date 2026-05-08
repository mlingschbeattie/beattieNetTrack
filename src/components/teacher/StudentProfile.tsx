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
  studentUsername: string;
  certId: string;
  domainCode: string;
  apiUrl: string;
  onClose: () => void;
  onSaved: () => void;
};

function OverrideModal({
  studentUsername, certId, domainCode, apiUrl, onClose, onSaved,
}: OverrideModalProps) {
  const [score, setScore] = useState('');
  const [reason, setReason] = useState('');
  const [status, setStatus] = useState<'idle' | 'saving' | 'error'>('idle');

  const handleSave = async () => {
    const val = Number(score);
    if (!Number.isFinite(val) || val < 0 || val > 100) return;
    setStatus('saving');
    try {
      const res = await fetch(`${apiUrl}/api/teacher/competency/override`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentUsername, certId, domainCode, overrideScore: val, reason }),
      });
      if (!res.ok) throw new Error(`${res.status}`);
      onSaved();
    } catch {
      setStatus('error');
    }
  };

  return (
    <div className="override-modal-backdrop" onClick={onClose}>
      <div className="override-modal" onClick={(e) => e.stopPropagation()}>
        <h3>Override Mastery Score</h3>
        <p className="override-modal__meta">
          {certId} — {domainCode} — {studentUsername}
        </p>
        <label className="override-modal__label">
          New score (0–100)
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
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [override, setOverride] = useState<{
    certId: string; domainCode: string;
  } | null>(null);

  const loadProfile = () => {
    setLoading(true);
    fetch(`${apiUrl}/api/competency/profile/${username}`, { credentials: 'include' })
      .then((r) => {
        if (!r.ok) throw new Error(`API ${r.status}`);
        return r.json() as Promise<Profile>;
      })
      .then((data) => { setProfile(data); setLoading(false); })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load profile');
        setLoading(false);
      });
  };

  useEffect(() => { loadProfile(); }, [username]);

  if (loading) return <div className="student-profile__loading">Loading profile…</div>;
  if (error) return <p className="callout callout--warn">{error}</p>;
  if (!profile) return null;

  return (
    <div className="student-profile">
      {/* Header */}
      <div className="student-profile__header">
        <div>
          <h2 className="student-profile__name">{profile.student.displayName}</h2>
          <p className="student-profile__meta">
            {profile.student.currentYear} · {profile.currentYearMinutes}m this year
            · {profile.allTimeMinutes}m all-time
          </p>
        </div>
        {profile.entranceExam && (
          <div className="student-profile__exam-badge">
            <span>Placement: </span>
            <strong>{profile.entranceExam.placementTier}</strong>
            <span> ({Math.round(profile.entranceExam.totalScore)}%)</span>
          </div>
        )}
      </div>

      {/* Cert cards */}
      {profile.certs.map((cert) => (
        <div key={cert.certId} className="student-profile__cert">
          <div className="student-profile__cert-header">
            <h3 className="student-profile__cert-name">{cert.certName}</h3>
            <MasteryBar value={cert.readiness} tier={cert.paTier} />
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
              {cert.domains.map((d) => (
                <tr key={d.domainCode}>
                  <td>
                    <span className="student-profile__domain-code">{d.domainCode}</span>{' '}
                    {d.domainName}
                  </td>
                  <td>{d.weightPct}%</td>
                  <td>
                    <MasteryBar value={d.masteryScore} tier={d.paTier} />
                  </td>
                  <td>
                    {d.activeMinutes}m / {d.expectedMinutes}m
                  </td>
                  <td>{d.attemptCount}</td>
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
