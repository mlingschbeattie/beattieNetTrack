import {
  asDir,
  basename,
  getNodeAtPath,
  listDirEntries,
  mkdirAtPath,
  normalizeAbsolutePath,
  resolvePath,
  tokenize,
  touchAtPath,
} from './fs';
import type { ExecResult, TerminalHistoryEntry, TerminalSpecV1, TerminalStateV1 } from './types';
import { TERMINAL_HISTORY_LIMIT } from './types';

const withHistory = (state: TerminalStateV1, entry: TerminalHistoryEntry): TerminalStateV1 => {
  const history = [...state.history, entry];
  const boundedHistory = history.slice(-TERMINAL_HISTORY_LIMIT);
  return {
    ...state,
    history: boundedHistory,
  };
};

const resultWithHistory = (
  state: TerminalStateV1,
  cmd: string,
  output: string,
  ok: boolean,
  next?: Partial<TerminalStateV1>
): ExecResult => {
  const nextState = withHistory(
    {
      ...state,
      ...next,
    },
    { cmd, output, ok }
  );

  return {
    nextState,
    output,
    ok,
  };
};

export const execCommand = (state: TerminalStateV1, spec: TerminalSpecV1, input: string): ExecResult => {
  const trimmedInput = input.trim();
  if (trimmedInput.length === 0) {
    return {
      nextState: state,
      output: '',
      ok: true,
    };
  }

  const tokens = tokenize(input);
  const cmd = tokens[0] ?? '';
  const args = tokens.slice(1);

  if (!spec.allowedCommands.includes(cmd)) {
    return resultWithHistory(state, trimmedInput, `${cmd}: command not allowed`, false);
  }

  if (cmd === 'pwd') {
    return resultWithHistory(state, trimmedInput, state.cwd, true);
  }

  if (cmd === 'ls') {
    const pathArg = args[0] ?? state.cwd;
    const targetPath = resolvePath(state.cwd, pathArg);
    const node = getNodeAtPath(state.fs, targetPath);

    if (!node) {
      return resultWithHistory(state, trimmedInput, `ls: cannot access '${pathArg}': No such file or directory`, false);
    }

    if (node.type === 'file') {
      return resultWithHistory(state, trimmedInput, basename(targetPath), true);
    }

    return resultWithHistory(state, trimmedInput, listDirEntries(node).join('\n'), true);
  }

  if (cmd === 'cd') {
    const pathArg = args[0];
    if (!pathArg) {
      return resultWithHistory(state, trimmedInput, 'cd: missing operand', false);
    }

    const targetPath = resolvePath(state.cwd, pathArg);
    const node = getNodeAtPath(state.fs, targetPath);

    if (!node) {
      return resultWithHistory(state, trimmedInput, `cd: ${pathArg}: No such file or directory`, false);
    }

    if (node.type !== 'dir') {
      return resultWithHistory(state, trimmedInput, `cd: ${pathArg}: Not a directory`, false);
    }

    return resultWithHistory(state, trimmedInput, '', true, { cwd: normalizeAbsolutePath(targetPath) });
  }

  if (cmd === 'mkdir') {
    const name = args[0];
    if (!name) {
      return resultWithHistory(state, trimmedInput, 'mkdir: missing operand', false);
    }

    const targetPath = resolvePath(state.cwd, name);
    const parentPath = resolvePath(targetPath, '..');
    if (!asDir(getNodeAtPath(state.fs, parentPath))) {
      return resultWithHistory(state, trimmedInput, `mkdir: cannot create directory '${name}': No such file or directory`, false);
    }

    const mkdirResult = mkdirAtPath(state.fs, targetPath);
    if (mkdirResult.exists) {
      return resultWithHistory(state, trimmedInput, `mkdir: cannot create directory '${name}': File exists`, false);
    }

    if (!mkdirResult.created) {
      return resultWithHistory(state, trimmedInput, `mkdir: cannot create directory '${name}': No such file or directory`, false);
    }

    return resultWithHistory(state, trimmedInput, '', true, { fs: mkdirResult.fs });
  }

  if (cmd === 'touch') {
    const name = args[0];
    if (!name) {
      return resultWithHistory(state, trimmedInput, 'touch: missing file operand', false);
    }

    const targetPath = resolvePath(state.cwd, name);
    const parentPath = resolvePath(targetPath, '..');
    if (!asDir(getNodeAtPath(state.fs, parentPath))) {
      return resultWithHistory(state, trimmedInput, `touch: ${name}: No such file or directory`, false);
    }

    const touchResult = touchAtPath(state.fs, targetPath);
    if (!touchResult.ok) {
      return resultWithHistory(state, trimmedInput, `touch: ${name}: No such file or directory`, false);
    }

    return resultWithHistory(state, trimmedInput, '', true, { fs: touchResult.fs });
  }

  if (cmd === 'cat') {
    const name = args[0];
    if (!name) {
      return resultWithHistory(state, trimmedInput, 'cat: missing file operand', false);
    }

    const targetPath = resolvePath(state.cwd, name);
    const node = getNodeAtPath(state.fs, targetPath);

    if (!node) {
      return resultWithHistory(state, trimmedInput, `cat: ${name}: No such file or directory`, false);
    }

    if (node.type === 'dir') {
      return resultWithHistory(state, trimmedInput, `cat: ${name}: Is a directory`, false);
    }

    return resultWithHistory(state, trimmedInput, node.content, true);
  }

  if (cmd === 'echo') {
    return resultWithHistory(state, trimmedInput, args.join(' '), true);
  }

  return resultWithHistory(state, trimmedInput, `${cmd}: command not found`, false);
};