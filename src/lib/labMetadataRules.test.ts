import test from 'node:test';
import assert from 'node:assert/strict';

import { compareValidationIssues, validateLabMetadata, type ValidationIssue } from './labMetadataRules.ts';

test('missing tier -> LAB_MISSING_TIER', () => {
  const issues = validateLabMetadata('terminal-basics', { engine: 'steps' });
  assert.equal(issues.length, 1);
  assert.equal(issues[0]?.code, 'LAB_MISSING_TIER');
  assert.equal(
    issues[0]?.message,
    '[LAB_MISSING_TIER] Lab "terminal-basics" is missing required field "tier".\n' +
      'Allowed values: guided | state-machine | sandbox.\n' +
      'Action: Add `tier` to src/content/labs/terminal-basics.mdx frontmatter.'
  );
});

test('invalid tier -> LAB_INVALID_TIER', () => {
  const issues = validateLabMetadata('terminal-basics', { tier: 'sandboxed', engine: 'steps' });
  assert.equal(issues.length, 1);
  assert.equal(issues[0]?.code, 'LAB_INVALID_TIER');
  assert.equal(
    issues[0]?.message,
    '[LAB_INVALID_TIER] Lab "terminal-basics" has invalid tier "sandboxed".\n' +
      'Allowed values: guided | state-machine | sandbox.\n' +
      'Action: Correct `tier` in frontmatter.'
  );
});

test('missing engine -> LAB_MISSING_ENGINE', () => {
  const issues = validateLabMetadata('terminal-basics', { tier: 'guided' });
  assert.equal(issues.length, 1);
  assert.equal(issues[0]?.code, 'LAB_MISSING_ENGINE');
  assert.equal(
    issues[0]?.message,
    '[LAB_MISSING_ENGINE] Lab "terminal-basics" is missing required field "engine".\n' +
      'Allowed values: sim-sandbox-terminal | steps.\n' +
      'Action: Add `engine` to src/content/labs/terminal-basics.mdx frontmatter.'
  );
});

test('invalid engine -> LAB_INVALID_ENGINE', () => {
  const issues = validateLabMetadata('terminal-basics', { tier: 'guided', engine: 'sim-fsm' });
  assert.equal(issues.length, 1);
  assert.equal(issues[0]?.code, 'LAB_INVALID_ENGINE');
  assert.equal(
    issues[0]?.message,
    '[LAB_INVALID_ENGINE] Lab "terminal-basics" declares engine "sim-fsm" which is not currently supported.\n' +
      'Allowed values: sim-sandbox-terminal | steps.\n' +
      'Action: Use a shipped engine or implement and register the new engine before declaring it.'
  );
});

test('mismatch engine=steps tier=sandbox -> LAB_ENGINE_TIER_MISMATCH', () => {
  const issues = validateLabMetadata('terminal-basics', { tier: 'sandbox', engine: 'steps' });
  assert.equal(issues.length, 1);
  assert.equal(issues[0]?.code, 'LAB_ENGINE_TIER_MISMATCH');
  assert.equal(
    issues[0]?.message,
    '[LAB_ENGINE_TIER_MISMATCH] Lab "terminal-basics" declares engine "steps" but tier "sandbox".\n' +
      'Rule: engine "steps" requires tier "guided".\n' +
      'Action: Either change tier to "guided" or implement and register a matching engine.'
  );
});

test('sim-sandbox-terminal engine is valid when shipped=true', () => {
  const issues = validateLabMetadata('terminal-sandbox-basics', {
    tier: 'sandbox',
    engine: 'sim-sandbox-terminal',
  });
  assert.deepEqual(issues, []);
});

test('valid engine=steps tier=guided -> no issues', () => {
  const issues = validateLabMetadata('terminal-basics', { tier: 'guided', engine: 'steps' });
  assert.deepEqual(issues, []);
});

test('deterministic issue ordering comparator', () => {
  const issues: ValidationIssue[] = [
    {
      slug: 'z-lab',
      code: 'LAB_INVALID_ENGINE',
      message: 'm1',
    },
    {
      slug: 'a-lab',
      code: 'LAB_ENGINE_TIER_MISMATCH',
      message: 'm2',
    },
    {
      slug: 'a-lab',
      code: 'LAB_MISSING_ENGINE',
      message: 'm3',
    },
    {
      slug: 'a-lab',
      code: 'LAB_INVALID_TIER',
      message: 'm4',
    },
    {
      slug: 'a-lab',
      code: 'LAB_MISSING_TIER',
      message: 'm5',
    },
  ];

  const sorted = [...issues].sort(compareValidationIssues);
  assert.deepEqual(
    sorted.map((issue) => `${issue.slug}:${issue.code}`),
    [
      'a-lab:LAB_MISSING_TIER',
      'a-lab:LAB_MISSING_ENGINE',
      'a-lab:LAB_INVALID_TIER',
      'a-lab:LAB_ENGINE_TIER_MISMATCH',
      'z-lab:LAB_INVALID_ENGINE',
    ]
  );
});
