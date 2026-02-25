import { cloneFsNode, getNodeAtPath, normalizeAbsolutePath } from './fs';
import type { ObjectiveCheck, ObjectiveSpec, TerminalSpecV1, TerminalStateV1 } from './types';

const checkObjective = (state: TerminalStateV1, objective: ObjectiveSpec): ObjectiveCheck => {
  if (objective.kind === 'cwd') {
    const expected = normalizeAbsolutePath(objective.pass.path);
    const actual = normalizeAbsolutePath(state.cwd);
    const pass = actual === expected;
    return {
      id: objective.id,
      label: objective.label,
      pass,
      message: pass ? undefined : `Expected cwd ${expected} but found ${actual}`,
    };
  }

  if (objective.kind === 'fs') {
    if (objective.pass.type === 'pathExists') {
      const node = getNodeAtPath(state.fs, objective.pass.path);
      const pass = Boolean(node && node.type === objective.pass.nodeType);
      return {
        id: objective.id,
        label: objective.label,
        pass,
        message: pass ? undefined : `Expected ${objective.pass.nodeType} at ${normalizeAbsolutePath(objective.pass.path)}`,
      };
    }

    const node = getNodeAtPath(state.fs, objective.pass.path);
    const pass = Boolean(node && node.type === 'file' && node.content.includes(objective.pass.substring));
    return {
      id: objective.id,
      label: objective.label,
      pass,
      message: pass ? undefined : `Expected file ${normalizeAbsolutePath(objective.pass.path)} to contain substring`,
    };
  }

  if (objective.pass.type === 'historyIncludes') {
    const value = objective.pass.value;
    const pass = state.history.some((entry) => entry.cmd.includes(value));
    return {
      id: objective.id,
      label: objective.label,
      pass,
      message: pass ? undefined : `Expected command history to include ${value}`,
    };
  }

  let matcher: RegExp;
  try {
    matcher = new RegExp(objective.pass.pattern, objective.pass.flags);
  } catch {
    return {
      id: objective.id,
      label: objective.label,
      pass: false,
      message: 'Invalid history regex pattern',
    };
  }

  const pass = state.history.some((entry) => matcher.test(entry.cmd));
  return {
    id: objective.id,
    label: objective.label,
    pass,
    message: pass ? undefined : `Expected command history to match ${objective.pass.pattern}`,
  };
};

export const createInitialState = (spec: TerminalSpecV1): TerminalStateV1 => ({
  version: 1,
  cwd: normalizeAbsolutePath(spec.initialCwd),
  fs: cloneFsNode(spec.fs),
  history: [],
});

export const evaluateObjectives = (
  state: TerminalStateV1,
  spec: TerminalSpecV1
): { checks: ObjectiveCheck[]; progress: number } => {
  const checks = spec.objectives.map((objective) => checkObjective(state, objective));
  const total = checks.length;
  if (total === 0) {
    return {
      checks,
      progress: 0,
    };
  }

  const passed = checks.filter((check) => check.pass).length;
  return {
    checks,
    progress: Math.round((passed / total) * 100),
  };
};