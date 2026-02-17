import test from 'node:test';
import assert from 'node:assert/strict';
import {
  getProgress,
  markLessonComplete,
  markLessonIncomplete,
  recordActivity,
  getTrackProgress,
  getLevel,
} from './progressStore';

const createMemoryStorage = () => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] ?? null,
    setItem: (key: string, value: string) => {
      store[key] = value;
    },
    reset: () => {
      store = {};
    },
  };
};

test('mark complete/incomplete updates XP', () => {
  const storage = createMemoryStorage();
  markLessonComplete('lesson-1', { difficulty: 'Beginner', estMinutes: 40 }, storage);
  let state = getProgress(storage);
  assert.equal(state.xpTotal, 15);

  markLessonComplete('lesson-1', { difficulty: 'Beginner', estMinutes: 40 }, storage);
  state = getProgress(storage);
  assert.equal(state.xpTotal, 15);

  markLessonIncomplete('lesson-1', storage);
  state = getProgress(storage);
  assert.equal(state.xpTotal, 0);
});

test('track progress aggregates XP and completion', () => {
  const storage = createMemoryStorage();
  markLessonComplete('a', { difficulty: 'Intermediate', estMinutes: 10 }, storage);
  markLessonComplete('b', { difficulty: 'Advanced', estMinutes: 70 }, storage);

  const progress = getTrackProgress(['a', 'b', 'c'], storage);
  assert.equal(progress.completed, 2);
  assert.equal(progress.total, 3);
  assert.ok(progress.xpEarned > 0);
});

test('streak increments across days', () => {
  const storage = createMemoryStorage();
  recordActivity(storage, new Date('2026-02-10T10:00:00Z'));
  recordActivity(storage, new Date('2026-02-11T10:00:00Z'));
  const state = getProgress(storage);
  assert.equal(state.streak.current, 2);
});

test('level derives from xpTotal', () => {
  assert.equal(getLevel(0), 1);
  assert.equal(getLevel(99), 1);
  assert.equal(getLevel(100), 2);
});
