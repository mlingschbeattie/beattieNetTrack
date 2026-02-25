import assert from 'node:assert/strict';
import test from 'node:test';

import {
  createInitialState,
  evaluateObjectives,
  execCommand,
  type FsNode,
  type TerminalSpecV1,
} from './terminalSandbox';

const baseFs: FsNode = {
  type: 'dir',
  children: {
    home: {
      type: 'dir',
      children: {
        student: {
          type: 'dir',
          children: {
            'seed.txt': {
              type: 'file',
              content: 'hello from seed',
            },
          },
        },
      },
    },
  },
};

const makeSpec = (overrides: Partial<TerminalSpecV1> = {}): TerminalSpecV1 => ({
  version: 1,
  prompt: '$ ',
  initialCwd: '/home/student',
  fs: baseFs,
  allowedCommands: ['pwd', 'ls', 'cd', 'mkdir', 'touch', 'cat', 'echo'],
  objectives: [],
  ...overrides,
});

test('determinism: same initial state + same input => same output and nextState', () => {
  const spec = makeSpec();
  const stateA = createInitialState(spec);
  const stateB = createInitialState(spec);

  const resultA = execCommand(stateA, spec, 'mkdir a');
  const resultB = execCommand(stateB, spec, 'mkdir a');

  assert.deepEqual(resultA, resultB);
});

test('pwd returns initial cwd', () => {
  const spec = makeSpec();
  const state = createInitialState(spec);

  const result = execCommand(state, spec, 'pwd');
  assert.equal(result.ok, true);
  assert.equal(result.output, '/home/student');
});

test('mkdir + ls sorted lexicographically', () => {
  const spec = makeSpec();
  const state = createInitialState(spec);

  const r1 = execCommand(state, spec, 'mkdir b');
  const r2 = execCommand(r1.nextState, spec, 'mkdir a');
  const r3 = execCommand(r2.nextState, spec, 'ls');

  assert.equal(r3.ok, true);
  assert.equal(r3.output, 'a\nb\nseed.txt');
});

test('cd path normalization keeps canonical cwd', () => {
  const spec = makeSpec();
  const state = createInitialState(spec);
  const result = execCommand(state, spec, 'cd ../student');

  assert.equal(result.ok, true);
  assert.equal(result.nextState.cwd, '/home/student');
});

test('touch + cat semantics for empty and seeded files', () => {
  const spec = makeSpec();
  const state = createInitialState(spec);

  const touched = execCommand(state, spec, 'touch note.txt');
  const catNew = execCommand(touched.nextState, spec, 'cat note.txt');
  const catSeed = execCommand(touched.nextState, spec, 'cat seed.txt');

  assert.equal(catNew.ok, true);
  assert.equal(catNew.output, '');
  assert.equal(catSeed.ok, true);
  assert.equal(catSeed.output, 'hello from seed');
});

test('disallow command when excluded by allowedCommands', () => {
  const spec = makeSpec({
    allowedCommands: ['pwd', 'ls', 'cd', 'touch', 'cat', 'echo'],
  });
  const state = createInitialState(spec);

  const result = execCommand(state, spec, 'mkdir denied');
  assert.equal(result.ok, false);
  assert.equal(result.output, 'mkdir: command not allowed');
});

test('history objective: historyIncludes passes after pwd', () => {
  const spec = makeSpec({
    objectives: [
      {
        id: 'hist-1',
        label: 'Run pwd once',
        kind: 'history',
        pass: { type: 'historyIncludes', value: 'pwd' },
      },
    ],
  });

  const state = createInitialState(spec);
  const next = execCommand(state, spec, 'pwd').nextState;

  const evaluation = evaluateObjectives(next, spec);
  assert.equal(evaluation.checks.length, 1);
  assert.equal(evaluation.checks[0]?.pass, true);
  assert.equal(evaluation.progress, 100);
});