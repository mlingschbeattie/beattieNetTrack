import { useEffect, useMemo, useRef, useState } from 'react';
import { codeExercises } from '../../lib/codeExercises';

type CodeRunnerProps = {
  labSlug: string;
  exerciseSlug: string;
};

type ExecutionResult = {
  output: string;
  error: string | null;
};

const createRunnerWorker = () => {
  const workerSource = `
    self.onmessage = async (event) => {
      const { code } = event.data;
      const logs = [];
      const sandboxConsole = {
        log: (...args) => logs.push(args.map((arg) => String(arg)).join(' ')),
        error: (...args) => logs.push(args.map((arg) => String(arg)).join(' ')),
      };
      try {
        const fn = new Function('console', \"'use strict';\\n\" + code);
        fn(sandboxConsole);
        self.postMessage({ type: 'ok', output: logs.join('\\n') });
      } catch (error) {
        self.postMessage({ type: 'error', output: logs.join('\\n'), error: error instanceof Error ? error.message : String(error) });
      }
    };
  `;

  const blob = new Blob([workerSource], { type: 'text/javascript' });
  return new Worker(URL.createObjectURL(blob));
};

const storageKey = (slug: string) => `code-runner:${slug}`;

const runCode = (code: string, timeout = 1500): Promise<ExecutionResult> =>
  new Promise((resolve) => {
    const worker = createRunnerWorker();
    const timer = window.setTimeout(() => {
      worker.terminate();
      resolve({ output: '', error: 'Execution timed out' });
    }, timeout);

    worker.onmessage = (event) => {
      window.clearTimeout(timer);
      worker.terminate();
      if (event.data.type === 'error') {
        resolve({ output: event.data.output ?? '', error: event.data.error ?? 'Execution error' });
        return;
      }
      resolve({ output: event.data.output ?? '', error: null });
    };

    worker.postMessage({ code });
  });

export default function CodeRunner({ labSlug, exerciseSlug }: CodeRunnerProps) {
  const exercise = useMemo(
    () => codeExercises[exerciseSlug] ?? codeExercises['code-basics'],
    [exerciseSlug]
  );
  const [code, setCode] = useState(exercise.starterCode);
  const codeRef = useRef(exercise.starterCode);
  const [output, setOutput] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    codeRef.current = code;
  }, [code]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const cached = window.localStorage.getItem(storageKey(labSlug));
    if (!cached) return;
    setCode(cached);
    codeRef.current = cached;
  }, [labSlug]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    window.localStorage.setItem(storageKey(labSlug), code);
  }, [labSlug, code]);

  const run = async () => {
    const result = await runCode(codeRef.current);
    setOutput(result.output);
    setError(result.error);
    return result;
  };

  const check = async () => {
    const result = await run();
    const normalizedOutput = (result.output ?? '').trim();
    const passed = !result.error && normalizedOutput.includes(exercise.expectedOutput.trim());

    window.dispatchEvent(
      new CustomEvent('workspace:result', {
        detail: {
          slug: labSlug,
          action: 'check',
          passed,
          progress: passed ? 100 : 50,
          message: passed ? 'Code checks passed' : 'Expected output not found',
          difficulty: 'Beginner',
          estMinutes: 20,
          checks: [
            {
              id: 'code-output',
              label: 'Expected output detected',
              pass: passed,
              message: passed ? 'Output matched expectation' : 'Expected output not found in run output',
            },
          ],
        },
      })
    );
  };

  const submit = async () => {
    const result = await run();
    const normalizedOutput = (result.output ?? '').trim();
    const passed = !result.error && normalizedOutput.includes(exercise.expectedOutput.trim());

    window.dispatchEvent(
      new CustomEvent('workspace:result', {
        detail: {
          slug: labSlug,
          action: 'submit',
          passed,
          progress: passed ? 100 : 50,
          message: passed ? 'Exercise submitted successfully' : 'Submit failed checks',
          difficulty: 'Beginner',
          estMinutes: 20,
          checks: [
            {
              id: 'code-submit-output',
              label: 'Submission output validated',
              pass: passed,
              message: passed ? 'Submission output matched requirement' : 'Submission output missing expected value',
            },
          ],
        },
      })
    );
  };

  const reset = () => {
    setCode(exercise.starterCode);
    codeRef.current = exercise.starterCode;
    setOutput('');
    setError(null);
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(storageKey(labSlug));
    }
    window.dispatchEvent(
      new CustomEvent('workspace:result', {
        detail: {
          slug: labSlug,
          action: 'reset',
          passed: false,
          progress: 0,
          message: 'Code reset',
        },
      })
    );
  };

  useEffect(() => {
    const onAction = (event: Event) => {
      const customEvent = event as CustomEvent;
      const detail = customEvent.detail as { action?: string; slug?: string };
      if (!detail || detail.slug !== labSlug) return;

      if (detail.action === 'run') void run();
      if (detail.action === 'check') void check();
      if (detail.action === 'submit') void submit();
      if (detail.action === 'reset') reset();
    };

    const onKeydown = (event: KeyboardEvent) => {
      if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        void submit();
      }
    };

    window.addEventListener('workspace:action', onAction);
    window.addEventListener('keydown', onKeydown);
    return () => {
      window.removeEventListener('workspace:action', onAction);
      window.removeEventListener('keydown', onKeydown);
    };
  }, [labSlug, code]);

  return (
    <div className="code-runner" data-testid="code-runner">
      <div className="code-runner__header">
        <strong>{exercise.title}</strong>
        <div className="code-runner__controls">
          <button className="btn-secondary" type="button" onClick={() => void run()} data-testid="code-run">Run</button>
          <button className="btn-primary" type="button" onClick={() => void check()}>Check</button>
          <button className="btn-ghost" type="button" onClick={reset}>Reset</button>
        </div>
      </div>
      <textarea
        className="code-runner__editor"
        data-testid="code-editor"
        value={code}
        onChange={(event) => {
          codeRef.current = event.target.value;
          setCode(event.target.value);
        }}
        spellCheck={false}
        aria-label="Code editor"
      />
      <div className="code-runner__output" data-testid="code-output">
        <h4>Output</h4>
        <pre>{error ? `${output}\n${error}`.trim() : output || '(no output yet)'}</pre>
      </div>
    </div>
  );
}
