import { useEffect, useMemo, useState } from 'react';
import { getLabState, markLabCompleted, saveLabState } from '../lib/progressStore';
import { startBeaconSession } from '../lib/cis/beacon';
import { emitLabStarted, emitLabCompleted, type CISDomainTag } from '../lib/events';
import type { DomainMapping } from '../types/lab';

type ExactValidator = {
  type: 'exact';
  value: string;
};

type OneOfValidator = {
  type: 'oneOf';
  values: string[];
};

type RegexValidator = {
  type: 'regex';
  pattern: string;
  flags?: string;
};

type StepValidator = ExactValidator | OneOfValidator | RegexValidator;

type LabStep = {
  id: string;
  title: string;
  prompt: string;
  inputLabel?: string;
  placeholder?: string;
  hint?: string;
  validator: StepValidator;
  successMessage?: string;
};

type LabRunnerProps = {
  labSlug: string;
  title: string;
  steps: readonly LabStep[];
  xpReward: number;
  backToTrackHref?: string;
  domains?: DomainMapping[];
  apiUrl?: string;
};

const validateAnswer = (value: string, validator: StepValidator) => {
  if (validator.type === 'exact') {
    return value === validator.value.trim();
  }
  if (validator.type === 'oneOf') {
    const accepted = new Set(validator.values.map((entry) => entry.trim()));
    return accepted.has(value);
  }
  try {
    const pattern = new RegExp(validator.pattern, validator.flags);
    return pattern.test(value);
  } catch {
    return false;
  }
};

export default function LabRunner({
  labSlug,
  title,
  steps,
  xpReward,
  backToTrackHref = '/tracks/network-engineer',
  domains = [],
  apiUrl = '',
}: LabRunnerProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [completedStepIds, setCompletedStepIds] = useState<string[]>([]);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [toastMsg, setToastMsg] = useState('');

  const totalSteps = steps.length;
  const progressPercent = totalSteps > 0 ? Math.round(((currentStepIndex + 1) / totalSteps) * 100) : 0;

  useEffect(() => {
    const state = getLabState(labSlug);
    const safeIndex = Math.max(0, Math.min(state.lastStepIndex ?? 0, Math.max(steps.length - 1, 0)));
    setCurrentStepIndex(safeIndex);
    setCompletedStepIds(state.completedStepIds ?? []);
    setIsCompleted(Boolean(state.completed));
  }, [labSlug, steps.length]);

  // CIS time-beacon: emit active-time pings every 30 s while student is working
  useEffect(() => {
    if (!apiUrl || domains.length === 0) return;
    const cisDomains: CISDomainTag[] = domains.map((d) => ({
      domainId: d.domainId,
      weight: d.weight ?? 1.0,
    }));
    const stop = startBeaconSession({
      domains: cisDomains,
      contentType: 'lab',
      contentId: labSlug,
      apiUrl,
    });
    return stop;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // CIS events: emit lab_started once per day on mount
  useEffect(() => {
    if (!apiUrl || domains.length === 0) return;
    const cisDomains: CISDomainTag[] = domains.map((d) => ({
      domainId: d.domainId,
      weight: d.weight ?? 1.0,
    }));
    emitLabStarted(labSlug, title, cisDomains, apiUrl);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const currentStep = useMemo(() => {
    if (steps.length === 0) return null;
    return steps[Math.max(0, Math.min(currentStepIndex, steps.length - 1))];
  }, [currentStepIndex, steps]);

  const currentAnswer = currentStep ? answers[currentStep.id] ?? '' : '';
  const currentStepCompleted = currentStep ? completedStepIds.includes(currentStep.id) : false;

  const persist = (partial: {
    lastStepIndex?: number;
    completedStepIds?: string[];
    completed?: boolean;
    completedAt?: string | null;
    xpAwarded?: boolean;
    xpEarned?: number;
  }) => {
    saveLabState(labSlug, {
      startedAt: new Date().toISOString(),
      ...partial,
    });
  };

  const handleSubmit = () => {
    if (!currentStep || isCompleted) return;
    const trimmed = (answers[currentStep.id] ?? '').trim();
    const passed = validateAnswer(trimmed, currentStep.validator);

    if (!passed) {
      setFeedback({ type: 'error', message: 'Not quite. Check the prompt and try again.' });
      return;
    }

    const nextCompleted = Array.from(new Set([...completedStepIds, currentStep.id]));
    const allDone = steps.every((step) => nextCompleted.includes(step.id));
    const successMessage = currentStep.successMessage ?? 'Correct. You can continue to the next step.';

    setCompletedStepIds(nextCompleted);
    setFeedback({ type: 'success', message: successMessage });

    if (allDone) {
      setToastMsg(`✓ Lab complete! +${xpReward} XP`);
      setTimeout(() => setToastMsg(''), 1500);
      const completedAt = new Date().toISOString();
      setIsCompleted(true);
      persist({
        completedStepIds: nextCompleted,
        completed: true,
        completedAt,
      });
      markLabCompleted(labSlug, xpReward);
      window.dispatchEvent(new CustomEvent('progress-updated'));
      // CIS event: emit lab_completed once (guarded by localStorage flag inside emitLabCompleted)
      if (apiUrl && domains.length > 0) {
        const cisDomains: CISDomainTag[] = domains.map((d) => ({
          domainId: d.domainId,
          weight: d.weight ?? 1.0,
        }));
        emitLabCompleted(labSlug, Object.keys(answers).length, cisDomains, apiUrl);
      }
      // Submit lab to server: saves answers + records initial mastery placeholder
      if (apiUrl) {
        fetch(`${apiUrl}/api/lms/labs/${labSlug}/submit`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            answers,
            completedAt: completedAt,
          }),
        }).catch(() => {});
      }
      return;
    }

    persist({
      lastStepIndex: currentStepIndex,
      completedStepIds: nextCompleted,
      completed: false,
      completedAt: null,
    });
    setToastMsg('✓ Step complete!');
    setTimeout(() => setToastMsg(''), 1500);
  };

  const handleNext = () => {
    const nextIndex = Math.min(currentStepIndex + 1, Math.max(steps.length - 1, 0));
    setCurrentStepIndex(nextIndex);
    setFeedback(null);
    setShowHint(false);
    persist({ lastStepIndex: nextIndex, completedStepIds, completed: false, completedAt: null });
  };

  if (!currentStep) {
    return (
      <article className="card" data-testid="lab-runner">
        <h3>Lab unavailable</h3>
        <p>No steps are configured for this lab yet.</p>
      </article>
    );
  }

  if (isCompleted) {
    return (
      <article className="card" data-testid="lab-complete">
        <h3>{title} complete</h3>
        <p>You earned {xpReward} XP.</p>
        <a className="btn-link" href={backToTrackHref}>Back to Track →</a>
      </article>
    );
  }

  return (
    <div className="lab-layout" data-testid="lab-runner">
      <aside className="lab-steps">
        <div className="lab-steps__title">Lab Steps</div>
        {steps.map((step, index) => {
          const isDone = completedStepIds.includes(step.id);
          const isActive = index === currentStepIndex;
          const isLocked = !isDone && !isActive;
          return (
            <div
              key={step.id}
              className={`lab-step${isActive ? ' lab-step--active' : ''}${isDone ? ' lab-step--complete' : ''}${isLocked ? ' lab-step--locked' : ''}`}
            >
              <span className="lab-step__num">{isDone ? '' : index + 1}</span>
              <span>{step.title}</span>
            </div>
          );
        })}
      </aside>

      <div>
        <div className="progress-bar-track" aria-hidden="true">
          <div className="progress-bar-fill" style={{ width: `${progressPercent}%` }} />
        </div>

        <div className="lab-instruction">
          <div className="lab-instruction__eyebrow" data-testid="lab-step-count">
            Step {currentStepIndex + 1} of {totalSteps}
          </div>
          <h3 className="lab-instruction__title">{currentStep.title}</h3>
          <div className="lab-instruction__body">{currentStep.prompt}</div>
        </div>

        <label className="u-block u-mb-2" htmlFor={`lab-input-${currentStep.id}`}>
          {currentStep.inputLabel ?? 'Command'}
        </label>
        <input
          id={`lab-input-${currentStep.id}`}
          className="input"
          data-testid="lab-input"
          type="text"
          value={currentAnswer}
          placeholder={currentStep.placeholder ?? 'Type your answer'}
          onChange={(event) => {
            const value = event.target.value;
            setAnswers((prev) => ({ ...prev, [currentStep.id]: value }));
          }}
        />

        <div className="quiz-runner__actions">
          <button className="quiz-btn quiz-btn--primary" type="button" data-testid="lab-submit" onClick={handleSubmit}>
            Submit
          </button>
          <button
            className="quiz-btn quiz-btn--ghost"
            type="button"
            data-testid="lab-hint"
            onClick={() => setShowHint((prev) => !prev)}
          >
            {showHint ? 'Hide hint' : 'Show hint'}
          </button>
          <button
            className="quiz-btn quiz-btn--primary"
            type="button"
            data-testid="lab-next"
            disabled={!currentStepCompleted}
            onClick={handleNext}
          >
            Next
          </button>
        </div>

        {showHint && currentStep.hint && (
          <div className="callout callout--info u-mt-3">
            <strong>Hint:</strong> {currentStep.hint}
          </div>
        )}

        {feedback && (
          <div className={`callout u-mt-3 ${feedback.type === 'success' ? 'callout--tip' : 'callout--warn'}`}>
            {feedback.message}
          </div>
        )}
      </div>

      {toastMsg && <div className="step-toast">{toastMsg}</div>}
    </div>
  );
}
