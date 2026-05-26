import { useEffect, useMemo, useState } from 'react';
import {
  getSectionProgress,
  markSectionComplete,
} from '../../lib/progressStore';

interface SectionCheck {
  prompt: string;
  options: string[];
  correct: number;
}

interface LessonSection {
  id: string;
  title: string;
  keyPoints: string[];
  check: SectionCheck[];
}

interface OutlineViewProps {
  lessonSlug: string;
  sections: LessonSection[];
}

type CheckPhase = 'idle' | 'q1' | 'q2';
type FeedbackState = { kind: 'correct' | 'incorrect'; index: number } | null;

const normalize = (value: string) => value.trim().toLowerCase();

const cleanText = (value: string) => value.replace(/\s+/g, ' ').trim();

const truncatePoint = (value: string, max = 130) => {
  if (value.length <= max) return value;
  return `${value.slice(0, max - 1).trimEnd()}...`;
};

const fallbackKeyPoints = (title: string): string[] => [
  `${title}: identify the main concept and where it applies in real hardware work.`,
  'Pay attention to component labels, connector locations, and role in the system.',
  'Use this section as a visual recognition and troubleshooting reference.',
];

const fallbackCheck = (title: string, keyPoints: string[]): SectionCheck[] => {
  const [first = title, second = 'this section'] = keyPoints;
  return [
    {
      prompt: `What is the main focus of "${title}"?`,
      options: [first, second, 'Only software updates', 'Only BIOS shortcuts'],
      correct: 0,
    },
    {
      prompt: `What should you be able to do after "${title}"?`,
      options: [
        'Recognize components and apply the concept during troubleshooting',
        'Skip directly to replacement without diagnosis',
        'Ignore connector and layout details',
        'Rely on guesswork to identify parts',
      ],
      correct: 0,
    },
  ];
};

const extractKeyPointsFromNodes = (nodes: Element[]): string[] => {
  const candidates: Array<{ text: string; score: number; index: number }> = [];
  let order = 0;

  const pushCandidate = (text: string, score: number) => {
    const cleaned = cleanText(text);
    if (cleaned.length < 28) return;
    candidates.push({ text: cleaned, score, index: order++ });
  };

  for (const node of nodes) {
    const tag = node.tagName.toLowerCase();

    if (tag === 'ul' || tag === 'ol') {
      const items = Array.from(node.querySelectorAll('li'));
      for (const item of items.slice(0, 4)) {
        pushCandidate(item.textContent ?? '', 3);
      }
      continue;
    }

    if (tag === 'h3' || tag === 'h4') {
      pushCandidate(node.textContent ?? '', 2);
      continue;
    }

    if (tag !== 'p') continue;

    const paragraph = cleanText(node.textContent ?? '');
    if (!paragraph) continue;

    const definitionMatch = paragraph.match(/^([^.!?]{3,80})(?:\s+[\u2014\-:]\s+)(.+)$/);
    if (definitionMatch) {
      pushCandidate(paragraph, 4);
      continue;
    }

    const firstSentence = paragraph.split(/(?<=[.!?])\s+/)[0] ?? paragraph;
    pushCandidate(firstSentence, 1);
  }

  const seen = new Set<string>();
  return candidates
    .sort((a, b) => (b.score - a.score) || (a.index - b.index))
    .map((item) => item.text)
    .filter((text) => {
      const key = normalize(text.replace(/[.,;:!?]+$/g, ''));
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, 3)
    .map((text) => truncatePoint(text));
};

const dispatchProgress = (lessonSlug: string, completed: number, total: number) => {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(
    new CustomEvent('outline-progress', {
      detail: { lessonSlug, completed, total },
    })
  );
};

const dispatchSectionSync = (lessonSlug: string) => {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(
    new CustomEvent('section-progress-updated', {
      detail: { lessonSlug },
    })
  );
};

export default function OutlineView({ lessonSlug, sections }: OutlineViewProps) {
  const [displaySections, setDisplaySections] = useState<LessonSection[]>(sections);
  const total = displaySections.length;
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});
  const [openMap, setOpenMap] = useState<Record<string, boolean>>({});
  const [phaseMap, setPhaseMap] = useState<Record<string, CheckPhase>>({});
  const [feedbackMap, setFeedbackMap] = useState<Record<string, FeedbackState>>({});

  useEffect(() => {
    let cancelled = false;
    let retryTimer: number | null = null;
    let attempts = 0;

    const sectionLookup = new Map<string, LessonSection>();
    for (const section of sections) {
      sectionLookup.set(normalize(section.title), section);
    }

    const hydrateFromReading = (): boolean => {
      const root = document.querySelector('[data-reading-content]');
      if (!root) return false;

      const h2Headings = Array.from(root.querySelectorAll('h2')) as HTMLHeadingElement[];
      const h3Headings = Array.from(root.querySelectorAll('h3')) as HTMLHeadingElement[];
      const headings = h2Headings.length ? h2Headings : h3Headings;
      if (!headings.length) return false;

      const enrichedSections = headings.map((heading, index) => {
        const title = cleanText(heading.textContent ?? '') || `Section ${index + 1}`;
        const authored = sectionLookup.get(normalize(title));

        const nodes: Element[] = [];
        let cursor = heading.nextElementSibling;
        while (
          cursor
          && cursor.tagName.toLowerCase() !== 'h2'
          && (!h3Headings.length || cursor.tagName.toLowerCase() !== 'h3')
        ) {
          const tag = cursor.tagName.toLowerCase();
          if (['p', 'ul', 'ol', 'h3', 'h4'].includes(tag)) {
            nodes.push(cursor);
          }
          cursor = cursor.nextElementSibling;
        }

        const generatedKeyPoints = extractKeyPointsFromNodes(nodes);
        const keyPoints = generatedKeyPoints.length
          ? generatedKeyPoints
          : authored?.keyPoints?.length
          ? authored.keyPoints
          : fallbackKeyPoints(title);

        const check = authored?.check?.length === 2
          ? authored.check
          : fallbackCheck(title, keyPoints);

        return {
          id: authored?.id ?? `outline-${lessonSlug}-${index + 1}`,
          title,
          keyPoints,
          check,
        } satisfies LessonSection;
      });

      setDisplaySections(enrichedSections.length ? enrichedSections : sections);
      return true;
    };

    const attemptHydrate = () => {
      if (cancelled) return;
      const ok = hydrateFromReading();
      if (ok) return;
      attempts += 1;
      if (attempts > 20) {
        setDisplaySections(sections);
        return;
      }
      retryTimer = window.setTimeout(attemptHydrate, 120);
    };

    attemptHydrate();

    const observer = new MutationObserver(() => {
      if (cancelled) return;
      hydrateFromReading();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    return () => {
      cancelled = true;
      if (retryTimer !== null) window.clearTimeout(retryTimer);
      observer.disconnect();
    };
  }, [lessonSlug, sections]);

  const syncProgress = () => {
    const progress = getSectionProgress(lessonSlug);
    setCompletedMap(progress);
    const completedCount = displaySections.filter((s) => progress[s.id]).length;
    dispatchProgress(lessonSlug, completedCount, total);
  };

  useEffect(() => {
    syncProgress();
  }, [lessonSlug, displaySections, total]);

  useEffect(() => {
    const handler = (event: Event) => {
      const detail = (event as CustomEvent<{ lessonSlug?: string }>).detail;
      if (!detail || detail.lessonSlug !== lessonSlug) return;
      syncProgress();
    };
    window.addEventListener('section-progress-updated', handler);
    return () => window.removeEventListener('section-progress-updated', handler);
  }, [lessonSlug, displaySections, total]);

  const completedCount = useMemo(
    () => displaySections.filter((s) => completedMap[s.id]).length,
    [displaySections, completedMap]
  );

  useEffect(() => {
    dispatchProgress(lessonSlug, completedCount, total);
  }, [lessonSlug, completedCount, total]);

  const toggleOpen = (id: string) => {
    setOpenMap((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const startCheck = (id: string) => {
    setPhaseMap((prev) => ({ ...prev, [id]: 'q1' }));
    setFeedbackMap((prev) => ({ ...prev, [id]: null }));
  };

  const handleAnswer = (section: LessonSection, optionIndex: number) => {
    const phase = phaseMap[section.id] ?? 'q1';
    const qIndex = phase === 'q2' ? 1 : 0;
    const question = section.check[qIndex];
    const isCorrect = optionIndex === question.correct;

    if (!isCorrect) {
      setFeedbackMap((prev) => ({
        ...prev,
        [section.id]: { kind: 'incorrect', index: optionIndex },
      }));
      return;
    }

    setFeedbackMap((prev) => ({
      ...prev,
      [section.id]: { kind: 'correct', index: optionIndex },
    }));

    window.setTimeout(() => {
      if (qIndex === 0) {
        setPhaseMap((prev) => ({ ...prev, [section.id]: 'q2' }));
        setFeedbackMap((prev) => ({ ...prev, [section.id]: null }));
      } else {
        markSectionComplete(lessonSlug, section.id);
        setCompletedMap((prev) => ({ ...prev, [section.id]: true }));
        dispatchSectionSync(lessonSlug);
        setPhaseMap((prev) => ({ ...prev, [section.id]: 'idle' }));
        setFeedbackMap((prev) => ({ ...prev, [section.id]: null }));
      }
    }, 600);
  };

  const jumpToReading = (title: string) => {
    window.dispatchEvent(
      new CustomEvent('lesson:jump-reading', {
        detail: { title },
      })
    );
  };

  return (
    <div className="outline-root" data-completed={completedCount} data-total={total}>
      <ol className="outline-list">
        {displaySections.map((section, index) => {
          const isOpen = Boolean(openMap[section.id]);
          const isDone = Boolean(completedMap[section.id]);
          const phase = phaseMap[section.id] ?? 'idle';
          const feedback = feedbackMap[section.id] ?? null;
          const statusLabel = isDone ? 'Done' : isOpen ? 'In progress' : 'Not started';
          const statusClass = isDone ? 'is-done' : isOpen ? 'is-active' : 'is-idle';
          const num = String(index + 1).padStart(2, '0');
          const qIndex = phase === 'q2' ? 1 : 0;
          const activeQuestion = phase !== 'idle' ? section.check[qIndex] : null;

          return (
            <li key={section.id} className={`outline-item ${statusClass} ${isOpen ? 'is-open' : ''}`}>
              <button
                type="button"
                className="outline-header"
                aria-expanded={isOpen}
                onClick={() => toggleOpen(section.id)}
              >
                <span className="outline-num">{num}</span>
                <span className="outline-title">{section.title}</span>
                <span className={`outline-status ${statusClass}`}>
                  <span className="outline-dot" aria-hidden="true" />
                  {statusLabel}
                </span>
                <span className={`outline-chevron ${isOpen ? 'is-open' : ''}`} aria-hidden="true">
                  ▾
                </span>
              </button>

              {isOpen ? (
                <div className="outline-body">
                  <ul className="outline-points">
                    {section.keyPoints.map((point, i) => (
                      <li key={i}>
                        <span className="outline-check" aria-hidden="true">✓</span>
                        <span>{point}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="outline-actions">
                    {isDone ? (
                      <div className="outline-chip is-done">Check passed</div>
                    ) : phase === 'idle' ? (
                      <button
                        type="button"
                        className="outline-chip is-action"
                        onClick={() => startCheck(section.id)}
                      >
                        Take quick check
                      </button>
                    ) : null}
                    <button
                      type="button"
                      className="outline-chip is-ghost"
                      onClick={() => jumpToReading(section.title)}
                    >
                      Jump to reading
                    </button>
                  </div>

                  {phase !== 'idle' && !isDone && activeQuestion ? (
                    <div className="outline-check-panel">
                      <div className="outline-check-meta">
                        Question {qIndex + 1} of 2
                      </div>
                      <p className="outline-check-prompt">{activeQuestion.prompt}</p>
                      <div className="outline-check-options">
                        {activeQuestion.options.map((option, i) => {
                          const isSelected = feedback?.index === i;
                          const stateClass =
                            isSelected && feedback?.kind === 'correct'
                              ? 'is-correct'
                              : isSelected && feedback?.kind === 'incorrect'
                              ? 'is-incorrect'
                              : '';
                          return (
                            <button
                              key={i}
                              type="button"
                              className={`outline-option ${stateClass}`}
                              onClick={() => handleAnswer(section, i)}
                              disabled={feedback?.kind === 'correct'}
                            >
                              {option}
                            </button>
                          );
                        })}
                      </div>
                      {feedback?.kind === 'incorrect' ? (
                        <div className="outline-feedback is-warn">Not quite — try again.</div>
                      ) : feedback?.kind === 'correct' ? (
                        <div className="outline-feedback is-ok">
                          {qIndex === 0 ? 'Correct — next question.' : 'Section complete.'}
                        </div>
                      ) : null}
                    </div>
                  ) : null}
                </div>
              ) : null}
            </li>
          );
        })}
      </ol>

      <style>{`
        .outline-root {
          display: block;
          width: 100%;
        }
        .outline-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: grid;
          gap: var(--space-3);
        }
        .outline-item {
          background: var(--color-surface);
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          overflow: hidden;
          transition: border-color var(--transition-fast);
        }
        .outline-item.is-done {
          border-color: var(--color-accent);
        }
        .outline-header {
          display: grid;
          grid-template-columns: auto 1fr auto auto;
          align-items: center;
          gap: var(--space-3);
          width: 100%;
          padding: var(--space-3) var(--space-4);
          background: transparent;
          border: 0;
          color: var(--color-text);
          font: inherit;
          text-align: left;
          cursor: pointer;
        }
        .outline-header:hover {
          background: var(--color-surface-2);
        }
        .outline-num {
          font-family: var(--font-mono);
          font-size: var(--text-sm);
          color: var(--color-text-muted);
          letter-spacing: 0.04em;
        }
        .outline-title {
          font-size: var(--text-base);
          font-weight: 600;
          color: var(--color-text);
        }
        .outline-status {
          display: inline-flex;
          align-items: center;
          gap: var(--space-2);
          font-size: var(--text-xs);
          color: var(--color-text-muted);
          padding: var(--space-1) var(--space-3);
          border-radius: var(--radius-pill);
          background: var(--color-surface-2);
          border: 1px solid var(--color-border);
        }
        .outline-status.is-done {
          color: var(--color-accent);
          border-color: var(--color-accent);
        }
        .outline-status.is-active {
          color: var(--color-primary);
          border-color: var(--color-primary);
        }
        .outline-dot {
          width: 8px;
          height: 8px;
          border-radius: var(--radius-full);
          background: var(--color-text-muted);
        }
        .outline-status.is-done .outline-dot { background: var(--color-accent); }
        .outline-status.is-active .outline-dot { background: var(--color-primary); }
        .outline-chevron {
          color: var(--color-text-muted);
          transition: transform var(--transition-fast);
          font-size: var(--text-base);
        }
        .outline-chevron.is-open {
          transform: rotate(180deg);
        }
        .outline-body {
          padding: 0 var(--space-4) var(--space-4);
          display: grid;
          gap: var(--space-4);
          border-top: 1px solid var(--color-border);
        }
        .outline-points {
          list-style: none;
          margin: var(--space-4) 0 0;
          padding: 0;
          display: grid;
          gap: var(--space-2);
        }
        .outline-points li {
          display: grid;
          grid-template-columns: auto 1fr;
          gap: var(--space-3);
          color: var(--color-text-soft);
          font-size: var(--text-sm);
          line-height: var(--leading-normal);
        }
        .outline-check {
          color: var(--color-accent);
          font-weight: 700;
        }
        .outline-chip {
          display: inline-flex;
          align-items: center;
          gap: var(--space-2);
          padding: var(--space-2) var(--space-4);
          border-radius: var(--radius-pill);
          font-size: var(--text-sm);
          font-weight: 600;
          border: 1px solid var(--color-border);
          background: var(--color-surface-2);
          color: var(--color-text);
          width: max-content;
          cursor: default;
        }
        .outline-chip.is-done {
          color: var(--color-accent);
          border-color: var(--color-accent);
          background: transparent;
        }
        button.outline-chip {
          cursor: pointer;
        }
        .outline-chip.is-action {
          color: var(--color-primary);
          border-color: var(--color-primary);
        }
        .outline-chip.is-action:hover {
          background: var(--color-highlight);
        }
        .outline-chip.is-ghost {
          color: var(--color-text-muted);
        }
        .outline-chip.is-ghost:hover {
          border-color: var(--color-primary);
          color: var(--color-primary);
        }
        .outline-actions {
          display: flex;
          flex-wrap: wrap;
          gap: var(--space-2);
          align-items: center;
        }
        .outline-check-panel {
          display: grid;
          gap: var(--space-3);
          padding: var(--space-4);
          background: var(--color-surface-2);
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
        }
        .outline-check-meta {
          font-size: var(--text-xs);
          color: var(--color-text-muted);
          text-transform: uppercase;
          letter-spacing: 0.08em;
        }
        .outline-check-prompt {
          margin: 0;
          font-size: var(--text-base);
          color: var(--color-text);
          line-height: var(--leading-normal);
        }
        .outline-check-options {
          display: grid;
          gap: var(--space-2);
        }
        .outline-option {
          display: block;
          width: 100%;
          text-align: left;
          padding: var(--space-3) var(--space-4);
          background: var(--color-surface);
          color: var(--color-text);
          border: 1px solid var(--color-border);
          border-radius: var(--radius-sm);
          font: inherit;
          cursor: pointer;
          transition: border-color var(--transition-fast), background var(--transition-fast);
        }
        .outline-option:hover:not(:disabled) {
          border-color: var(--color-primary);
          background: var(--color-highlight);
        }
        .outline-option:disabled {
          cursor: default;
        }
        .outline-option.is-correct {
          border-color: var(--color-accent);
          color: var(--color-accent);
        }
        .outline-option.is-incorrect {
          border-color: var(--color-warning);
          color: var(--color-warning);
        }
        .outline-feedback {
          font-size: var(--text-sm);
          padding: var(--space-2) var(--space-3);
          border-radius: var(--radius-sm);
        }
        .outline-feedback.is-ok {
          color: var(--color-accent);
          border: 1px solid var(--color-accent);
        }
        .outline-feedback.is-warn {
          color: var(--color-warning);
          border: 1px solid var(--color-warning);
        }
        @media (max-width: 640px) {
          .outline-header {
            grid-template-columns: auto 1fr auto;
          }
          .outline-status {
            display: none;
          }
        }
      `}</style>
    </div>
  );
}
