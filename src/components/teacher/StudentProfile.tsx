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

type StudentCert = {
  id: string;
  certTrackId: string;
  title: string;
  examCode: string | null;
  passedAt: string;
  credentialId: string | null;
  verificationUrl: string | null;
  notes: string | null;
  recordedAt: string;
};

type CrossoverRule = {
  id: string;
  sourceCertId: string;
  targetDomainId: string;
  creditScore: string;
  waiveContent: boolean;
  reason: string;
};

const AVAILABLE_TRACKS = [
  { id: 'aplus1', title: 'CompTIA A+ Core 1', examCode: '220-1101' },
  { id: 'aplus2', title: 'CompTIA A+ Core 2', examCode: '220-1102' },
  { id: 'netplus', title: 'CompTIA Network+', examCode: 'N10-008' },
  { id: 'secplus', title: 'CompTIA Security+', examCode: 'SY0-701' },
  { id: 'nocti', title: 'NOCTI Computer Networking', examCode: 'NOCTI-CN' },
];

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

function getAcademicYear(): number {
  const now = new Date();
  return now.getMonth() >= 7 ? now.getFullYear() + 1 : now.getFullYear();
}

function OverrideModal({
  studentId, studentUsername, certId, domainCode, apiUrl, onClose, onSaved,
}: OverrideModalProps) {
  const [score, setScore] = useState('');
  const [reason, setReason] = useState('');
  const [status, setStatus] = useState<'idle' | 'saving' | 'error'>('idle');

  const handleSave = async () => {
    const num = Number.parseFloat(score);
    if (isNaN(num) || num < 0 || num > 100) return;
    if (!studentId) {
      setStatus('error');
      return;
    }
    setStatus('saving');
    try {
      const res = await fetch(`${apiUrl}/api/cis/scores/override`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          studentId,
          domainId: domainCode,
          academicYear: getAcademicYear(),
          overrideScore: num,
          reason: reason.trim() || 'Teacher manual override',
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

type RecordCertModalProps = {
  studentId?: string;
  studentUsername: string;
  apiUrl: string;
  crossoverRules: CrossoverRule[];
  existingCertTrackIds: string[];
  onClose: () => void;
  onSaved: () => void;
};

function RecordCertModal({
  studentId,
  studentUsername,
  apiUrl,
  crossoverRules,
  existingCertTrackIds,
  onClose,
  onSaved,
}: RecordCertModalProps) {
  const availableToGrant = AVAILABLE_TRACKS.filter(
    (t) => !existingCertTrackIds.includes(t.id)
  );
  const initialTrack = availableToGrant[0]?.id || AVAILABLE_TRACKS[0]?.id || 'aplus1';

  const [certTrackId, setCertTrackId] = useState(initialTrack);
  const [passedAt, setPassedAt] = useState(new Date().toISOString().slice(0, 10));
  const [credentialId, setCredentialId] = useState('');
  const [notes, setNotes] = useState('');
  const [status, setStatus] = useState<'idle' | 'saving' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const selectedTrackInfo = AVAILABLE_TRACKS.find((t) => t.id === certTrackId);
  const previewCrossovers = crossoverRules.filter((r) => r.sourceCertId === certTrackId);

  const handleRecord = async () => {
    setStatus('saving');
    setErrorMsg(null);
    try {
      const targetId = studentId || studentUsername;
      const res = await fetch(`${apiUrl}/api/cis/students/${targetId}/certifications`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          certTrackId,
          passedAt,
          credentialId: credentialId.trim() || undefined,
          notes: notes.trim() || undefined,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.message || `Server responded with ${res.status}`);
      }

      setStatus('idle');
      onSaved();
    } catch (err) {
      setStatus('error');
      setErrorMsg(err instanceof Error ? err.message : 'Failed to record certification');
    }
  };

  return (
    <div className="override-modal-backdrop" onClick={onClose}>
      <div className="override-modal record-cert-modal" onClick={(e) => e.stopPropagation()}>
        <h3>Record Passed Industry Certification</h3>
        <p className="override-modal__meta">
          Student: <strong>{studentUsername}</strong>
        </p>

        <label className="override-modal__label">
          Certification Track
          <select
            className="input"
            value={certTrackId}
            onChange={(e) => setCertTrackId(e.target.value)}
          >
            {AVAILABLE_TRACKS.map((t) => (
              <option key={t.id} value={t.id}>
                {t.title} ({t.examCode}) {existingCertTrackIds.includes(t.id) ? '— Already Earned' : ''}
              </option>
            ))}
          </select>
        </label>

        <div className="record-cert-modal__row">
          <label className="override-modal__label" style={{ flex: 1 }}>
            Date Passed
            <input
              className="input"
              type="date"
              value={passedAt}
              onChange={(e) => setPassedAt(e.target.value)}
            />
          </label>

          <label className="override-modal__label" style={{ flex: 1.2 }}>
            Credential / Verification ID (optional)
            <input
              className="input"
              type="text"
              placeholder="e.g. COMP001020304"
              value={credentialId}
              onChange={(e) => setCredentialId(e.target.value)}
            />
          </label>
        </div>

        <label className="override-modal__label">
          Notes / Official Link (optional)
          <textarea
            className="input"
            rows={2}
            placeholder="e.g. Verified via CompTIA CertMetrics portal."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </label>

        {/* Crossover preview */}
        <div className="crossover-preview-box">
          <div className="crossover-preview-box__title">
            Automatic Masteries & Waivers to be Applied:
          </div>
          <p className="crossover-preview-box__desc">
            • <strong>Direct Track:</strong> 100% mastery and STRONG readiness on all {selectedTrackInfo?.title} domains.
          </p>
          {previewCrossovers.length > 0 ? (
            <div>
              <p className="crossover-preview-box__desc">
                • <strong>{previewCrossovers.length} Crossover Domain Credits:</strong>
              </p>
              <ul className="crossover-preview-box__list">
                {previewCrossovers.map((cr) => (
                  <li key={cr.id}>
                    <code>{cr.targetDomainId}</code> — {cr.reason}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <p className="crossover-preview-box__desc pc-lab__muted">
              • No cross-track domain rules defined for this certification.
            </p>
          )}
        </div>

        {status === 'error' && errorMsg && (
          <p className="override-modal__error">{errorMsg}</p>
        )}

        <div className="override-modal__actions">
          <button className="btn btn--secondary" onClick={onClose} type="button">
            Cancel
          </button>
          <button
            className="btn btn--primary"
            onClick={handleRecord}
            disabled={status === 'saving'}
            type="button"
          >
            {status === 'saving' ? 'Granting Credits…' : 'Record & Grant Credits'}
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
  const [studentCerts, setStudentCerts] = useState<StudentCert[]>([]);
  const [crossoverRules, setCrossoverRules] = useState<CrossoverRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [override, setOverride] = useState<{
    certId: string; domainCode: string;
  } | null>(null);
  const [showRecordModal, setShowRecordModal] = useState(false);
  const [revokingCertId, setRevokingCertId] = useState<string | null>(null);

  const loadProfile = () => {
    setLoading(true);

    const pProfile = fetch(`${baseApiUrl}/api/cis/students/${username}`, { credentials: 'include' })
      .then((r) => {
        if (!r.ok) throw new Error(`API ${r.status}`);
        return r.json();
      });

    const pCerts = fetch(`${baseApiUrl}/api/cis/students/${username}/certifications`, { credentials: 'include' })
      .then((r) => (r.ok ? r.json() : { certs: [] }))
      .catch(() => ({ certs: [] }));

    const pRules = crossoverRules.length > 0
      ? Promise.resolve({ rules: crossoverRules })
      : fetch(`${baseApiUrl}/api/cis/crossover-rules`, { credentials: 'include' })
          .then((r) => (r.ok ? r.json() : { rules: [] }))
          .catch(() => ({ rules: [] }));

    Promise.all([pProfile, pCerts, pRules])
      .then(([raw, certsData, rulesData]) => {
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

        setStudentCerts(certsData.certs || []);
        if (rulesData.rules) {
          setCrossoverRules(rulesData.rules);
        }
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : 'Failed to load profile');
        setLoading(false);
      });
  };

  useEffect(() => { loadProfile(); }, [username, baseApiUrl]);

  const handleRevokeCert = async (certTrackId: string, certTitle: string) => {
    if (!window.confirm(`Are you sure you want to revoke "${certTitle}" for ${profile?.student?.displayName || username}? This will remove certification records and recompute domain readiness.`)) {
      return;
    }
    setRevokingCertId(certTrackId);
    try {
      const targetId = profile?.student?.id || username;
      const res = await fetch(`${baseApiUrl}/api/cis/students/${targetId}/certifications/${certTrackId}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (!res.ok) throw new Error(`Revocation returned ${res.status}`);
      loadProfile();
    } catch (err) {
      alert(`Failed to revoke certification: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setRevokingCertId(null);
    }
  };

  if (loading) return <div className="student-profile__loading">Loading profile…</div>;
  if (error) return <p className="callout callout--warn">{error}</p>;
  if (!profile) return null;

  const earnedTrackIds = studentCerts.map((c) => c.certTrackId);

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

      {/* Certifications & Prior Learning Card */}
      <div className="student-profile__certs-section">
        <div className="student-profile__certs-header">
          <div>
            <h3 className="student-profile__section-title">Industry Certifications & Prior Learning</h3>
            <p className="student-profile__section-desc">
              Passed certifications grant 100% domain readiness, waive associated coursework in the LMS, and credit verified crossover domains into Network+ and Security+.
            </p>
          </div>
          {isTeacher && (
            <button
              type="button"
              className="btn btn--primary btn--sm"
              onClick={() => setShowRecordModal(true)}
            >
              + Record Certification
            </button>
          )}
        </div>

        {studentCerts.length === 0 ? (
          <div className="student-profile__no-certs">
            <p>No industry certifications formally recorded yet.</p>
          </div>
        ) : (
          <div className="student-profile__cert-badges-grid">
            {studentCerts.map((cert) => {
              const crossovers = crossoverRules.filter((r) => r.sourceCertId === cert.certTrackId);
              return (
                <div key={cert.id} className="student-cert-badge-card">
                  <div className="student-cert-badge-card__top">
                    <div className="student-cert-badge-card__badge">
                      <span className="student-cert-badge-card__icon">✓</span>
                      <div>
                        <h4 className="student-cert-badge-card__title">{cert.title}</h4>
                        <span className="student-cert-badge-card__code">
                          {cert.examCode || cert.certTrackId}
                        </span>
                      </div>
                    </div>
                    {isTeacher && (
                      <button
                        type="button"
                        className="btn btn--ghost btn--xs student-cert-badge-card__revoke"
                        disabled={revokingCertId === cert.certTrackId}
                        onClick={() => handleRevokeCert(cert.certTrackId, cert.title)}
                        title="Revoke certification"
                      >
                        {revokingCertId === cert.certTrackId ? 'Revoking…' : 'Revoke'}
                      </button>
                    )}
                  </div>

                  <div className="student-cert-badge-card__details">
                    <div className="student-cert-badge-card__meta-item">
                      <span className="label">Passed:</span>
                      <span className="val">{cert.passedAt}</span>
                    </div>
                    {cert.credentialId && (
                      <div className="student-cert-badge-card__meta-item">
                        <span className="label">Credential ID:</span>
                        <span className="val font-mono">{cert.credentialId}</span>
                      </div>
                    )}
                    {cert.notes && (
                      <div className="student-cert-badge-card__meta-item">
                        <span className="label">Notes:</span>
                        <span className="val">{cert.notes}</span>
                      </div>
                    )}
                  </div>

                  {crossovers.length > 0 && (
                    <div className="student-cert-badge-card__crossovers">
                      <div className="student-cert-badge-card__crossover-label">
                        Applied Crossover Credits ({crossovers.length} domains):
                      </div>
                      <div className="student-cert-badge-card__crossover-chips">
                        {crossovers.map((cr) => (
                          <span
                            key={cr.id}
                            className="student-cert-badge-card__chip"
                            title={cr.reason}
                          >
                            <code>{cr.targetDomainId}</code> · 100% Waived
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Cert track domain cards */}
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
          studentId={profile?.student?.id}
          studentUsername={username}
          certId={override.certId}
          domainCode={override.domainCode}
          apiUrl={apiUrl}
          onClose={() => setOverride(null)}
          onSaved={() => { setOverride(null); loadProfile(); }}
        />
      )}

      {showRecordModal && (
        <RecordCertModal
          studentId={profile?.student?.id}
          studentUsername={username}
          apiUrl={apiUrl}
          crossoverRules={crossoverRules}
          existingCertTrackIds={earnedTrackIds}
          onClose={() => setShowRecordModal(false)}
          onSaved={() => {
            setShowRecordModal(false);
            loadProfile();
          }}
        />
      )}
    </div>
  );
}
