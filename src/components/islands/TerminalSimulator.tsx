import { useEffect, useMemo, useRef, useState } from 'react';
import { terminalScenarios, type TerminalNode, type TerminalScenario } from '../../lib/terminalScenarios';

type TerminalSimulatorProps = {
  labSlug: string;
  scenarioSlug: string;
};

type TerminalState = {
  cwd: string;
  history: string[];
  commandHistory: string[];
  completedExpected: string[];
};

type CheckResult = {
  passed: boolean;
  progress: number;
  message: string;
  feedback: string[];
};

const normalizePath = (rawPath: string) => {
  const sanitized = rawPath.replace(/\\/g, '/').trim();
  const parts = sanitized.split('/').filter(Boolean);
  return `/${parts.join('/')}`;
};

const resolvePath = (cwd: string, inputPath: string) => {
  const base = inputPath.startsWith('/') ? [] : cwd.split('/').filter(Boolean);
  inputPath
    .split('/')
    .filter(Boolean)
    .forEach((segment) => {
      if (segment === '.') return;
      if (segment === '..') {
        base.pop();
        return;
      }
      base.push(segment);
    });
  return `/${base.join('/')}`;
};

const findNode = (tree: TerminalNode[], absolutePath: string): TerminalNode | null => {
  const segments = absolutePath.split('/').filter(Boolean);
  let nodes = tree;
  let current: TerminalNode | null = { type: 'dir', name: '/', children: tree };

  for (const segment of segments) {
    const next = nodes.find((node) => node.name === segment);
    if (!next) return null;
    current = next;
    nodes = next.children ?? [];
  }

  return current;
};

const getDefaultState = (scenario: TerminalScenario): TerminalState => ({
  cwd: normalizePath(scenario.startPath),
  history: [`${scenario.user}@lab:${normalizePath(scenario.startPath)}$`],
  commandHistory: [],
  completedExpected: [],
});

const storageKey = (slug: string) => `terminal-state:${slug}`;

const readState = (slug: string, scenario: TerminalScenario) => {
  if (typeof window === 'undefined') return getDefaultState(scenario);
  try {
    const raw = window.localStorage.getItem(storageKey(slug));
    if (!raw) return getDefaultState(scenario);
    const parsed = JSON.parse(raw) as TerminalState;
    if (!parsed || typeof parsed !== 'object') return getDefaultState(scenario);
    return {
      cwd: typeof parsed.cwd === 'string' ? parsed.cwd : normalizePath(scenario.startPath),
      history: Array.isArray(parsed.history) ? parsed.history : [],
      commandHistory: Array.isArray(parsed.commandHistory) ? parsed.commandHistory : [],
      completedExpected: Array.isArray(parsed.completedExpected) ? parsed.completedExpected : [],
    };
  } catch {
    return getDefaultState(scenario);
  }
};

const saveState = (slug: string, state: TerminalState) => {
  if (typeof window === 'undefined') return;
  window.localStorage.setItem(storageKey(slug), JSON.stringify(state));
};

export default function TerminalSimulator({ labSlug, scenarioSlug }: TerminalSimulatorProps) {
  const scenario = useMemo(() => terminalScenarios[scenarioSlug] ?? terminalScenarios['terminal-basics'], [scenarioSlug]);
  const [state, setState] = useState<TerminalState>(() => getDefaultState(scenario));
  const [command, setCommand] = useState('');
  const outputRef = useRef<HTMLDivElement>(null);
  const historyCursorRef = useRef(-1);

  const appendLines = (lines: string[], next?: Partial<TerminalState>) => {
    setState((prev) => {
      const updated: TerminalState = {
        ...prev,
        ...next,
        history: [...prev.history, ...lines],
      };
      saveState(labSlug, updated);
      return updated;
    });
  };

  const runCommand = (raw: string) => {
    const trimmed = raw.trim();
    if (!trimmed) return;

    const prompt = `${scenario.user}@lab:${state.cwd}$ ${trimmed}`;
    const tokens = trimmed.split(/\s+/);
    const base = tokens[0]?.toLowerCase();
    const args = tokens.slice(1);

    const commandHistory = [...state.commandHistory, trimmed];
    const nextCompleted = new Set(state.completedExpected);
    scenario.expectations.forEach((expectation) => {
      if (expectation.command.toLowerCase() === trimmed.toLowerCase()) {
        nextCompleted.add(expectation.command.toLowerCase());
      }
    });

    if (base === 'help') {
      appendLines([prompt, 'Commands: help, clear, ls, cd, cat, pwd, whoami, echo, mkdir, touch'], {
        commandHistory,
        completedExpected: Array.from(nextCompleted),
      });
      return;
    }

    if (base === 'clear') {
      const updated: TerminalState = {
        ...state,
        history: [],
        commandHistory,
        completedExpected: Array.from(nextCompleted),
      };
      saveState(labSlug, updated);
      setState(updated);
      return;
    }

    if (base === 'pwd') {
      appendLines([prompt, state.cwd], { commandHistory, completedExpected: Array.from(nextCompleted) });
      return;
    }

    if (base === 'whoami') {
      appendLines([prompt, scenario.user], { commandHistory, completedExpected: Array.from(nextCompleted) });
      return;
    }

    if (base === 'echo') {
      appendLines([prompt, args.join(' ')], { commandHistory, completedExpected: Array.from(nextCompleted) });
      return;
    }

    if (base === 'ls') {
      const target = args[0] ? resolvePath(state.cwd, args[0]) : state.cwd;
      const node = findNode(scenario.tree, target);
      if (!node || node.type !== 'dir') {
        appendLines([prompt, `ls: cannot access '${args[0] ?? target}': No such directory`], {
          commandHistory,
          completedExpected: Array.from(nextCompleted),
        });
        return;
      }
      const names = (node.children ?? []).map((child) => child.name).join('  ') || '(empty)';
      appendLines([prompt, names], { commandHistory, completedExpected: Array.from(nextCompleted) });
      return;
    }

    if (base === 'cd') {
      const target = args[0] ? resolvePath(state.cwd, args[0]) : '/';
      const node = findNode(scenario.tree, target);
      if (!node || node.type !== 'dir') {
        appendLines([prompt, `cd: no such file or directory: ${args[0] ?? target}`], {
          commandHistory,
          completedExpected: Array.from(nextCompleted),
        });
        return;
      }
      appendLines([prompt], {
        commandHistory,
        cwd: target,
        completedExpected: Array.from(nextCompleted),
      });
      return;
    }

    if (base === 'cat') {
      const targetArg = args[0];
      if (!targetArg) {
        appendLines([prompt, 'cat: missing file argument'], {
          commandHistory,
          completedExpected: Array.from(nextCompleted),
        });
        return;
      }
      const target = resolvePath(state.cwd, targetArg);
      const node = findNode(scenario.tree, target);
      if (!node || node.type !== 'file') {
        appendLines([prompt, `cat: ${targetArg}: No such file`], {
          commandHistory,
          completedExpected: Array.from(nextCompleted),
        });
        return;
      }
      appendLines([prompt, node.content ?? ''], { commandHistory, completedExpected: Array.from(nextCompleted) });
      return;
    }

    if (base === 'mkdir' || base === 'touch') {
      appendLines([prompt, `${base}: simulated only in this lab`], {
        commandHistory,
        completedExpected: Array.from(nextCompleted),
      });
      return;
    }

    appendLines([prompt, `${base}: command not found`], {
      commandHistory,
      completedExpected: Array.from(nextCompleted),
    });
  };

  const resetTerminal = () => {
    const next = getDefaultState(scenario);
    setState(next);
    setCommand('');
    historyCursorRef.current = -1;
    saveState(labSlug, next);
  };

  const checkTerminal = (): CheckResult => {
    const expected = scenario.expectations.map((entry) => entry.command.toLowerCase());
    const completed = new Set(state.completedExpected);
    const matched = expected.filter((commandKey) => completed.has(commandKey));
    const progress = expected.length ? Math.round((matched.length / expected.length) * 100) : 100;
    const missing = scenario.expectations
      .filter((entry) => !completed.has(entry.command.toLowerCase()))
      .map((entry) => entry.feedback);
    return {
      passed: missing.length === 0,
      progress,
      message: missing.length === 0 ? 'Terminal checks passed' : 'Missing required commands',
      feedback: missing,
    };
  };

  useEffect(() => {
    const persisted = readState(labSlug, scenario);
    setState(persisted);
  }, [labSlug, scenario]);

  useEffect(() => {
    outputRef.current?.scrollTo({ top: outputRef.current.scrollHeight, behavior: 'auto' });
  }, [state.history]);

  useEffect(() => {
    const onAction = (event: Event) => {
      const customEvent = event as CustomEvent;
      const detail = customEvent.detail as { action?: string; slug?: string };
      if (!detail || detail.slug !== labSlug) return;

      if (detail.action === 'reset') {
        resetTerminal();
        window.dispatchEvent(
          new CustomEvent('workspace:result', {
            detail: { slug: labSlug, action: 'reset', passed: true, progress: 0, message: 'Terminal reset' },
          })
        );
        return;
      }

      if (detail.action === 'check' || detail.action === 'submit') {
        const result = checkTerminal();
        window.dispatchEvent(
          new CustomEvent('workspace:result', {
            detail: {
              slug: labSlug,
              action: detail.action,
              passed: result.passed,
              progress: result.progress,
              message: result.passed ? result.message : `${result.message}: ${result.feedback.join(' | ')}`,
              difficulty: 'Beginner',
              estMinutes: 20,
              checks: [
                {
                  id: 'terminal-expected',
                  label: 'Required commands completed',
                  pass: result.passed,
                  message: result.feedback.join(' | '),
                },
              ],
            },
          })
        );
        return;
      }

      if (detail.action === 'run') {
        window.dispatchEvent(
          new CustomEvent('workspace:result', {
            detail: {
              slug: labSlug,
              action: 'run',
              passed: true,
              progress: checkTerminal().progress,
              message: 'Terminal ready',
            },
          })
        );
      }
    };

    window.addEventListener('workspace:action', onAction);
    return () => window.removeEventListener('workspace:action', onAction);
  }, [labSlug, state]);

  const lineKind = (line: string): string => {
    if (line.includes('@lab:') && line.includes('$')) return 'cmd';
    if (
      line.includes('command not found') ||
      line.includes('No such') ||
      line.includes('cannot access') ||
      line.includes('missing file argument')
    ) return 'error';
    return '';
  };

  return (
    <div className="terminal-window" data-testid="terminal-simulator">
      <div className="terminal-titlebar">
        <div className="terminal-titlebar__dots">
          <span className="terminal-titlebar__dot terminal-titlebar__dot--red" />
          <span className="terminal-titlebar__dot terminal-titlebar__dot--yellow" />
          <span className="terminal-titlebar__dot terminal-titlebar__dot--green" />
        </div>
        <span className="terminal-titlebar__label">{scenario.user}@beattie-lab:~</span>
      </div>
      <div className="terminal-body" ref={outputRef} data-testid="terminal-output">
        <div className="terminal-output">
          {state.history.map((line, index) => {
            const kind = lineKind(line);
            return (
              <span
                key={`${line}-${index}`}
                className={`terminal-output__line${kind ? ` terminal-output__line--${kind}` : ''}`}
              >
                {line || '\u00a0'}
              </span>
            );
          })}
        </div>
        <div className="terminal-input-row">
          <span className="terminal-prompt">{scenario.user}@lab:{state.cwd}$</span>
          <input
            id={`terminal-input-${labSlug}`}
            aria-label="Terminal command input"
            className="terminal-input"
            value={command}
            onChange={(event) => setCommand(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                runCommand(command);
                setCommand('');
                historyCursorRef.current = -1;
              }
              if (event.key === 'ArrowUp') {
                event.preventDefault();
                const prev = historyCursorRef.current;
                const next = prev < 0 ? state.commandHistory.length - 1 : Math.max(0, prev - 1);
                historyCursorRef.current = next;
                setCommand(state.commandHistory[next] ?? '');
              }
              if (event.key === 'ArrowDown') {
                event.preventDefault();
                const prev = historyCursorRef.current;
                if (prev < 0) return;
                const next = Math.min(state.commandHistory.length - 1, prev + 1);
                historyCursorRef.current = next;
                setCommand(state.commandHistory[next] ?? '');
              }
            }}
            placeholder="Type a command"
            data-testid="terminal-input"
          />
          <button
            className="btn-primary"
            type="button"
            onClick={() => {
              runCommand(command);
              setCommand('');
              historyCursorRef.current = -1;
            }}
            data-testid="terminal-run"
          >
            Enter
          </button>
        </div>
      </div>
    </div>
  );
}
