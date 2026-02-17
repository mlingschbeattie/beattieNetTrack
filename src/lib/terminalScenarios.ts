export type TerminalNode = {
  type: 'file' | 'dir';
  name: string;
  content?: string;
  children?: TerminalNode[];
};

export type TerminalExpectation = {
  command: string;
  feedback: string;
};

export type TerminalScenario = {
  title: string;
  user: string;
  startPath: string;
  tree: TerminalNode[];
  expectations: TerminalExpectation[];
};

const terminalBasics: TerminalScenario = {
  title: 'Terminal Basics',
  user: 'student',
  startPath: '/home/student',
  tree: [
    {
      type: 'dir',
      name: 'home',
      children: [
        {
          type: 'dir',
          name: 'student',
          children: [
            { type: 'file', name: 'README.txt', content: 'Welcome to the lab environment.' },
            {
              type: 'dir',
              name: 'projects',
              children: [{ type: 'file', name: 'notes.txt', content: 'Network diagnostics notes.' }],
            },
          ],
        },
      ],
    },
  ],
  expectations: [
    { command: 'pwd', feedback: 'Show your current working directory.' },
    { command: 'ls', feedback: 'List files in the current directory.' },
    { command: 'cat README.txt', feedback: 'Read the introductory file.' },
  ],
};

export const terminalScenarios: Record<string, TerminalScenario> = {
  'terminal-basics': terminalBasics,
  'tour-terminal-challenge': {
    ...terminalBasics,
    title: 'Tour Terminal Challenge',
    expectations: [
      { command: 'help', feedback: 'Open available command list.' },
      { command: 'pwd', feedback: 'Show your current directory.' },
    ],
  },
};
