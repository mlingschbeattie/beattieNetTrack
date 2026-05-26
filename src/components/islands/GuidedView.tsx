import { useEffect, useMemo, useState } from 'react';
import { getSectionProgress, markSectionComplete } from '../../lib/progressStore';

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

interface GuidedViewProps {
  lessonSlug: string;
  sections: LessonSection[];
}

interface GuidedReadingSection {
  id: string;
  title: string;
  sectionId: string;
  blocks: string[];
  check: SectionCheck;
}

type FeedbackState = { kind: 'correct' | 'incorrect'; index: number } | null;

const normalize = (value: string) => value.trim().toLowerCase();

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

const fallbackCheck = (title: string): SectionCheck => ({
  prompt: `Checkpoint: did you understand the main idea of "${title}"?`,
  options: ['Yes - I can explain it', 'Not yet', 'Need one more example', 'I skipped this section'],
  correct: 0,
});

const fallbackSectionId = (lessonSlug: string, index: number) => `reading-${lessonSlug}-${index + 1}`;

export default function GuidedView({ lessonSlug, sections }: GuidedViewProps) {
  const [readingSections, setReadingSections] = useState<GuidedReadingSection[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [revealedCount, setRevealedCount] = useState<Record<string, number>>({});
  const [autoPlay, setAutoPlay] = useState(false);
  const [autoSeconds, setAutoSeconds] = useState(5);
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});
  const [feedbackMap, setFeedbackMap] = useState<Record<string, FeedbackState>>({});

  const activeSection = readingSections[activeIndex] ?? null;

  const sectionLookup = useMemo(() => {
    const map = new Map<string, LessonSection>();
    for (const section of sections) {
      map.set(normalize(section.title), section);
    }
    return map;
  }, [sections]);

  const syncProgress = (targetSections: GuidedReadingSection[] = readingSections) => {
    const progress = getSectionProgress(lessonSlug);
    setCompletedMap(progress);
    const completedCount = targetSections.filter((section) => progress[section.sectionId]).length;
    dispatchProgress(lessonSlug, completedCount, targetSections.length);
  };

  useEffect(() => {
    const root = document.querySelector('[data-reading-content]');
    if (!root) {
      setReadingSections([]);
      return;
    }

    const h2s = Array.from(root.querySelectorAll('h2')) as HTMLHeadingElement[];

    const nextReadingSections: GuidedReadingSection[] = h2s.map((heading, index) => {
      const title = heading.textContent?.trim() || `Section ${index + 1}`;
      const matched = sectionLookup.get(normalize(title));
      const sectionId = matched?.id ?? fallbackSectionId(lessonSlug, index);

      if (!heading.id) heading.id = `guided-heading-${lessonSlug}-${index + 1}`;

      const blocks: string[] = [];
      let node = heading.nextElementSibling;
      while (node && node.tagName.toLowerCase() !== 'h2') {
        const tag = node.tagName.toLowerCase();
        if (['p', 'ul', 'ol', 'pre', 'table', 'blockquote', 'div', 'h3', 'h4'].includes(tag)) {
          blocks.push(node.outerHTML);
        }
        node = node.nextElementSibling;
      }

      return {
        id: `${heading.id}-guided`,
        title,
        sectionId,
        blocks: blocks.length ? blocks : [`<p>No section content blocks were detected for <strong>${title}</strong>.</p>`],
        check: matched?.check?.[0] ?? fallbackCheck(title),
      };
    });

    if (!nextReadingSections.length) {
      const bodyBlocks = Array.from(root.querySelectorAll('p')).slice(0, 6).map((p) => p.outerHTML);
      nextReadingSections.push({
        id: `guided-fallback-${lessonSlug}`,
        title: 'Lesson Walkthrough',
        sectionId: fallbackSectionId(lessonSlug, 0),
        blocks: bodyBlocks.length ? bodyBlocks : ['<p>Use Reading mode to view the full lesson content.</p>'],
        check: fallbackCheck('Lesson Walkthrough'),
      });
    }

    const initialReveal = Object.fromEntries(nextReadingSections.map((s) => [s.id, 1]));
    setReadingSections(nextReadingSections);
    setRevealedCount(initialReveal);
    setActiveIndex(0);
    syncProgress(nextReadingSections);
  }, [lessonSlug, sectionLookup]);

  useEffect(() => {
    if (!autoPlay || !activeSection) return;
    const currentReveal = revealedCount[activeSection.id] ?? 1;
    if (currentReveal >= activeSection.blocks.length) return;

    const timeout = window.setTimeout(() => {
      setRevealedCount((prev) => ({
        ...prev,
        [activeSection.id]: Math.min(activeSection.blocks.length, (prev[activeSection.id] ?? 1) + 1),
      }));
    }, Math.max(2, autoSeconds) * 1000);

    return () => window.clearTimeout(timeout);
  }, [autoPlay, autoSeconds, activeSection, revealedCount]);

  useEffect(() => {
    const handler = (event: Event) => {
      const detail = (event as CustomEvent<{ lessonSlug?: string }>).detail;
      if (!detail || detail.lessonSlug !== lessonSlug) return;
      syncProgress();
    };

    window.addEventListener('section-progress-updated', handler);
    return () => window.removeEventListener('section-progress-updated', handler);
  }, [lessonSlug, readingSections]);

  const completedCount = useMemo(
    () => readingSections.filter((section) => completedMap[section.sectionId]).length,
    [readingSections, completedMap]
  );

  const moveSection = (delta: number) => {
    setActiveIndex((idx) => Math.min(readingSections.length - 1, Math.max(0, idx + delta)));
    setFeedbackMap({});
  };

  const revealNext = () => {
    if (!activeSection) return;
    setRevealedCount((prev) => ({
      ...prev,
      [activeSection.id]: Math.min(activeSection.blocks.length, (prev[activeSection.id] ?? 1) + 1),
    }));
  };

  const revealPrev = () => {
    if (!activeSection) return;
    setRevealedCount((prev) => ({
      ...prev,
      [activeSection.id]: Math.max(1, (prev[activeSection.id] ?? 1) - 1),
    }));
  };

  const revealAll = () => {
    if (!activeSection) return;
    setRevealedCount((prev) => ({
      ...prev,
      [activeSection.id]: activeSection.blocks.length,
    }));
  };

  const goToReading = (title: string) => {
    window.dispatchEvent(
      new CustomEvent('lesson:jump-reading', {
        detail: { title },
      })
    );
  };

  const answerCheckpoint = (optionIndex: number) => {
    if (!activeSection) return;
    const isCorrect = optionIndex === activeSection.check.correct;

    if (!isCorrect) {
      setFeedbackMap((prev) => ({
        ...prev,
        [activeSection.id]: { kind: 'incorrect', index: optionIndex },
      }));
      return;
    }

    setFeedbackMap((prev) => ({
      ...prev,
      [activeSection.id]: { kind: 'correct', index: optionIndex },
    }));

    window.setTimeout(() => {
      markSectionComplete(lessonSlug, activeSection.sectionId);
      dispatchSectionSync(lessonSlug);
      syncProgress();
      setFeedbackMap((prev) => ({
        ...prev,
        [activeSection.id]: null,
      }));
    }, 450);
  };

  if (!activeSection) return null;

  const revealed = Math.max(1, revealedCount[activeSection.id] ?? 1);
  const visibleBlocks = activeSection.blocks.slice(0, revealed);
  const isDone = Boolean(completedMap[activeSection.sectionId]);
  const feedback = feedbackMap[activeSection.id] ?? null;

  return (
    <div className="guided-root" data-completed={completedCount} data-total={readingSections.length}>
      <div className="guided-head">
        <div>
          <p className="guided-eyebrow">Guided Walkthrough</p>
          <h3>{activeSection.title}</h3>
        </div>
        <div className="guided-progress">{activeIndex + 1} / {readingSections.length}</div>
      </div>

      <div className="guided-controls">
        <button type="button" className="guided-btn" onClick={() => moveSection(-1)} disabled={activeIndex === 0}>Previous Section</button>
        <button type="button" className="guided-btn" onClick={() => moveSection(1)} disabled={activeIndex === readingSections.length - 1}>Next Section</button>
        <button type="button" className="guided-btn guided-btn--ghost" onClick={() => goToReading(activeSection.title)}>
          Jump To Reading
        </button>
      </div>

      <div className="guided-pacing">
        <label className="guided-toggle">
          <input
            type="checkbox"
            checked={autoPlay}
            onChange={(event) => setAutoPlay(event.target.checked)}
          />
          Auto reveal
        </label>
        <label className="guided-speed">
          Pace
          <select
            value={autoSeconds}
            onChange={(event) => setAutoSeconds(Number(event.target.value))}
            disabled={!autoPlay}
          >
            <option value={3}>Fast</option>
            <option value={5}>Normal</option>
            <option value={7}>Slow</option>
          </select>
        </label>
      </div>

      <article className="guided-reading-blocks">
        {visibleBlocks.map((html, index) => (
          <section
            key={`${activeSection.id}-block-${index}`}
            className="guided-reading-block"
            dangerouslySetInnerHTML={{ __html: html }}
          />
        ))}
      </article>

      <div className="guided-reveal-controls">
        <button type="button" className="guided-btn" onClick={revealPrev} disabled={revealed <= 1}>Reveal Less</button>
        <button type="button" className="guided-btn" onClick={revealNext} disabled={revealed >= activeSection.blocks.length}>Reveal Next</button>
        <button type="button" className="guided-btn" onClick={revealAll} disabled={revealed >= activeSection.blocks.length}>Reveal Full Section</button>
      </div>

      {isDone ? (
        <div className="guided-chip is-done">Section complete</div>
      ) : (
        <div className="guided-check">
          <p className="guided-check__prompt">{activeSection.check.prompt}</p>
          <div className="guided-check__options">
            {activeSection.check.options.map((option, index) => {
              const isSelected = feedback?.index === index;
              const stateClass =
                isSelected && feedback?.kind === 'correct'
                  ? 'is-correct'
                  : isSelected && feedback?.kind === 'incorrect'
                    ? 'is-incorrect'
                    : '';
              return (
                <button
                  key={index}
                  type="button"
                  className={`guided-option ${stateClass}`}
                  onClick={() => answerCheckpoint(index)}
                  disabled={feedback?.kind === 'correct'}
                >
                  {option}
                </button>
              );
            })}
          </div>
          {feedback?.kind === 'incorrect' ? (
            <p className="guided-feedback is-warn">Not quite - try again.</p>
          ) : feedback?.kind === 'correct' ? (
            <p className="guided-feedback is-ok">Nice. Section marked complete.</p>
          ) : null}
        </div>
      )}

      <ol className="guided-index">
        {readingSections.map((section, index) => (
          <li key={section.id}>
            <button
              type="button"
              className={`guided-index__item ${index === activeIndex ? 'is-active' : ''} ${completedMap[section.sectionId] ? 'is-done' : ''}`}
              onClick={() => setActiveIndex(index)}
            >
              <span>{String(index + 1).padStart(2, '0')}</span>
              <span>{section.title}</span>
            </button>
          </li>
        ))}
      </ol>

      <style>{`
        .guided-root {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          background: var(--color-surface);
          padding: var(--space-4);
          display: grid;
          gap: var(--space-4);
        }
        .guided-head {
          display: flex;
          justify-content: space-between;
          gap: var(--space-3);
          align-items: baseline;
        }
        .guided-head h3 {
          margin: 0;
          font-size: var(--text-xl);
        }
        .guided-eyebrow {
          margin: 0 0 var(--space-1);
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--color-text-muted);
          font-size: var(--text-xs);
        }
        .guided-progress {
          font-family: var(--font-mono);
          color: var(--color-primary);
          font-size: var(--text-sm);
        }
        .guided-controls,
        .guided-reveal-controls {
          display: flex;
          flex-wrap: wrap;
          gap: var(--space-2);
        }
        .guided-btn {
          border: 1px solid var(--color-border);
          background: var(--color-surface-2);
          color: var(--color-text);
          border-radius: var(--radius-sm);
          padding: var(--space-2) var(--space-3);
          font: inherit;
          font-size: var(--text-sm);
          cursor: pointer;
        }
        .guided-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        .guided-btn:hover:not(:disabled) {
          border-color: var(--color-primary);
        }
        .guided-btn--ghost {
          color: var(--color-primary);
        }
        .guided-pacing {
          display: flex;
          gap: var(--space-3);
          align-items: center;
          flex-wrap: wrap;
        }
        .guided-toggle,
        .guided-speed {
          display: inline-flex;
          gap: var(--space-2);
          align-items: center;
          color: var(--color-text-muted);
          font-size: var(--text-sm);
        }
        .guided-speed select {
          border: 1px solid var(--color-border);
          background: var(--color-surface-2);
          color: var(--color-text);
          border-radius: var(--radius-sm);
          padding: var(--space-1) var(--space-2);
        }
        .guided-reading-blocks {
          display: grid;
          gap: var(--space-3);
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          padding: var(--space-4);
          background: linear-gradient(180deg, var(--color-surface-2), var(--color-surface));
        }
        .guided-reading-block {
          color: var(--color-text-soft);
          line-height: var(--leading-normal);
          animation: guided-fade 220ms ease-out both;
        }
        .guided-reading-block :global(p) {
          margin: 0;
        }
        .guided-reading-block :global(p + p) {
          margin-top: var(--space-3);
        }
        .guided-reading-block :global(ul),
        .guided-reading-block :global(ol) {
          margin: 0;
          padding-left: 1.2rem;
        }
        .guided-reading-block :global(li + li) {
          margin-top: var(--space-2);
        }
        .guided-reading-block :global(strong) {
          color: var(--color-text);
        }
        .guided-chip {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-pill);
          padding: var(--space-2) var(--space-3);
          width: max-content;
          font-size: var(--text-sm);
        }
        .guided-chip.is-done {
          color: var(--color-accent);
          border-color: var(--color-accent);
        }
        .guided-check {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          padding: var(--space-3);
          background: var(--color-surface-2);
          display: grid;
          gap: var(--space-3);
        }
        .guided-check__prompt {
          margin: 0;
          color: var(--color-text);
        }
        .guided-check__options {
          display: grid;
          gap: var(--space-2);
        }
        .guided-option {
          text-align: left;
          border: 1px solid var(--color-border);
          background: var(--color-surface);
          color: var(--color-text);
          border-radius: var(--radius-sm);
          padding: var(--space-2) var(--space-3);
          cursor: pointer;
          font: inherit;
        }
        .guided-option:hover:not(:disabled) {
          border-color: var(--color-primary);
        }
        .guided-option.is-correct {
          border-color: var(--color-accent);
          color: var(--color-accent);
        }
        .guided-option.is-incorrect {
          border-color: var(--color-warning);
          color: var(--color-warning);
        }
        .guided-feedback {
          margin: 0;
          font-size: var(--text-sm);
        }
        .guided-feedback.is-ok {
          color: var(--color-accent);
        }
        .guided-feedback.is-warn {
          color: var(--color-warning);
        }
        .guided-index {
          list-style: none;
          margin: 0;
          padding: 0;
          display: grid;
          gap: var(--space-2);
        }
        .guided-index__item {
          width: 100%;
          border: 1px solid var(--color-border);
          background: transparent;
          color: var(--color-text-soft);
          border-radius: var(--radius-sm);
          padding: var(--space-2) var(--space-3);
          text-align: left;
          display: grid;
          grid-template-columns: auto 1fr;
          gap: var(--space-3);
          cursor: pointer;
          font: inherit;
        }
        .guided-index__item.is-active {
          border-color: var(--color-primary);
          color: var(--color-text);
        }
        .guided-index__item.is-done {
          border-color: var(--color-accent);
        }
        @keyframes guided-fade {
          from {
            opacity: 0;
            transform: translateY(6px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}
