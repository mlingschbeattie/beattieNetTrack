import assert from 'node:assert/strict';
import test from 'node:test';

import { referenceChecksPayloadForAction } from './referenceChecksEngine.ts';
import { coerceWorkspaceResultPayload } from './workspaceResultContract.ts';

const allowedTopLevelKeys = new Set([
  'slug',
  'action',
  'passed',
  'progress',
  'message',
  'difficulty',
  'estMinutes',
  'score',
  'checks',
]);

test('reference engine payloads pass canonical contract for run/check/submit/reset', () => {
  const slug = 'reference-checks';
  const actions = ['run', 'check', 'submit', 'reset'] as const;
  for (const action of actions) {
    const payload = referenceChecksPayloadForAction(slug, action);
    assert.deepEqual(coerceWorkspaceResultPayload(payload), payload);
  }
});

test('reference engine payloads emit no unknown top-level keys', () => {
  const slug = 'reference-checks';
  const actions = ['run', 'check', 'submit', 'reset'] as const;
  for (const action of actions) {
    const payload = referenceChecksPayloadForAction(slug, action);
    const keys = Object.keys(payload);
    for (const key of keys) {
      assert.equal(allowedTopLevelKeys.has(key), true);
    }
  }
});
