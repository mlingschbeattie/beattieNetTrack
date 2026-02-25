export type FsDir = { type: 'dir'; children: Record<string, FsNode> };
export type FsFile = { type: 'file'; content: string };
export type FsNode = FsDir | FsFile;

export type ObjectiveSpec =
  | {
      id: string;
      label: string;
      kind: 'fs';
      pass:
        | { type: 'pathExists'; path: string; nodeType: 'dir' | 'file' }
        | { type: 'fileContains'; path: string; substring: string };
    }
  | {
      id: string;
      label: string;
      kind: 'cwd';
      pass: { type: 'cwdIs'; path: string };
    }
  | {
      id: string;
      label: string;
      kind: 'history';
      pass:
        | { type: 'historyIncludes'; value: string }
        | { type: 'historyMatches'; pattern: string; flags?: string };
    };

export type TerminalSpecV1 = {
  version: 1;
  prompt: string;
  initialCwd: string;
  fs: FsNode;
  allowedCommands: string[];
  objectives: ObjectiveSpec[];
};

export type TerminalHistoryEntry = { cmd: string; output: string; ok: boolean };

export type TerminalStateV1 = {
  version: 1;
  cwd: string;
  fs: FsNode;
  history: TerminalHistoryEntry[];
};

export type ExecResult = {
  nextState: TerminalStateV1;
  output: string;
  ok: boolean;
};

export type ObjectiveCheck = { id: string; label: string; pass: boolean; message?: string };

export const TERMINAL_HISTORY_LIMIT = 200;