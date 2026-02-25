import { useMemo, useState } from 'react';
import { referenceChecksPayloadForAction } from '../lib/referenceChecksEngine.ts';

type ReferenceChecksRunnerProps = {
  labSlug: string;
};

export default function ReferenceChecksRunner({ labSlug }: ReferenceChecksRunnerProps) {
  const [lastMessage, setLastMessage] = useState<string>('No action yet.');

  const actions = useMemo(() => ['run', 'check', 'submit', 'reset'] as const, []);

  const emit = (action: (typeof actions)[number]) => {
    const payload = referenceChecksPayloadForAction(labSlug, action);
    window.dispatchEvent(new CustomEvent('workspace:result', { detail: payload }));
    setLastMessage(payload.message ?? 'Done');
  };

  return (
    <article className="card" data-testid="reference-checks-runner">
      <h3>Reference Checks Simulator</h3>
      <p>Deterministic harness for workspace result contract regression checks.</p>
      <div className="card__footer" style={{ gap: '0.5rem', flexWrap: 'wrap' }}>
        <button type="button" className="btn" onClick={() => emit('run')} data-testid="reference-run">
          Run
        </button>
        <button type="button" className="btn" onClick={() => emit('check')} data-testid="reference-check">
          Check
        </button>
        <button type="button" className="btn" onClick={() => emit('submit')} data-testid="reference-submit">
          Submit
        </button>
        <button type="button" className="btn-ghost" onClick={() => emit('reset')} data-testid="reference-reset">
          Reset
        </button>
      </div>
      <p className="u-mt-2" data-testid="reference-last-message">
        <strong>Last:</strong> {lastMessage}
      </p>
    </article>
  );
}
