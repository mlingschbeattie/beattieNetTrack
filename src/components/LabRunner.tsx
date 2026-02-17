import { useEffect, useMemo, useState } from 'react';
import { getLabState, markLabCompleted, saveLabState } from '../lib/progressStore';

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
}: LabRunnerProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [completedStepIds, setCompletedStepIds] = useState<string[]>([]);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const totalSteps = steps.length;
  const progressPercent = totalSteps > 0 ? Math.round(((currentStepIndex + 1) / totalSteps) * 100) : 0;

  useEffect(() => {
    const state = getLabState(labSlug);
    const safeIndex = Math.max(0, Math.min(state.lastStepIndex ?? 0, Math.max(steps.length - 1, 0)));
    setCurrentStepIndex(safeIndex);
    setCompletedStepIds(state.completedStepIds ?? []);
    setIsCompleted(Boolean(state.completed));
  }, [labSlug, steps.length]);

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
      const completedAt = new Date().toISOString();
      setIsCompleted(true);
      persist({
        completedStepIds: nextCompleted,
        completed: true,
        completedAt,
      });
      markLabCompleted(labSlug, xpReward);
      window.dispatchEvent(new CustomEvent('progress-updated'));
      return;
    }

    persist({
      lastStepIndex: currentStepIndex,
      completedStepIds: nextCompleted,
      completed: false,
      completedAt: null,
    });
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
    <div className="card" data-testid="lab-runner">
      <div className="card__meta">
        <span className="badge" data-testid="lab-step-count">Step {currentStepIndex + 1} of {totalSteps}</span>
      </div>
      <div className="progress progress--thin" aria-hidden="true">
        <div className="progress__bar" style={{ width: `${progressPercent}%` }}></div>
      </div>

      <h3>{currentStep.title}</h3>
      <p>{currentStep.prompt}</p>

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

      <div className="card__footer u-mt-3">
        <button className="btn" type="button" data-testid="lab-submit" onClick={handleSubmit}>Submit</button>
        <button
          className="btn-ghost"
          type="button"
          data-testid="lab-hint"
          onClick={() => setShowHint((prev) => !prev)}
        >
          {showHint ? 'Hide hint' : 'Show hint'}
        </button>
        <button
          className="btn"
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
        <div className={`callout u-mt-3 ${feedback.type === 'success' ? 'callout--success' : 'callout--warn'}`}>
          {feedback.message}
        </div>
      )}
    </div>
  );
}
