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
  focusPoints: string[];
  excerpt: string;
}

const normalize = (value: string) => value.trim().toLowerCase();

const cleanText = (value: string) => value.replace(/\s+/g, ' ').trim();

const truncate = (value: string, max = 170) => {
  if (value.length <= max) return value;
  return `${value.slice(0, max - 1).trimEnd()}...`;
};

const fallbackSectionId = (lessonSlug: string, index: number) => `guided-${lessonSlug}-${index + 1}`;

const fallbackFocusPoints = (title: string): string[] => [
  `Identify the main purpose of ${title}.`,
  'Connect the concept to a real troubleshooting decision.',
  'Use this as a checkpoint before moving to the next section.',
];

const extractFocusPoints = (nodes: Element[]): string[] => {
  const items: string[] = [];

  for (const node of nodes) {
    const tag = node.tagName.toLowerCase();

    if ((tag === 'ul' || tag === 'ol') && items.length < 3) {
      const listItems = Array.from(node.querySelectorAll('li'));
      for (const li of listItems) {
        const text = cleanText(li.textContent ?? '');
        if (text.length >= 24) items.push(text);
        if (items.length >= 3) break;
      }
    }

    if (items.length >= 3) break;

    if (tag === 'p') {
      const paragraph = cleanText(node.textContent ?? '');
      if (!paragraph) continue;
      const sentence = paragraph.split(/(?<=[.!?])\s+/)[0] ?? paragraph;
      if (sentence.length >= 24) items.push(sentence);
      if (items.length >= 3) break;
    }
  }

  const seen = new Set<string>();
  return items
    .map((text) => truncate(text, 145))
    .filter((text) => {
      const key = normalize(text.replace(/[.,;:!?]+$/g, ''));
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, 3);
};

const extractExcerpt = (nodes: Element[], title: string) => {
  const paragraphNode = nodes.find((node) => node.tagName.toLowerCase() === 'p');
  if (!paragraphNode) {
    return `Use Reading mode for the full details in "${title}".`;
  }
  const paragraph = cleanText(paragraphNode.textContent ?? '');
  if (!paragraph) {
    return `Use Reading mode for the full details in "${title}".`;
  }
  return truncate(paragraph, 240);
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

export default function GuidedView({ lessonSlug, sections }: GuidedViewProps) {
  const [readingSections, setReadingSections] = useState<GuidedReadingSection[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});

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
    let cancelled = false;
    let retryTimer: number | null = null;
    let attempts = 0;

    const hydrateFromReading = (): boolean => {
      const root = document.querySelector('[data-reading-content]');
      if (!root) return false;

      const h2Headings = Array.from(root.querySelectorAll('h2')) as HTMLHeadingElement[];
      const h3Headings = Array.from(root.querySelectorAll('h3')) as HTMLHeadingElement[];
      const headings = h2Headings.length ? h2Headings : h3Headings;
      if (!headings.length) return false;

      const nextSections: GuidedReadingSection[] = headings.map((heading, index) => {
        const title = cleanText(heading.textContent ?? '') || `Section ${index + 1}`;
        const matched = sectionLookup.get(normalize(title));
        const sectionId = matched?.id ?? fallbackSectionId(lessonSlug, index);

        if (!heading.id) {
          heading.id = `guided-heading-${lessonSlug}-${index + 1}`;
        }

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

        const focusPoints = matched?.keyPoints?.length
          ? matched.keyPoints.slice(0, 3)
          : extractFocusPoints(nodes).length
          ? extractFocusPoints(nodes)
          : fallbackFocusPoints(title);

        return {
          id: `${heading.id}-guided`,
          title,
          sectionId,
          focusPoints,
          excerpt: extractExcerpt(nodes, title),
        };
      });

      if (!nextSections.length) return false;

      setReadingSections(nextSections);
      setActiveIndex((prev) => Math.min(prev, Math.max(0, nextSections.length - 1)));
      syncProgress(nextSections);
      return true;
    };

    const attemptHydrate = () => {
      if (cancelled) return;
      const ok = hydrateFromReading();
      if (ok) return;
      attempts += 1;
      if (attempts > 20) {
        setReadingSections([]);
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
  }, [lessonSlug, sectionLookup]);

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

  const goToReading = (title: string) => {
    window.dispatchEvent(
      new CustomEvent('lesson:jump-reading', {
        detail: { title },
      })
    );
  };

  const moveSection = (delta: number) => {
    setActiveIndex((idx) => Math.min(readingSections.length - 1, Math.max(0, idx + delta)));
  };

  const markDone = () => {
    if (!activeSection) return;
    markSectionComplete(lessonSlug, activeSection.sectionId);
    setCompletedMap((prev) => ({ ...prev, [activeSection.sectionId]: true }));
    dispatchSectionSync(lessonSlug);
    if (activeIndex < readingSections.length - 1) {
      setActiveIndex((idx) => idx + 1);
    }
  };

  if (!activeSection) return null;

  const isDone = Boolean(completedMap[activeSection.sectionId]);

  return (
    <div className="guided-root" data-completed={completedCount} data-total={readingSections.length}>
      <div className="guided-head">
        <div>
          <p className="guided-eyebrow">Guided Walkthrough</p>
          <h3>{activeSection.title}</h3>
          <p className="guided-subhead">Step {activeIndex + 1} of {readingSections.length}</p>
        </div>
        <div className="guided-state">
          {completedCount} / {readingSections.length} complete
        </div>
      </div>

      <section className="guided-focus">
        <h4>Focus Points</h4>
        <ul>
          {activeSection.focusPoints.map((point, idx) => (
            <li key={idx}>{point}</li>
          ))}
        </ul>
      </section>

      <section className="guided-excerpt">
        <h4>Quick Read</h4>
        <p>{activeSection.excerpt}</p>
      </section>

      <div className="guided-actions">
        <button type="button" className="guided-btn" onClick={() => moveSection(-1)} disabled={activeIndex === 0}>
          Previous
        </button>
        <button type="button" className="guided-btn" onClick={() => moveSection(1)} disabled={activeIndex === readingSections.length - 1}>
          Next
        </button>
        <button type="button" className="guided-btn is-ghost" onClick={() => goToReading(activeSection.title)}>
          Open reading section
        </button>
        <button type="button" className="guided-btn is-primary" onClick={markDone} disabled={isDone}>
          {isDone ? 'Completed' : 'Mark complete'}
        </button>
      </div>

      <ol className="guided-index" aria-label="Guided section list">
        {readingSections.map((section, index) => {
          const active = index === activeIndex;
          const done = Boolean(completedMap[section.sectionId]);
          return (
            <li key={section.id}>
              <button
                type="button"
                className={`guided-index__item ${active ? 'is-active' : ''} ${done ? 'is-done' : ''}`}
                onClick={() => setActiveIndex(index)}
              >
                <span>{String(index + 1).padStart(2, '0')}</span>
                <span>{section.title}</span>
              </button>
            </li>
          );
        })}
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
          align-items: flex-start;
          gap: var(--space-3);
          flex-wrap: wrap;
        }
        .guided-eyebrow {
          margin: 0 0 var(--space-1);
          text-transform: uppercase;
          letter-spacing: 0.06em;
          font-size: var(--text-xs);
          color: var(--color-text-muted);
        }
        .guided-head h3 {
          margin: 0;
          font-size: var(--text-xl);
          color: var(--color-text);
        }
        .guided-subhead {
          margin: var(--space-1) 0 0;
          color: var(--color-text-muted);
          font-size: var(--text-sm);
        }
        .guided-state {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-pill);
          padding: var(--space-1) var(--space-3);
          color: var(--color-text-muted);
          font-size: var(--text-sm);
          background: var(--color-surface-2);
        }
        .guided-focus,
        .guided-excerpt {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          background: var(--color-surface-2);
          padding: var(--space-3);
        }
        .guided-focus h4,
        .guided-excerpt h4 {
          margin: 0 0 var(--space-2);
          color: var(--color-text);
          font-size: var(--text-base);
        }
        .guided-focus ul {
          margin: 0;
          padding-left: 1.2rem;
          display: grid;
          gap: var(--space-2);
          color: var(--color-text-soft);
        }
        .guided-excerpt p {
          margin: 0;
          color: var(--color-text-soft);
          line-height: var(--leading-normal);
        }
        .guided-actions {
          display: flex;
          gap: var(--space-2);
          flex-wrap: wrap;
        }
        .guided-btn {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-sm);
          background: var(--color-surface-2);
          color: var(--color-text);
          font: inherit;
          font-size: var(--text-sm);
          padding: var(--space-2) var(--space-3);
          cursor: pointer;
        }
        .guided-btn.is-primary {
          color: var(--color-primary);
          border-color: var(--color-primary);
        }
        .guided-btn.is-ghost {
          color: var(--color-primary);
        }
        .guided-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
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
          border-radius: var(--radius-sm);
          background: transparent;
          color: var(--color-text-soft);
          font: inherit;
          padding: var(--space-2) var(--space-3);
          text-align: left;
          display: grid;
          grid-template-columns: auto 1fr;
          gap: var(--space-3);
          cursor: pointer;
        }
        .guided-index__item.is-active {
          border-color: var(--color-primary);
          color: var(--color-text);
        }
        .guided-index__item.is-done {
          border-color: var(--color-accent);
        }
      `}</style>
    </div>
  );
}
