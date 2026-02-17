import { useEffect, useMemo, useState } from 'react';
import {
  clearAllChecks,
  getLastResult,
  getRequirementChecklist,
  setRequirementChecklist,
  subscribeChecks,
  type LastCheckResult,
  type RequirementItem,
} from '../../lib/checksStore';
import {
  getPanelState,
  setPanelState,
  subscribePanel,
  type RightPanelTab,
} from '../../lib/panelStore';

type Props = {
  routePath: string;
  hints?: string[];
  checklist?: string[];
};

const parseContext = (path: string) => {
  const segments = path.split('/').filter(Boolean);
  if (!segments.length) return {};

  if (segments[0] === 'workspace') {
    return { itemType: segments[1], itemSlug: segments[2] };
  }

  if (segments[0] === 'labs') {
    return { itemType: 'lab', itemSlug: segments[1] };
  }

  if (segments[0] === 'quizzes') {
    return { itemType: 'quiz', itemSlug: segments[1] };
  }

  if (segments[0] === 'tour') {
    return { itemType: 'tour', itemSlug: segments[1] };
  }

  return {};
};

const formatTimestamp = (timestamp: number) =>
  new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

export default function RightPanel({ routePath, hints = [], checklist = [] }: Props) {
  const [panelState, setLocalPanelState] = useState(() => getPanelState());
  const [notes, setNotes] = useState('');
  const [revealedHints, setRevealedHints] = useState(0);

  const context = useMemo(() => parseContext(routePath), [routePath]);
  const itemSlug = context.itemSlug;
  const [latestResult, setLatestResult] = useState<LastCheckResult | null>(() => (itemSlug ? getLastResult(itemSlug) : null));
  const [requirements, setRequirements] = useState<RequirementItem[]>(() => (itemSlug ? getRequirementChecklist(itemSlug) : []));

  useEffect(() => subscribePanel(setLocalPanelState), []);

  useEffect(() => {
    if (!itemSlug) {
      setLatestResult(null);
      setRequirements([]);
      return;
    }
    setLatestResult(getLastResult(itemSlug));
    if (checklist.length > 0) {
      setRequirementChecklist(
        itemSlug,
        checklist.map((label, index) => ({ id: `content-check-${index + 1}`, label }))
      );
    }
    setRequirements(getRequirementChecklist(itemSlug));
    return subscribeChecks((state) => {
      setLatestResult(state.records[itemSlug] ?? null);
      setRequirements(state.requirements[itemSlug] ?? []);
    });
  }, [itemSlug, checklist]);

  useEffect(() => {
    if (!itemSlug || typeof window === 'undefined') {
      setNotes('');
      return;
    }
    const key = `workspace_notes:${itemSlug}`;
    setNotes(window.localStorage.getItem(key) ?? '');
  }, [itemSlug]);

  useEffect(() => {
    if (!itemSlug || typeof window === 'undefined') return;
    const key = `workspace_notes:${itemSlug}`;
    window.localStorage.setItem(key, notes);
  }, [itemSlug, notes]);

  useEffect(() => {
    setRevealedHints(0);
  }, [itemSlug]);

  const setTab = (activeTab: RightPanelTab) => setPanelState({ activeTab });

  const toggle = () => setPanelState({ isOpen: !panelState.isOpen });

  const failedChecks = latestResult?.checks.filter((check) => !check.pass) ?? [];
  const visibleHints = hints.slice(0, revealedHints);
  const nextHintNumber = Math.min(hints.length, revealedHints + 1);

  const clearNotes = () => {
    setNotes('');
    if (!itemSlug || typeof window === 'undefined') return;
    window.localStorage.removeItem(`workspace_notes:${itemSlug}`);
  };

  const exportNotes = async () => {
    if (!notes.trim() || typeof navigator === 'undefined' || !navigator.clipboard) return;
    await navigator.clipboard.writeText(notes);
  };

  return (
    <aside
      className={`right-panel ${panelState.isOpen ? 'right-panel--open' : ''}`}
      style={{ ['--right-panel-width' as string]: `${panelState.width}px` }}
      data-testid="right-panel"
    >
      <button type="button" className="right-panel__toggle pill" data-testid="right-panel-toggle" onClick={toggle}>
        <span>{panelState.activeTab[0].toUpperCase() + panelState.activeTab.slice(1)}</span>
        <span>{panelState.isOpen ? 'Hide' : 'Show'}</span>
      </button>

      <div className="right-panel__drawer card" aria-hidden={!panelState.isOpen}>
        <header className="right-panel__header">
          <div className="workspace-tabs">
            {([
              ['checks', 'Checks'],
              ['hints', 'Hints'],
              ['notes', 'Notes'],
              ['coach', 'Coach (Coming Soon)'],
            ] as const).map(([key, label]) => (
              <button
                key={key}
                type="button"
                className={`workspace-tab ${panelState.activeTab === key ? 'workspace-tab--active' : ''}`}
                onClick={() => setTab(key)}
                disabled={key === 'coach'}
              >
                {label}
              </button>
            ))}
          </div>
        </header>

        <div className="right-panel__body">
          {panelState.activeTab === 'checks' && (
            <div className="right-panel__checks" data-testid="checks-panel">
              <article className="card">
                <h4>Requirement checklist</h4>
                {requirements.length > 0 ? (
                  <ul>
                    {requirements.map((requirement) => (
                      <li key={requirement.id}>
                        {typeof requirement.pass === 'boolean' ? (requirement.pass ? '✔' : '✖') : '•'} {requirement.label}
                        {requirement.message ? ` — ${requirement.message}` : ''}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="pc-lab__muted">No checklist authored for this item yet.</p>
                )}
              </article>

              {latestResult ? (
                <article className="card">
                  <h4>Latest result</h4>
                  <p>
                    <span className={`pill ${latestResult.passed ? 'pill--success' : ''}`}>
                      {latestResult.passed ? 'PASS' : 'NEEDS WORK'}
                    </span>
                  </p>
                  {typeof latestResult.score === 'number' && <p>Score: {latestResult.score}%</p>}
                  {failedChecks.length > 0 ? (
                    <>
                      <p><strong>Failed checks</strong></p>
                      <ul>
                        {failedChecks.map((check) => (
                          <li key={check.id}>
                            ✖ {check.label}
                            {check.message ? ` — ${check.message}` : ''}
                          </li>
                        ))}
                      </ul>
                    </>
                  ) : (
                    <p className="pc-lab__muted">No failed checks in latest result.</p>
                  )}
                  <p className="pc-lab__muted">Updated {formatTimestamp(latestResult.timestamp)}</p>
                </article>
              ) : (
                <p className="pc-lab__muted">Run Check or Submit to populate this panel.</p>
              )}
              <button type="button" className="btn-ghost" onClick={() => clearAllChecks()}>Clear checks</button>
            </div>
          )}

          {panelState.activeTab === 'hints' && (
            <article className="card">
              <h4>Hints</h4>
              {hints.length > 0 ? (
                <>
                  <ul>
                    {visibleHints.map((hint, index) => (
                      <li key={`${hint}-${index}`}>{hint}</li>
                    ))}
                  </ul>
                  {revealedHints < hints.length && (
                    <button
                      type="button"
                      className="btn-secondary"
                      onClick={() => setRevealedHints((value) => Math.min(hints.length, value + 1))}
                    >
                      Show hint {nextHintNumber}
                    </button>
                  )}
                </>
              ) : (
                <p className="pc-lab__muted">
                  No hints authored yet. <a href="#hints-frontmatter">Add hints in content frontmatter</a>.
                </p>
              )}
            </article>
          )}

          {panelState.activeTab === 'notes' && (
            <article className="card">
              <h4>Notes</h4>
              <textarea
                className="right-panel__notes"
                placeholder="Write your notes..."
                value={notes}
                onChange={(event) => setNotes(event.target.value)}
              />
              <div className="right-panel__actions">
                <button type="button" className="btn-ghost" onClick={clearNotes}>Clear notes</button>
                <button type="button" className="btn-secondary" onClick={() => void exportNotes()} disabled={!notes.trim()}>
                  Export
                </button>
              </div>
            </article>
          )}

          {panelState.activeTab === 'coach' && (
            <article className="card">
              <h4>Coach</h4>
              <p className="pc-lab__muted">Coming soon: Beattie Tech Coach (class LLM integration)</p>
            </article>
          )}
        </div>
      </div>
    </aside>
  );
}
