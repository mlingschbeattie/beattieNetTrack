import { useEffect, useState } from 'react';
import type { PublicQuiz, QuizAnswer, ServerQuizResult } from '../lib/quizEngine';
import type { DomainMapping } from '../types/lab';

type QuizRunnerProps = {
  quiz: PublicQuiz;
  workspaceSlug?: string;
  domains?: DomainMapping[];
  apiUrl?: string;
};

const storageKey = (slug: string) => `quiz-runner:${slug}`;

// The browser never has the answer key. Submit sends the answers to the hub, which grades
// them, records the score and returns the results with the correct answers. Check only says
// how many questions are answered.
const submitUrl = (slug: string) => `/api/lms/quizzes/${encodeURIComponent(slug)}/submit`;

export default function QuizRunner({ quiz, workspaceSlug }: QuizRunnerProps) {
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, QuizAnswer>>({});
  const [result, setResult] = useState<ServerQuizResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const showResults = result !== null;
  const activeQuestion = quiz.questions[current];
  const activeResult = result?.results.find((entry) => entry.id === activeQuestion?.id);
  const answerFeedback = showResults && activeResult ? (activeResult.correct ? 'Correct' : 'Incorrect') : null;
  const explanationText = (activeResult?.explanation ?? '').trim();
  const showExplanation = showResults && !!activeResult && !activeResult.correct && explanationText.length > 0;

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      const raw = window.localStorage.getItem(storageKey(quiz.slug));
      if (!raw) return;
      const parsed = JSON.parse(raw) as { answers?: Record<string, QuizAnswer>; current?: number };
      if (parsed.answers && typeof parsed.answers === 'object') setAnswers(parsed.answers);
      if (typeof parsed.current === 'number') {
        setCurrent(Math.max(0, Math.min(quiz.questions.length - 1, parsed.current)));
      }
    } catch {
      // ignore malformed cache
    }
  }, [quiz.slug, quiz.questions.length]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      window.localStorage.setItem(storageKey(quiz.slug), JSON.stringify({ answers, current }));
    } catch {
      // storage full or blocked: answers stay in memory
    }
  }, [quiz.slug, answers, current]);

  const setSingle = (questionId: string, selectedIndex: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: { type: 'single', selectedIndex } }));
  };

  const toggleMulti = (questionId: string, optionIndex: number) => {
    setAnswers((prev) => {
      const existing = prev[questionId];
      const selected = existing?.type === 'multi' ? existing.selectedIndices : [];
      const next = selected.includes(optionIndex)
        ? selected.filter((entry) => entry !== optionIndex)
        : [...selected, optionIndex];
      return { ...prev, [questionId]: { type: 'multi', selectedIndices: next } };
    });
  };

  const setShort = (questionId: string, value: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: { type: 'short', value } }));
  };

  const isAnswered = (questionId: string) => {
    const answer = answers[questionId];
    if (!answer) return false;
    if (answer.type === 'single') return answer.selectedIndex != null;
    if (answer.type === 'multi') return answer.selectedIndices.length > 0;
    return answer.value.trim().length > 0;
  };

  const canAdvance = () => !!activeQuestion && isAnswered(activeQuestion.id);
  const answeredCount = quiz.questions.filter((q) => isAnswered(q.id)).length;

  const dispatchResult = (detail: Record<string, unknown>) => {
    if (!workspaceSlug) return;
    window.dispatchEvent(new CustomEvent('workspace:result', { detail: { slug: workspaceSlug, ...detail } }));
  };

  const reset = () => {
    setAnswers({});
    setCurrent(0);
    setResult(null);
    setError(null);
    dispatchResult({ action: 'reset', passed: false, score: 0, progress: 0, message: 'Quiz reset' });
  };

  const check = () => {
    const total = quiz.questions.length;
    dispatchResult({
      action: 'check',
      passed: false,
      progress: total ? Math.round((answeredCount / total) * 100) : 0,
      message: `${answeredCount} of ${total} answered. Answers are shown after you submit.`,
      checks: [
        {
          id: 'quiz-answered',
          label: 'Every question answered',
          pass: answeredCount === total,
          message: `${answeredCount} of ${total} answered`,
        },
      ],
    });
  };

  const submit = async () => {
    if (submitting || showResults) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch(submitUrl(quiz.slug), {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers }),
      });
      const body = (await res.json().catch(() => ({}))) as Partial<ServerQuizResult> & { message?: string };
      if (!res.ok || typeof body.score !== 'number' || !Array.isArray(body.results)) {
        throw new Error(body.message || `Could not submit (HTTP ${res.status}). Your answers are saved; try again.`);
      }
      const graded = body as ServerQuizResult;
      setResult(graded);
      const missed = graded.results.filter((entry) => !entry.correct);
      dispatchResult({
        action: 'submit',
        passed: graded.passed,
        score: graded.score,
        progress: graded.score,
        message: graded.passed ? 'Quiz passed' : 'Quiz not yet passing',
        estMinutes: 15,
        difficulty: 'Intermediate',
        checks: [
          {
            id: 'quiz-threshold',
            label: `Reached pass threshold ${quiz.passThreshold}%`,
            pass: graded.passed,
            message: `Score ${graded.score}%`,
          },
          ...missed.slice(0, 4).map((entry) => ({
            id: `quiz-${entry.id}`,
            label: `Question ${entry.id}`,
            pass: false,
            message: entry.explanation ?? 'Review this question.',
          })),
        ],
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not submit. Your answers are saved; try again.');
    } finally {
      setSubmitting(false);
    }
  };

  useEffect(() => {
    const onAction = (event: Event) => {
      const detail = (event as CustomEvent).detail as { action?: string; slug?: string };
      if (!detail || detail.slug !== (workspaceSlug ?? quiz.slug)) return;
      if (detail.action === 'reset') reset();
      else if (detail.action === 'check') check();
      else if (detail.action === 'submit') void submit();
    };
    window.addEventListener('workspace:action', onAction);
    return () => window.removeEventListener('workspace:action', onAction);
  });

  if (!activeQuestion) {
    return <div className="quiz-runner">No questions found.</div>;
  }

  const optionClasses = (selected: boolean, isCorrect: boolean) =>
    [
      'quiz-option',
      selected ? 'quiz-option--selected' : '',
      isCorrect ? 'quiz-option--correct' : '',
      showResults && selected && !isCorrect ? 'quiz-option--incorrect' : '',
      showResults ? 'quiz-option--revealed' : '',
    ]
      .filter(Boolean)
      .join(' ');

  return (
    <div className="quiz-runner" data-testid="quiz-runner">
      <div className="quiz-runner__header">
        <div className="quiz-runner__counter">
          QUESTION {current + 1} OF {quiz.questions.length}
        </div>
        <div className="pill pill--pass">PASS ≥ {quiz.passThreshold}%</div>
      </div>

      <div
        className="progress-bar-track"
        role="progressbar"
        aria-valuenow={current + 1}
        aria-valuemin={1}
        aria-valuemax={quiz.questions.length}
        aria-label={`Question ${current + 1} of ${quiz.questions.length}`}
      >
        <div
          className="progress-bar-fill"
          style={{ width: `${quiz.questions.length ? ((current + 1) / quiz.questions.length) * 100 : 0}%` }}
        />
      </div>

      <div className="quiz-question">
        <p className="quiz-question__prompt" id={`quiz-prompt-${activeQuestion.id}`}>{activeQuestion.prompt}</p>
        <div
          className="quiz-options"
          role={activeQuestion.type === 'single' ? 'radiogroup' : activeQuestion.type === 'multi' ? 'group' : undefined}
          aria-labelledby={`quiz-prompt-${activeQuestion.id}`}
        >
          {activeQuestion.type === 'single' &&
            activeQuestion.options.map((option, index) => {
              const answer = answers[activeQuestion.id];
              const selected = answer?.type === 'single' ? answer.selectedIndex === index : false;
              const isCorrect = showResults && activeResult?.correctIndex === index;
              return (
                <div
                  key={`${index}-${option}`}
                  role="radio"
                  aria-checked={selected}
                  tabIndex={showResults ? -1 : 0}
                  className={optionClasses(selected, isCorrect)}
                  data-testid={`quiz-option-${index}`}
                  onClick={() => !showResults && setSingle(activeQuestion.id, index)}
                  onKeyDown={(e) => {
                    if (!showResults && (e.key === 'Enter' || e.key === ' ')) {
                      e.preventDefault();
                      setSingle(activeQuestion.id, index);
                    }
                  }}
                >
                  <span className="quiz-option__letter">{String.fromCharCode(65 + index)}</span>
                  <span className="quiz-option__text">{option}</span>
                </div>
              );
            })}

          {activeQuestion.type === 'multi' &&
            activeQuestion.options.map((option, index) => {
              const answer = answers[activeQuestion.id];
              const selected = answer?.type === 'multi' ? answer.selectedIndices.includes(index) : false;
              const isCorrect = showResults && !!activeResult?.correctIndices?.includes(index);
              return (
                <div
                  key={`${index}-${option}`}
                  role="checkbox"
                  aria-checked={selected}
                  tabIndex={showResults ? -1 : 0}
                  className={optionClasses(selected, isCorrect)}
                  onClick={() => !showResults && toggleMulti(activeQuestion.id, index)}
                  onKeyDown={(e) => {
                    if (!showResults && (e.key === 'Enter' || e.key === ' ')) {
                      e.preventDefault();
                      toggleMulti(activeQuestion.id, index);
                    }
                  }}
                >
                  <span className="quiz-option__letter">{String.fromCharCode(65 + index)}</span>
                  <span className="quiz-option__text">{option}</span>
                </div>
              );
            })}

          {activeQuestion.type === 'short' &&
            (() => {
              const answer = answers[activeQuestion.id];
              const value = answer?.type === 'short' ? answer.value : '';
              return (
                <>
                  <input
                    className="quiz-short-input"
                    type="text"
                    value={value}
                    readOnly={showResults}
                    onChange={(event) => setShort(activeQuestion.id, event.target.value)}
                    placeholder="Type your answer"
                    aria-labelledby={`quiz-prompt-${activeQuestion.id}`}
                    data-testid="quiz-short-input"
                  />
                  {showResults && !activeResult?.correct && activeResult?.acceptedAnswers?.length ? (
                    <p className="quiz-answer-accepted">Accepted answers include: {activeResult.acceptedAnswers.join(', ')}</p>
                  ) : null}
                </>
              );
            })()}
        </div>
      </div>

      {answerFeedback && (
        <div
          className={activeResult?.correct ? 'quiz-answer-feedback quiz-answer-feedback--correct' : 'quiz-answer-feedback quiz-answer-feedback--incorrect'}
          role="status"
          aria-live="polite"
        >
          {answerFeedback}
        </div>
      )}

      {showExplanation && (
        <div className="quiz-eli5" role="note" aria-label="Explanation">
          <div className="quiz-eli5__body">
            <strong>Here's why:</strong> {explanationText}
          </div>
        </div>
      )}

      {error && (
        <div className="quiz-answer-feedback quiz-answer-feedback--incorrect" role="alert" data-testid="quiz-error">
          {error}
        </div>
      )}

      <div className="quiz-runner__actions">
        <button
          className="quiz-btn quiz-btn--ghost"
          type="button"
          onClick={() => setCurrent((prev) => Math.max(0, prev - 1))}
          disabled={current === 0}
        >
          Back
        </button>
        {current < quiz.questions.length - 1 ? (
          <button
            className="quiz-btn quiz-btn--primary"
            type="button"
            onClick={() => setCurrent((prev) => Math.min(quiz.questions.length - 1, prev + 1))}
            disabled={!canAdvance() && !showResults}
          >
            Next
          </button>
        ) : (
          !showResults && (
            <button
              className="quiz-btn quiz-btn--primary"
              type="button"
              data-testid="quiz-submit"
              onClick={() => void submit()}
              disabled={!canAdvance() || submitting}
            >
              {submitting ? 'Grading...' : 'Submit'}
            </button>
          )
        )}
      </div>

      {showResults && result && (
        <div className="quiz-results" data-testid="quiz-results">
          <div className="quiz-results__score" data-testid="quiz-score">{result.score}%</div>
          <div className="quiz-results__label">
            {result.correctCount}/{result.total} correct
          </div>
          <div className={result.passed ? 'quiz-results__pass' : 'quiz-results__fail'}>
            {result.passed ? '✓ Passed' : '✗ Try again'}
          </div>
          {result.countsAs === 'practice' && (
            <div className="quiz-results__label" data-testid="quiz-practice-note">
              Retake: this attempt is recorded as practice, since the answers were shown before.
            </div>
          )}
          <button className="quiz-btn quiz-btn--ghost" type="button" onClick={reset}>
            Retake
          </button>
        </div>
      )}
    </div>
  );
}
