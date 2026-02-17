export type QuizSingleQuestion = {
  id: string;
  type: 'single';
  prompt: string;
  options: string[];
  correctIndex: number;
  explanation?: string;
};

export type QuizMultiQuestion = {
  id: string;
  type: 'multi';
  prompt: string;
  options: string[];
  correctIndices: number[];
  explanation?: string;
};

export type QuizShortQuestion = {
  id: string;
  type: 'short';
  prompt: string;
  acceptedAnswers: string[];
  explanation?: string;
};

export type QuizQuestion = QuizSingleQuestion | QuizMultiQuestion | QuizShortQuestion;

export type QuizDefinition = {
  slug: string;
  title: string;
  description?: string;
  passThreshold: number;
  questions: QuizQuestion[];
};

export type QuizAnswer =
  | { type: 'single'; selectedIndex: number | null }
  | { type: 'multi'; selectedIndices: number[] }
  | { type: 'short'; value: string };

export type QuizQuestionResult = {
  id: string;
  correct: boolean;
  feedback: string;
};

export type QuizGradeResult = {
  score: number;
  correctCount: number;
  total: number;
  passed: boolean;
  results: QuizQuestionResult[];
};

export const normalizeText = (value: string) =>
  value
    .toLowerCase()
    .trim()
    .replace(/\s+/g, ' ')
    .replace(/[.,!?;:]+$/g, '');

export const gradeQuiz = (
  quiz: QuizDefinition,
  answers: Record<string, QuizAnswer>
): QuizGradeResult => {
  const results = quiz.questions.map((question) => {
    const answer = answers[question.id];
    if (!answer) {
      return { id: question.id, correct: false, feedback: 'No answer provided.' };
    }

    if (question.type === 'single') {
      const selected = answer.type === 'single' ? answer.selectedIndex : null;
      const correct = selected === question.correctIndex;
      return {
        id: question.id,
        correct,
        feedback: correct
          ? 'Correct.'
          : question.explanation ?? `Correct answer: ${question.options[question.correctIndex]}`,
      };
    }

    if (question.type === 'multi') {
      const selected = answer.type === 'multi' ? [...answer.selectedIndices].sort((a, b) => a - b) : [];
      const expected = [...question.correctIndices].sort((a, b) => a - b);
      const correct = selected.length === expected.length && selected.every((value, index) => value === expected[index]);
      return {
        id: question.id,
        correct,
        feedback: correct
          ? 'Correct.'
          : question.explanation ?? 'Review all selected options and try again.',
      };
    }

    const value = answer.type === 'short' ? normalizeText(answer.value) : '';
    const accepted = question.acceptedAnswers.map((entry) => normalizeText(entry));
    const correct = accepted.includes(value);
    return {
      id: question.id,
      correct,
      feedback: correct ? 'Correct.' : question.explanation ?? `Accepted answers include: ${question.acceptedAnswers.join(', ')}`,
    };
  });

  const correctCount = results.filter((entry) => entry.correct).length;
  const total = quiz.questions.length;
  const score = total ? Math.round((correctCount / total) * 100) : 0;

  return {
    score,
    correctCount,
    total,
    passed: score >= quiz.passThreshold,
    results,
  };
};
