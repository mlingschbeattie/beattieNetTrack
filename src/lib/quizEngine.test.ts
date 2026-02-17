import test from 'node:test';
import assert from 'node:assert/strict';
import { gradeQuiz, normalizeText, type QuizDefinition } from './quizEngine';

const sampleQuiz: QuizDefinition = {
  slug: 'sample',
  title: 'Sample Quiz',
  passThreshold: 70,
  questions: [
    {
      id: 'q1',
      type: 'single',
      prompt: 'OSI layer for IP?',
      options: ['Application', 'Transport', 'Network', 'Physical'],
      correctIndex: 2,
    },
    {
      id: 'q2',
      type: 'multi',
      prompt: 'Select private ranges',
      options: ['10.0.0.0/8', '8.8.8.8', '192.168.0.0/16'],
      correctIndices: [0, 2],
    },
    {
      id: 'q3',
      type: 'short',
      prompt: 'Command to show route table on Windows?',
      acceptedAnswers: ['route print', 'route    print'],
    },
  ],
};

test('normalizeText normalizes punctuation and spacing', () => {
  assert.equal(normalizeText(' Route   Print! '), 'route print');
});

test('gradeQuiz grades all supported question types', () => {
  const grade = gradeQuiz(sampleQuiz, {
    q1: { type: 'single', selectedIndex: 2 },
    q2: { type: 'multi', selectedIndices: [2, 0] },
    q3: { type: 'short', value: '  Route Print  ' },
  });

  assert.equal(grade.correctCount, 3);
  assert.equal(grade.score, 100);
  assert.equal(grade.passed, true);
});
