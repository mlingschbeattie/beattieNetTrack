import { useEffect, useState } from 'react';

interface StudentAnswer {
  studentId: string;
  studentName: string;
  answers: Record<string, string>;
  submittedAt: string | null;
}

interface GradeEntryProps {
  labId: string;
  labTitle: string;
  apiUrl: string;
}

type GradeState = 'idle' | 'saving' | 'saved' | 'error';

export default function GradeEntry({ labId, labTitle, apiUrl }: GradeEntryProps) {
  const [students, setStudents] = useState<StudentAnswer[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [scores, setScores] = useState<Record<string, string>>({});
  const [gradeStates, setGradeStates] = useState<Record<string, GradeState>>({});

  useEffect(() => {
    fetch(`${apiUrl}/api/lms/labs/${labId}/answers`, { credentials: 'include' })
      .then((res) => {
        if (!res.ok) throw new Error(`Server returned ${res.status}`);
        return res.json() as Promise<StudentAnswer[]>;
      })
      .then((data) => {
        setStudents(data);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setFetchError(err instanceof Error ? err.message : 'Failed to load answers');
        setLoading(false);
      });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleGrade = async (studentId: string) => {
    const raw = scores[studentId] ?? '';
    const score = parseInt(raw, 10);
    if (Number.isNaN(score) || score < 0 || score > 100) {
      setGradeStates((prev) => ({ ...prev, [studentId]: 'error' }));
      return;
    }

    setGradeStates((prev) => ({ ...prev, [studentId]: 'saving' }));

    try {
      const res = await fetch(`${apiUrl}/api/lms/labs/${labId}/grade`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentId, score }),
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      setGradeStates((prev) => ({ ...prev, [studentId]: 'saved' }));
    } catch {
      setGradeStates((prev) => ({ ...prev, [studentId]: 'error' }));
    }
  };

  if (loading) {
    return (
      <div className="card" data-testid="grade-entry-loading">
        <p>Loading student answers…</p>
      </div>
    );
  }

  if (fetchError) {
    return (
      <div className="card" data-testid="grade-entry-error">
        <p className="callout callout--warn">Failed to load answers: {fetchError}</p>
      </div>
    );
  }

  if (students.length === 0) {
    return (
      <div className="card" data-testid="grade-entry-empty">
        <p>No submissions yet for <strong>{labTitle}</strong>.</p>
      </div>
    );
  }

  return (
    <div className="grade-entry" data-testid="grade-entry">
      <h2 className="grade-entry__title">Grade: {labTitle}</h2>
      <table className="grade-entry__table">
        <thead>
          <tr>
            <th>Student</th>
            <th>Submitted</th>
            <th>Answers</th>
            <th>Score (0–100)</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => {
            const state = gradeStates[student.studentId] ?? 'idle';
            return (
              <tr key={student.studentId}>
                <td>{student.studentName || student.studentId}</td>
                <td>{student.submittedAt ? new Date(student.submittedAt).toLocaleDateString() : '—'}</td>
                <td>
                  <details>
                    <summary>{Object.keys(student.answers).length} answer(s)</summary>
                    <ul className="grade-entry__answers">
                      {Object.entries(student.answers).map(([stepId, answer]) => (
                        <li key={stepId}>
                          <strong>{stepId}:</strong> {answer}
                        </li>
                      ))}
                    </ul>
                  </details>
                </td>
                <td>
                  <input
                    className="input"
                    type="number"
                    min={0}
                    max={100}
                    value={scores[student.studentId] ?? ''}
                    onChange={(e) =>
                      setScores((prev) => ({ ...prev, [student.studentId]: e.target.value }))
                    }
                    disabled={state === 'saving' || state === 'saved'}
                    aria-label={`Score for ${student.studentName || student.studentId}`}
                  />
                </td>
                <td>
                  {state === 'saved' ? (
                    <span className="badge badge--success">✓ Saved</span>
                  ) : (
                    <button
                      className="quiz-btn quiz-btn--primary"
                      type="button"
                      onClick={() => handleGrade(student.studentId)}
                      disabled={state === 'saving'}
                    >
                      {state === 'saving' ? 'Saving…' : 'Save grade'}
                    </button>
                  )}
                  {state === 'error' && (
                    <span className="callout callout--warn u-mt-1">
                      Invalid score or save failed.
                    </span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
