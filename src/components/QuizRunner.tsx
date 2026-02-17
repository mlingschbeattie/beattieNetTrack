import { useEffect, useMemo, useState } from 'react';
import { gradeQuiz, type QuizAnswer, type QuizDefinition } from '../lib/quizEngine';

type QuizRunnerProps = {
  quiz: QuizDefinition;
  workspaceSlug?: string;
};

const storageKey = (slug: string) => `quiz-runner:${slug}`;

export default function QuizRunner({ quiz, workspaceSlug }: QuizRunnerProps) {
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, QuizAnswer>>({});
  const [showResults, setShowResults] = useState(false);

  const grade = useMemo(() => gradeQuiz(quiz, answers), [quiz, answers]);
  const activeQuestion = quiz.questions[current];

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      const raw = window.localStorage.getItem(storageKey(quiz.slug));
      if (!raw) return;
      const parsed = JSON.parse(raw) as { answers?: Record<string, QuizAnswer>; current?: number };
      if (parsed.answers && typeof parsed.answers === 'object') {
        setAnswers(parsed.answers);
      }
      if (typeof parsed.current === 'number') {
        setCurrent(Math.max(0, Math.min(quiz.questions.length - 1, parsed.current)));
      }
    } catch {
      // ignore malformed cache
    }
  }, [quiz.slug, quiz.questions.length]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    window.localStorage.setItem(
      storageKey(quiz.slug),
      JSON.stringify({ answers, current })
    );
  }, [quiz.slug, answers, current]);

  const setSingle = (questionId: string, selectedIndex: number) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: { type: 'single', selectedIndex },
    }));
  };

  const toggleMulti = (questionId: string, optionIndex: number) => {
    setAnswers((prev) => {
      const existing = prev[questionId];
      const selected = existing?.type === 'multi' ? existing.selectedIndices : [];
      const next = selected.includes(optionIndex)
        ? selected.filter((entry) => entry !== optionIndex)
        : [...selected, optionIndex];
      return {
        ...prev,
        [questionId]: { type: 'multi', selectedIndices: next },
      };
    });
  };

  const setShort = (questionId: string, value: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: { type: 'short', value },
    }));
  };

  const canAdvance = () => {
    const answer = answers[activeQuestion.id];
    if (!answer) return false;
    if (answer.type === 'single') return answer.selectedIndex != null;
    if (answer.type === 'multi') return answer.selectedIndices.length > 0;
    return answer.value.trim().length > 0;
  };

  const emitWorkspaceResult = (action: 'check' | 'submit' | 'reset') => {
    if (!workspaceSlug) return;

    if (action === 'reset') {
      window.dispatchEvent(
        new CustomEvent('workspace:result', {
          detail: {
            slug: workspaceSlug,
            action,
            passed: false,
            score: 0,
            progress: 0,
            message: 'Quiz reset',
          },
        })
      );
      return;
    }

    const missed = grade.results.filter((result) => !result.correct);

    window.dispatchEvent(
      new CustomEvent('workspace:result', {
        detail: {
          slug: workspaceSlug,
          action,
          passed: grade.passed,
          score: grade.score,
          progress: grade.score,
          message: grade.passed ? 'Quiz passed' : 'Quiz not yet passing',
          estMinutes: 15,
          difficulty: 'Intermediate',
          checks: [
            {
              id: 'quiz-threshold',
              label: `Reached pass threshold ${quiz.passThreshold}%`,
              pass: grade.passed,
              message: `Score ${grade.score}%`,
            },
            ...missed.slice(0, 4).map((result) => ({
              id: `quiz-${result.id}`,
              label: `Question ${result.id}`,
              pass: false,
              message: result.feedback,
            })),
          ],
        },
      })
    );
  };

  useEffect(() => {
    const onAction = (event: Event) => {
      const customEvent = event as CustomEvent;
      const detail = customEvent.detail as { action?: string; slug?: string };
      if (!detail || detail.slug !== (workspaceSlug ?? quiz.slug)) return;

      if (detail.action === 'reset') {
        setAnswers({});
        setCurrent(0);
        setShowResults(false);
        emitWorkspaceResult('reset');
        return;
      }

      if (detail.action === 'check' || detail.action === 'submit') {
        setShowResults(true);
        emitWorkspaceResult(detail.action);
      }
    };

    window.addEventListener('workspace:action', onAction);
    return () => window.removeEventListener('workspace:action', onAction);
  }, [workspaceSlug, quiz.slug, grade]);

  if (!activeQuestion) {
    return <div className="quiz-card">No questions found.</div>;
  }

  const activeResult = grade.results.find((result) => result.id === activeQuestion.id);

  return (
    <div className="quiz-card" data-testid="quiz-runner">
      <div className="quiz-card__header">
        <div>
          <h2>{quiz.title}</h2>
          <div className="quiz-card__meta">
            Question {current + 1} of {quiz.questions.length}
          </div>
        </div>
        <div className="pill">Pass {quiz.passThreshold}%</div>
      </div>

      <div className="progress progress--thin" aria-hidden="true">
        <div className="progress__bar" style={{ width: `${quiz.questions.length ? ((current + 1) / quiz.questions.length) * 100 : 0}%` }}></div>
      </div>

      <div className="quiz-question">
        <h3>{activeQuestion.prompt}</h3>
        <div className="quiz-options">
          {activeQuestion.type === 'single' &&
            activeQuestion.options.map((option, index) => {
              const answer = answers[activeQuestion.id];
              const selected = answer?.type === 'single' ? answer.selectedIndex === index : false;
              return (
                <button
                  key={option}
                  type="button"
                  className={`quiz-option ${selected ? 'quiz-option--selected' : ''}`}
                  data-testid={`quiz-option-${index}`}
                  onClick={() => setSingle(activeQuestion.id, index)}
                >
                  {option}
                </button>
              );
            })}

          {activeQuestion.type === 'multi' &&
            activeQuestion.options.map((option, index) => {
              const answer = answers[activeQuestion.id];
              const selected = answer?.type === 'multi' ? answer.selectedIndices.includes(index) : false;
              return (
                <button
                  key={option}
                  type="button"
                  className={`quiz-option ${selected ? 'quiz-option--selected' : ''}`}
                  onClick={() => toggleMulti(activeQuestion.id, index)}
                >
                  {option}
                </button>
              );
            })}

          {activeQuestion.type === 'short' && (
            (() => {
              const answer = answers[activeQuestion.id];
              const value = answer?.type === 'short' ? answer.value : '';
              return (
            <input
              className="quiz-short-input"
              type="text"
              value={value}
              onChange={(event) => setShort(activeQuestion.id, event.target.value)}
              placeholder="Type your answer"
              data-testid="quiz-short-input"
            />
              );
            })()
          )}
        </div>
      </div>

      {showResults && activeResult && (
        <div className={`quiz-feedback ${activeResult.correct ? 'quiz-feedback--ok' : 'quiz-feedback--error'}`}>
          {activeResult.feedback}
        </div>
      )}

      <div className="quiz-actions">
        <button className="btn-secondary" type="button" onClick={() => setCurrent((prev) => Math.max(0, prev - 1))} disabled={current === 0}>
          Back
        </button>
        {current < quiz.questions.length - 1 ? (
          <button className="btn-primary" type="button" onClick={() => {
            setCurrent((prev) => Math.min(quiz.questions.length - 1, prev + 1));
          }} disabled={!canAdvance()}>
            Next
          </button>
        ) : (
          <button className="btn-primary" type="button" data-testid="quiz-submit" onClick={() => {
            setShowResults(true);
            emitWorkspaceResult('submit');
          }} disabled={!canAdvance()}>
            Submit
          </button>
        )}
      </div>

      {showResults && (
        <div className="quiz-card__results" data-testid="quiz-results">
          <strong data-testid="quiz-score">{grade.score}%</strong>
          <span>
            {grade.correctCount}/{grade.total} correct · {grade.passed ? 'Passed' : 'Try again'}
          </span>
          <button className="btn-ghost" type="button" onClick={() => {
            setAnswers({});
            setCurrent(0);
            setShowResults(false);
            emitWorkspaceResult('reset');
          }}>
            Retake
          </button>
        </div>
      )}
    </div>
  );
}
