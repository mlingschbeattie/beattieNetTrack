import { useState, useEffect, useMemo, useCallback } from 'react';

export type CiaPillar = 'confidentiality' | 'integrity' | 'availability';

export type IncidentData = {
  id: string;
  title: string;
  scenario: string;
  correctPillar: CiaPillar;
  correctThreatIndex: number;
  threatOptions: string[];
  correctDefenseIndex: number;
  defenseOptions: string[];
  socraticExplanation: string;
  hint: string;
};

export const INCIDENTS: IncidentData[] = [
  {
    id: 'incident-1',
    title: 'Public Cloud Storage Bucket Exposure',
    scenario:
      'A routine security audit discovers an Amazon S3 bucket owned by the school district containing 14,000 student enrollment, medical, and IEP records with world-readable permissions (AllUsers: READ) enabled.',
    correctPillar: 'confidentiality',
    threatOptions: [
      'Misconfigured cloud storage bucket ACL allowing anonymous read access',
      'Volumetric Distributed Denial of Service (DDoS) overwhelming cloud hosting bandwidth',
      'SQL Injection in the online course registration portal database',
    ],
    correctThreatIndex: 0,
    defenseOptions: [
      'Enable S3 "Block Public Access", restrict bucket policy to authenticated IAM roles, and audit access logs',
      'Reboot the web servers and restore application files from offline backup tape',
      'Deploy endpoint antivirus software to all student Chromebooks',
    ],
    correctDefenseIndex: 0,
    socraticExplanation:
      'Confidentiality was breached first because sensitive, private student PII was exposed to unauthorized viewers. The records were not altered or falsified (integrity was preserved), and the bucket remained accessible (availability was preserved)—the core failure was unauthorized disclosure.',
    hint: 'Determine whether the data was altered, whether the server crashed, or whether private records were exposed to unauthorized eyes.',
  },
  {
    id: 'incident-2',
    title: 'Unauthorized Payroll Script Modification',
    scenario:
      'During end-of-month reconciliation, the payroll director discovers employee direct deposit bank routing numbers in the accounting database were silently changed at 2:14 AM by an automated PowerShell script utilizing a dormant service account.',
    correctPillar: 'integrity',
    threatOptions: [
      'DNS cache poisoning redirecting bank domain name lookups',
      'Compromised service account credentials executing unauthorized database UPDATE queries',
      'TCP SYN flood exhausting SQL database connection pool',
    ],
    correctThreatIndex: 1,
    defenseOptions: [
      'Disable the compromised service account, freeze payroll batching, and verify records against immutable backup logs',
      'Put a Cloudflare CDN proxy in front of the accounting server',
      'Change the guest Wi-Fi pre-shared key across campus',
    ],
    correctDefenseIndex: 0,
    socraticExplanation:
      'Integrity was violated first because the accuracy and trustworthiness of financial data was tampered with. The database stayed online (availability was intact), and the records were not leaked publicly (confidentiality was not the initial breach)—the attack corrupted data validity.',
    hint: 'The data in the database was modified without permission, meaning the records can no longer be trusted as accurate.',
  },
  {
    id: 'incident-3',
    title: 'Registration Portal Denial-of-Service Outage',
    scenario:
      'At 8:00 AM on the first day of senior course registration, the student enrollment portal becomes completely unreachable. Network monitoring indicates an external botnet is blasting the web application gateway with 300,000 HTTP requests per second.',
    correctPillar: 'availability',
    threatOptions: [
      'Stored Cross-Site Scripting (XSS) injected into course syllabus descriptions',
      'Credential stuffing attack against individual student email accounts',
      'Volumetric Layer 7 HTTP flood / Distributed Denial of Service (DDoS) exhausting web server bandwidth and CPU',
    ],
    correctThreatIndex: 2,
    defenseOptions: [
      'Format the web server hard drives and reinstall the operating system',
      'Engage upstream anti-DDoS scrubbing, activate WAF rate limiting, and challenge automated bot traffic',
      'Broadcast a mass email to all students asking them to try registering tomorrow',
    ],
    correctDefenseIndex: 1,
    socraticExplanation:
      'Availability is the primary failure because authorized users are denied access to a critical service when needed. No records were exposed to unauthorized readers (confidentiality) and database tables were not corrupted (integrity)—legitimate access was blocked.',
    hint: 'Legitimate users cannot access the system when they need to because the server is overwhelmed.',
  },
];

const PILLAR_DEFINITIONS: Array<{ id: CiaPillar; label: string; icon: string; description: string }> = [
  {
    id: 'confidentiality',
    label: 'Confidentiality',
    icon: '🔒',
    description: 'Protecting data from unauthorized disclosure and snooping',
  },
  {
    id: 'integrity',
    label: 'Integrity',
    icon: '🛡️',
    description: 'Guarding data against unauthorized tampering, alteration, or corruption',
  },
  {
    id: 'availability',
    label: 'Availability',
    icon: '⚡',
    description: 'Ensuring reliable, timely access to systems for authorized users',
  },
];

type IncidentAnswer = {
  pillar?: CiaPillar;
  threatIndex?: number;
  defenseIndex?: number;
  isVerified?: boolean;
};

interface CiaTriadClassifierProps {
  activitySlug?: string;
}

export default function CiaTriadClassifier({
  activitySlug = 'cfs-cia-triad-classifier',
}: CiaTriadClassifierProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, IncidentAnswer>>({});
  const [submitted, setSubmitted] = useState(false);
  const [showHint, setShowHint] = useState(false);

  const activeIncident = INCIDENTS[currentIndex];
  const activeAnswer = answers[activeIncident.id] || {};

  const evaluateIncident = useCallback((incident: IncidentData, answer: IncidentAnswer) => {
    const pillarCorrect = answer.pillar === incident.correctPillar;
    const threatCorrect = answer.threatIndex === incident.correctThreatIndex;
    const defenseCorrect = answer.defenseIndex === incident.correctDefenseIndex;
    const isComplete = Boolean(answer.pillar && answer.threatIndex !== undefined && answer.defenseIndex !== undefined);
    const isFullyCorrect = pillarCorrect && threatCorrect && defenseCorrect;
    return { pillarCorrect, threatCorrect, defenseCorrect, isComplete, isFullyCorrect };
  }, []);

  const overallResults = useMemo(() => {
    let totalScore = 0;
    const checks = INCIDENTS.map((incident) => {
      const ans = answers[incident.id] || {};
      const evalRes = evaluateIncident(incident, ans);
      // Each incident has 3 components: Pillar (40%), Threat (30%), Defense (30%)
      let points = 0;
      if (evalRes.pillarCorrect) points += 40;
      if (evalRes.threatCorrect) points += 30;
      if (evalRes.defenseCorrect) points += 30;
      totalScore += points;

      return {
        id: incident.id,
        label: incident.title,
        pass: evalRes.isFullyCorrect,
        points,
        evalRes,
      };
    });

    const averageScore = Math.round(totalScore / INCIDENTS.length);
    const passed = averageScore >= 70;
    const allAnswered = INCIDENTS.every((inc) => {
      const a = answers[inc.id];
      return a && a.pillar && a.threatIndex !== undefined && a.defenseIndex !== undefined;
    });

    return { checks, averageScore, passed, allAnswered };
  }, [answers, evaluateIncident]);

  const emitWorkspaceResult = useCallback(
    (action: 'check' | 'submit' | 'reset') => {
      if (action === 'reset') {
        window.dispatchEvent(
          new CustomEvent('workspace:result', {
            detail: {
              slug: activitySlug,
              action: 'reset',
              passed: false,
              score: 0,
              progress: 0,
              message: 'Triage reset',
              estMinutes: 10,
              difficulty: 'Beginner',
              checks: INCIDENTS.map((inc) => ({
                id: inc.id,
                label: inc.title,
                pass: false,
                message: 'Pending triage',
              })),
            },
          })
        );
        return;
      }

      window.dispatchEvent(
        new CustomEvent('workspace:result', {
          detail: {
            slug: activitySlug,
            action,
            passed: overallResults.passed,
            score: overallResults.averageScore,
            progress: overallResults.averageScore,
            message: overallResults.passed
              ? `Triage Complete: ${overallResults.averageScore}% Accuracy`
              : `Triage In Progress: ${overallResults.averageScore}% (Pass threshold is 70%)`,
            estMinutes: 10,
            difficulty: 'Beginner',
            checks: overallResults.checks.map((chk) => ({
              id: chk.id,
              label: chk.label,
              pass: chk.pass,
              message: chk.pass ? 'All triage criteria matched' : `${chk.points}/100 points`,
            })),
          },
        })
      );
    },
    [activitySlug, overallResults]
  );

  // Listen for bottom-bar WorkspaceLayout actions (Run, Check, Submit, Reset)
  useEffect(() => {
    const handleWorkspaceAction = (event: Event) => {
      const customEvent = event as CustomEvent;
      const detail = customEvent.detail as { action?: string; slug?: string };
      if (!detail || detail.slug !== activitySlug) return;

      if (detail.action === 'reset') {
        setAnswers({});
        setCurrentIndex(0);
        setSubmitted(false);
        setShowHint(false);
        emitWorkspaceResult('reset');
        return;
      }

      if (detail.action === 'check') {
        // Mark current incident as verified so feedback shows
        setAnswers((prev) => ({
          ...prev,
          [activeIncident.id]: {
            ...prev[activeIncident.id],
            isVerified: true,
          },
        }));
        emitWorkspaceResult('check');
        return;
      }

      if (detail.action === 'submit') {
        setSubmitted(true);
        // Verify all incidents
        setAnswers((prev) => {
          const updated = { ...prev };
          INCIDENTS.forEach((inc) => {
            updated[inc.id] = { ...updated[inc.id], isVerified: true };
          });
          return updated;
        });
        emitWorkspaceResult('submit');
      }
    };

    window.addEventListener('workspace:action', handleWorkspaceAction);
    return () => window.removeEventListener('workspace:action', handleWorkspaceAction);
  }, [activitySlug, activeIncident.id, emitWorkspaceResult]);

  const selectPillar = (pillar: CiaPillar) => {
    setAnswers((prev) => ({
      ...prev,
      [activeIncident.id]: {
        ...prev[activeIncident.id],
        pillar,
      },
    }));
  };

  const selectThreat = (threatIndex: number) => {
    setAnswers((prev) => ({
      ...prev,
      [activeIncident.id]: {
        ...prev[activeIncident.id],
        threatIndex,
      },
    }));
  };

  const selectDefense = (defenseIndex: number) => {
    setAnswers((prev) => ({
      ...prev,
      [activeIncident.id]: {
        ...prev[activeIncident.id],
        defenseIndex,
      },
    }));
  };

  const handleVerifyCurrent = () => {
    setAnswers((prev) => ({
      ...prev,
      [activeIncident.id]: {
        ...prev[activeIncident.id],
        isVerified: true,
      },
    }));
    emitWorkspaceResult('check');
  };

  const handleSubmitAll = () => {
    setSubmitted(true);
    setAnswers((prev) => {
      const updated = { ...prev };
      INCIDENTS.forEach((inc) => {
        updated[inc.id] = { ...updated[inc.id], isVerified: true };
      });
      return updated;
    });
    emitWorkspaceResult('submit');
  };

  const activeEval = evaluateIncident(activeIncident, activeAnswer);
  const isCurrentComplete = activeEval.isComplete;

  return (
    <div className="cia-classifier" data-testid="cia-classifier" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="pill pill--muted" style={{ fontWeight: 600, fontSize: '12px' }}>
            INCIDENT {currentIndex + 1} OF {INCIDENTS.length}
          </span>
          <span className="pill pill--pass" style={{ fontSize: '12px' }}>
            PASS ≥ 70%
          </span>
        </div>

        {/* Step dots */}
        <div style={{ display: 'flex', gap: '6px' }}>
          {INCIDENTS.map((inc, idx) => {
            const ans = answers[inc.id] || {};
            const res = evaluateIncident(inc, ans);
            const isDone = res.isComplete;
            const isCurrent = idx === currentIndex;
            return (
              <button
                key={inc.id}
                type="button"
                onClick={() => setCurrentIndex(idx)}
                style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '50%',
                  border: isCurrent ? '2px solid var(--accent-blue)' : '1px solid var(--border-subtle)',
                  background: isCurrent
                    ? 'rgba(56, 217, 255, 0.15)'
                    : isDone
                      ? ans.isVerified && res.isFullyCorrect
                        ? 'rgba(0, 255, 179, 0.15)'
                        : 'rgba(255, 255, 255, 0.05)'
                      : 'transparent',
                  color: isCurrent ? 'var(--accent-blue)' : 'var(--text-muted)',
                  fontSize: '12px',
                  fontWeight: 700,
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                }}
                title={inc.title}
                aria-label={`Jump to ${inc.title}`}
              >
                {ans.isVerified && res.isFullyCorrect ? '✓' : idx + 1}
              </button>
            );
          })}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar-track" role="progressbar" aria-valuenow={currentIndex + 1} aria-valuemin={1} aria-valuemax={INCIDENTS.length}>
        <div
          className="progress-bar-fill"
          style={{ width: `${((currentIndex + 1) / INCIDENTS.length) * 100}%` }}
        />
      </div>

      {/* Scenario Briefing Card */}
      <div
        className="card"
        style={{
          borderLeft: '4px solid var(--accent-blue)',
          padding: '16px 20px',
          background: 'rgba(56, 217, 255, 0.03)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
          <h3 style={{ margin: 0, fontSize: '18px', color: 'var(--text-bright)' }}>
            {activeIncident.title}
          </h3>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '12px', padding: '2px 8px' }}
            onClick={() => setShowHint(!showHint)}
          >
            {showHint ? 'Hide Hint' : '💡 Need Hint?'}
          </button>
        </div>

        <p style={{ margin: 0, fontSize: '14.5px', lineHeight: '1.6', color: 'var(--text-normal)' }}>
          {activeIncident.scenario}
        </p>

        {showHint && (
          <div
            className="callout callout--info"
            style={{ marginTop: '12px', fontSize: '13px', padding: '10px 14px' }}
          >
            <strong>Triage Tip:</strong> {activeIncident.hint}
          </div>
        )}
      </div>

      {/* Step 1: CIA Pillar Selection */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <label style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text-bright)' }}>
          Step 1: Which primary CIA Triad property was impacted first?
        </label>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
          {PILLAR_DEFINITIONS.map((pillar) => {
            const isSelected = activeAnswer.pillar === pillar.id;
            const isRevealed = Boolean(activeAnswer.isVerified);
            const isCorrect = isRevealed && pillar.id === activeIncident.correctPillar;
            const isWrongSelection = isRevealed && isSelected && pillar.id !== activeIncident.correctPillar;

            return (
              <button
                key={pillar.id}
                type="button"
                onClick={() => selectPillar(pillar.id)}
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  padding: '14px',
                  borderRadius: 'var(--radius-md, 8px)',
                  border: isCorrect
                    ? '2px solid var(--accent-green, #10b981)'
                    : isWrongSelection
                      ? '2px solid var(--danger, #ef4444)'
                      : isSelected
                        ? '2px solid var(--accent-purple, #a855f7)'
                        : '1px solid var(--border-subtle, rgba(255,255,255,0.1))',
                  background: isCorrect
                    ? 'rgba(0, 255, 179, 0.08)'
                    : isWrongSelection
                      ? 'rgba(255, 75, 129, 0.08)'
                      : isSelected
                        ? 'rgba(192, 132, 252, 0.08)'
                        : 'rgba(2, 5, 16, 0.5)',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                  <span style={{ fontSize: '18px' }}>{pillar.icon}</span>
                  <span style={{ fontWeight: 700, fontSize: '14px', color: isSelected ? 'var(--text-bright)' : 'var(--text-normal)' }}>
                    {pillar.label}
                  </span>
                </div>
                <span style={{ fontSize: '11.5px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                  {pillar.description}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Step 2: Threat Vector Selection */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <label style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text-bright)' }}>
          Step 2: Identify the root cause or attack vector:
        </label>
        <div className="quiz-options" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {activeIncident.threatOptions.map((opt, idx) => {
            const isSelected = activeAnswer.threatIndex === idx;
            const isRevealed = Boolean(activeAnswer.isVerified);
            const isCorrect = isRevealed && idx === activeIncident.correctThreatIndex;
            const isWrongSelection = isRevealed && isSelected && idx !== activeIncident.correctThreatIndex;

            const classes = [
              'quiz-option',
              isSelected ? 'quiz-option--selected' : '',
              isCorrect ? 'quiz-option--correct' : '',
              isWrongSelection ? 'quiz-option--incorrect' : '',
              isRevealed ? 'quiz-option--revealed' : '',
            ]
              .filter(Boolean)
              .join(' ');

            return (
              <div
                key={opt}
                className={classes}
                role="radio"
                aria-checked={isSelected}
                tabIndex={0}
                onClick={() => selectThreat(idx)}
              >
                <span className="quiz-option__letter">{String.fromCharCode(65 + idx)}</span>
                <span className="quiz-option__text" style={{ fontSize: '13.5px' }}>{opt}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Step 3: Immediate Defensive Action */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <label style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text-bright)' }}>
          Step 3: Select the immediate containment / defensive control:
        </label>
        <div className="quiz-options" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {activeIncident.defenseOptions.map((opt, idx) => {
            const isSelected = activeAnswer.defenseIndex === idx;
            const isRevealed = Boolean(activeAnswer.isVerified);
            const isCorrect = isRevealed && idx === activeIncident.correctDefenseIndex;
            const isWrongSelection = isRevealed && isSelected && idx !== activeIncident.correctDefenseIndex;

            const classes = [
              'quiz-option',
              isSelected ? 'quiz-option--selected' : '',
              isCorrect ? 'quiz-option--correct' : '',
              isWrongSelection ? 'quiz-option--incorrect' : '',
              isRevealed ? 'quiz-option--revealed' : '',
            ]
              .filter(Boolean)
              .join(' ');

            return (
              <div
                key={opt}
                className={classes}
                role="radio"
                aria-checked={isSelected}
                tabIndex={0}
                onClick={() => selectDefense(idx)}
              >
                <span className="quiz-option__letter">{String.fromCharCode(65 + idx)}</span>
                <span className="quiz-option__text" style={{ fontSize: '13.5px' }}>{opt}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Socratic Feedback Callout (When Verified) */}
      {activeAnswer.isVerified && (
        <div
          className={`callout ${activeEval.isFullyCorrect ? 'callout--success' : 'callout--warn'}`}
          style={{ padding: '14px 18px', borderRadius: 'var(--radius-md, 8px)' }}
        >
          <div style={{ fontWeight: 700, marginBottom: '6px', fontSize: '14px' }}>
            {activeEval.isFullyCorrect
              ? '🎯 Triage Verified: Accurate Classification!'
              : '⚠️ Partial Triage: Recheck Incident Details'}
          </div>
          <p style={{ margin: 0, fontSize: '13.5px', lineHeight: '1.5' }}>
            {activeIncident.socraticExplanation}
          </p>
        </div>
      )}

      {/* Overall Submission Banner (If Submitted) */}
      {submitted && (
        <div
          className={`callout ${overallResults.passed ? 'callout--success' : 'callout--error'}`}
          style={{ padding: '16px 20px', borderRadius: 'var(--radius-md, 8px)' }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h4 style={{ margin: 0, fontSize: '16px' }}>
              {overallResults.passed ? '🏆 Incident Triage Mission Complete!' : '⚠️ Triage Mastery Not Yet Achieved'}
            </h4>
            <span className="pill pill--pass" style={{ fontSize: '13px' }}>
              Overall Score: {overallResults.averageScore}%
            </span>
          </div>
          <p style={{ margin: '8px 0 0 0', fontSize: '13.5px' }}>
            {overallResults.passed
              ? 'Excellent analytical discipline. You accurately identified root causes, isolated the primary failure domain across the CIA Triad, and applied correct immediate defensive countermeasures.'
              : 'Review your incident triage selections and explanations above. Make corrections, verify your findings, and resubmit to pass.'}
          </p>
        </div>
      )}

      {/* Action and Navigation Toolbar */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderTop: '1px solid var(--border-subtle, rgba(255,255,255,0.08))',
          paddingTop: '16px',
          marginTop: '8px',
          flexWrap: 'wrap',
          gap: '12px',
        }}
      >
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            type="button"
            className="btn-ghost"
            disabled={currentIndex === 0}
            onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
            style={{ opacity: currentIndex === 0 ? 0.5 : 1, cursor: currentIndex === 0 ? 'not-allowed' : 'pointer' }}
          >
            ← Previous Incident
          </button>
          <button
            type="button"
            className="btn-ghost"
            disabled={currentIndex === INCIDENTS.length - 1}
            onClick={() => setCurrentIndex((prev) => Math.min(INCIDENTS.length - 1, prev + 1))}
            style={{
              opacity: currentIndex === INCIDENTS.length - 1 ? 0.5 : 1,
              cursor: currentIndex === INCIDENTS.length - 1 ? 'not-allowed' : 'pointer',
            }}
          >
            Next Incident →
          </button>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            type="button"
            className="btn-link"
            onClick={handleVerifyCurrent}
            disabled={!isCurrentComplete}
            style={{
              fontSize: '13.5px',
              padding: '8px 16px',
              opacity: !isCurrentComplete ? 0.5 : 1,
              cursor: !isCurrentComplete ? 'not-allowed' : 'pointer',
            }}
          >
            <span>Verify Incident {currentIndex + 1}</span>
            <span className="icon-directional">✓</span>
          </button>

          <button
            type="button"
            className="btn-link"
            onClick={handleSubmitAll}
            disabled={!overallResults.allAnswered}
            style={{
              fontSize: '13.5px',
              padding: '8px 18px',
              background: overallResults.allAnswered ? 'var(--accent-purple, #a855f7)' : undefined,
              borderColor: overallResults.allAnswered ? 'var(--accent-purple, #a855f7)' : undefined,
              color: overallResults.allAnswered ? '#ffffff' : undefined,
              opacity: !overallResults.allAnswered ? 0.5 : 1,
              cursor: !overallResults.allAnswered ? 'not-allowed' : 'pointer',
            }}
          >
            <span>Submit Triage Report</span>
            <span className="icon-directional">→</span>
          </button>
        </div>
      </div>
    </div>
  );
}
