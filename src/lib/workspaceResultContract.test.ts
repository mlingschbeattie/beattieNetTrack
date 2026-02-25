import assert from 'node:assert/strict';
import test from 'node:test';

import { coerceWorkspaceResultPayload, validateWorkspaceResultPayload } from './workspaceResultContract.ts';

const goodPayload = {
  slug: 'terminal-basics',
  action: 'submit',
  passed: true,
  progress: 100,
  message: 'Terminal checks passed',
  difficulty: 'Beginner',
  estMinutes: 20,
  score: 100,
  checks: [
    {
      id: 'terminal-expected',
      label: 'Required commands completed',
      pass: true,
      message: 'All required commands completed',
    },
  ],
} as const;

test('accepts known-good emitter payload with checks', () => {
  assert.equal(validateWorkspaceResultPayload(goodPayload), true);
  assert.deepEqual(coerceWorkspaceResultPayload(goodPayload), goodPayload);
});

test('rejects payload missing required key slug', () => {
  const payload = {
    action: 'check',
    passed: true,
    progress: 50,
  };
  assert.equal(validateWorkspaceResultPayload(payload), false);
  assert.equal(coerceWorkspaceResultPayload(payload), null);
});

test('rejects wrong required field types', () => {
  const payload = {
    slug: 'quiz-a',
    action: 'submit',
    passed: 'true',
    progress: '100',
  };
  assert.equal(validateWorkspaceResultPayload(payload), false);
});

test('rejects non-finite progress values', () => {
  const nanPayload = {
    slug: 'quiz-a',
    action: 'submit',
    passed: true,
    progress: Number.NaN,
  };
  const infPayload = {
    slug: 'quiz-a',
    action: 'submit',
    passed: true,
    progress: Number.POSITIVE_INFINITY,
  };
  assert.equal(validateWorkspaceResultPayload(nanPayload), false);
  assert.equal(validateWorkspaceResultPayload(infPayload), false);
});

test('rejects unknown extra field', () => {
  const payload = {
    slug: 'code-basics',
    action: 'check',
    passed: true,
    progress: 100,
    extra: true,
  };
  assert.equal(validateWorkspaceResultPayload(payload), false);
});

test('rejects timestamp-like field', () => {
  const payload = {
    slug: 'code-basics',
    action: 'check',
    passed: true,
    progress: 100,
    timestamp: 123,
  };
  assert.equal(validateWorkspaceResultPayload(payload), false);
});

test('accepts minimal docs payload', () => {
  const payload = {
    slug: 'pc-assembly',
    action: 'check',
    passed: true,
    progress: 100,
    message: 'OK',
  } as const;
  assert.equal(validateWorkspaceResultPayload(payload), true);
});

test('accepts valid run payload', () => {
  const payload = {
    slug: 'terminal-basics',
    action: 'run',
    passed: true,
    progress: 60,
    message: 'Terminal ready',
  } as const;
  assert.equal(validateWorkspaceResultPayload(payload), true);
});

test('rejects malformed checks item', () => {
  const payload = {
    slug: 'pc-assembly',
    action: 'submit',
    passed: false,
    progress: 40,
    checks: [
      {
        id: 'x',
        label: 'Broken check object',
        pass: 'nope',
      },
    ],
  };
  assert.equal(validateWorkspaceResultPayload(payload), false);
});

test('rejects checks item missing required key', () => {
  const payload = {
    slug: 'pc-assembly',
    action: 'submit',
    passed: true,
    progress: 95,
    checks: [
      {
        label: 'Missing id',
        pass: true,
      },
    ],
  };
  assert.equal(validateWorkspaceResultPayload(payload), false);
});

test('rejects malformed checks with unknown keys', () => {
  const payload = {
    slug: 'pc-assembly',
    action: 'submit',
    passed: true,
    progress: 90,
    checks: [
      {
        id: 'x',
        label: 'Known check',
        pass: true,
        unknown: 'value',
      },
    ],
  };
  assert.equal(validateWorkspaceResultPayload(payload), false);
});
