import { useMemo, useState } from 'react';
import {
  createInitialState,
  evaluateObjectives,
  execCommand,
  type ObjectiveCheck,
  type TerminalSpecV1,
  type TerminalStateV1,
} from '../lib/terminalSandbox';
import { getLabState, markLabCompleted, saveLabState } from '../lib/progressStore';

type TerminalSandboxRunnerProps = {
  labSlug: string;
  xpReward: number;
  spec: TerminalSpecV1;
};

type PersistedLabState = {
  startedAt: string | null;
  completedAt: string | null;
  completed: boolean;
  completedStepIds: string[];
  lastStepIndex: number;
  terminalState?: TerminalStateV1;
  terminalProgress?: {
    checks: ObjectiveCheck[];
    progress: number;
  };
};

const stableChecks = (checks: ObjectiveCheck[]): ObjectiveCheck[] =>
  checks.map((check) => ({
    id: check.id,
    label: check.label,
    pass: check.pass,
    message: check.message,
  }));

export default function TerminalSandboxRunner({ labSlug, xpReward, spec }: TerminalSandboxRunnerProps) {
  const initialFromStore = useMemo(() => {
    const stored = getLabState(labSlug) as PersistedLabState;
    const terminalState = stored.terminalState ?? createInitialState(spec);
    const evaluation = evaluateObjectives(terminalState, spec);

    return {
      startedAt: stored.startedAt ?? null,
      completedAt: stored.completedAt ?? null,
      terminalState,
      checks: stableChecks(stored.terminalProgress?.checks ?? evaluation.checks),
      progress:
        typeof stored.terminalProgress?.progress === 'number'
          ? stored.terminalProgress.progress
          : evaluation.progress,
      lastOutput: '',
      input: '',
    };
  }, [labSlug, spec]);

  const [terminalState, setTerminalState] = useState<TerminalStateV1>(initialFromStore.terminalState);
  const [checks, setChecks] = useState<ObjectiveCheck[]>(initialFromStore.checks);
  const [progress, setProgress] = useState<number>(initialFromStore.progress);
  const [startedAt, setStartedAt] = useState<string | null>(initialFromStore.startedAt);
  const [completedAt, setCompletedAt] = useState<string | null>(initialFromStore.completedAt);
  const [input, setInput] = useState(initialFromStore.input);
  const [lastOutput, setLastOutput] = useState(initialFromStore.lastOutput);

 const saveState = (
  nextState: TerminalStateV1,
  nextChecks: ObjectiveCheck[],
  nextProgress: number,
  completionAt: string | null,
  completedOverride?: boolean
) => {
  const effectiveStartedAt = startedAt ?? new Date().toISOString();
  if (!startedAt) {
    setStartedAt(effectiveStartedAt);
  }

  const completed = typeof completedOverride === 'boolean' ? completedOverride : Boolean(completionAt);

  saveLabState(labSlug, {
    startedAt: effectiveStartedAt,
    completedAt: completionAt,
    completed,
    terminalState: nextState,
    terminalProgress: {
      checks: nextChecks,
      progress: nextProgress,
    },
    completedStepIds: [],
    lastStepIndex: 0,
  } as Partial<PersistedLabState>);
};

  const emitWorkspaceResult = (
    action: 'submit' | 'reset',
    passed: boolean,
    nextProgress: number,
    message: string,
    nextChecks: ObjectiveCheck[]
  ) => {
    window.dispatchEvent(
      new CustomEvent('workspace:result', {
        detail: {
          slug: labSlug,
          action,
          passed,
          progress: nextProgress,
          message,
          checks: stableChecks(nextChecks),
        },
      })
    );
  };

  const runCommand = () => {
    const exec = execCommand(terminalState, spec, input);
    const evaluation = evaluateObjectives(exec.nextState, spec);
    const nextChecks = stableChecks(evaluation.checks);
    const nextProgress = evaluation.progress;

    setTerminalState(exec.nextState);
    setChecks(nextChecks);
    setProgress(nextProgress);
    setLastOutput(exec.output);

    let nextCompletedAt = completedAt;
    if (nextProgress === 100 && !completedAt) {
      const nowIso = new Date().toISOString();
      nextCompletedAt = nowIso;
      setCompletedAt(nowIso);
      markLabCompleted(labSlug, xpReward);
      window.dispatchEvent(new CustomEvent('progress-updated'));
    }

    saveState(exec.nextState, nextChecks, nextProgress, nextCompletedAt);

    // Deterministic passed rule: a submit passes if the command executed successfully.
    const passed = exec.ok;
    const message = exec.ok ? 'Command executed' : exec.output || 'Command failed';
    emitWorkspaceResult('submit', passed, nextProgress, message, nextChecks);
    setInput('');
  };

  const resetTerminal = () => {
  const persisted = getLabState(labSlug) as PersistedLabState;

  const persistedCompleted = Boolean(persisted.completed);
  const preservedCompletedAt = completedAt ?? persisted.completedAt ?? null;
  const shouldPreserveCompletion = persistedCompleted || Boolean(preservedCompletedAt);

  const resetState = createInitialState(spec);
  const evaluation = evaluateObjectives(resetState, spec);
  const nextChecks = stableChecks(evaluation.checks);
  const nextProgress = evaluation.progress;

  setTerminalState(resetState);
  setChecks(nextChecks);
  setProgress(nextProgress);
  setInput('');
  setLastOutput('');

  // IMPORTANT: do not revoke completion once earned
  setCompletedAt(shouldPreserveCompletion ? preservedCompletedAt : null);

  saveState(
    resetState,
    nextChecks,
    nextProgress,
    shouldPreserveCompletion ? preservedCompletedAt : null,
    shouldPreserveCompletion
  );

  emitWorkspaceResult(
    'reset',
    false,
    nextProgress,
    'Terminal reset',
    nextChecks.length > 0
      ? nextChecks
      : [{ id: 'terminal-reset', label: 'Terminal reset', pass: false, message: 'Terminal reset' }]
  );
};

  return (
    <article className="card" data-testid="terminal-sandbox-runner">
      <h3>Terminal Sandbox</h3>
      <div className="card__meta" style={{ marginBottom: '0.75rem' }}>
        <span className="badge">Progress {progress}%</span>
      </div>

      <div
        data-testid="terminal-output"
        style={{
          minHeight: '220px',
          maxHeight: '220px',
          overflowY: 'auto',
          border: '1px solid var(--line)',
          borderRadius: '12px',
          padding: '0.75rem',
          marginBottom: '0.75rem',
          background: 'var(--surface-2)',
          fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace',
          whiteSpace: 'pre-wrap',
        }}
      >
        {terminalState.history.length === 0 ? 'No commands yet.' : null}
        {terminalState.history.map((entry, index) => (
          <div key={`${index}:${entry.cmd}`}>
            <div>{spec.prompt}{entry.cmd}</div>
            <div>{entry.output}</div>
          </div>
        ))}
      </div>

      <label className="u-block u-mb-2" htmlFor="terminal-sandbox-input">Command</label>
      <input
        id="terminal-sandbox-input"
        className="input"
        data-testid="terminal-input"
        value={input}
        onChange={(event) => setInput(event.target.value)}
        placeholder="Type a command"
        onKeyDown={(event) => {
          if (event.key === 'Enter') {
            event.preventDefault();
            runCommand();
          }
        }}
      />

      <div className="card__footer u-mt-3">
        <button type="button" className="btn" data-testid="terminal-run" onClick={runCommand}>
          Run
        </button>
        <button type="button" className="btn-ghost" data-testid="terminal-reset" onClick={resetTerminal}>
          Reset
        </button>
      </div>

      <div data-testid="terminal-checks" className="u-mt-3">
        <h4>Objective checks</h4>
        <ul>
          {checks.map((check) => (
            <li key={check.id}>
              {check.pass ? '✔' : '✖'} {check.label}
              {check.message ? ` — ${check.message}` : ''}
            </li>
          ))}
        </ul>
      </div>

      {lastOutput ? <p className="u-mt-2"><strong>Latest output:</strong> {lastOutput}</p> : null}
      <p className="u-mt-2"><strong>Current directory:</strong> {terminalState.cwd}</p>
    </article>
  );
}