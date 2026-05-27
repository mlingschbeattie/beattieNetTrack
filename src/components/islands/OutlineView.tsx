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

interface OutlineViewProps {
  lessonSlug: string;
  sections: LessonSection[];
}

const normalize = (value: string) => value.trim().toLowerCase();

const cleanText = (value: string) => value.replace(/\s+/g, ' ').trim();

const truncatePoint = (value: string, max = 130) => {
  if (value.length <= max) return value;
  return `${value.slice(0, max - 1).trimEnd()}...`;
};

const fallbackKeyPoints = (title: string): string[] => [
  `${title}: identify the core concept and where to use it during troubleshooting.`,
  'Pay attention to visual identifiers, connectors, and common mistakes.',
  'Use this section as a quick-reference map before jumping into details.',
];

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

    const definitionMatch = paragraph.match(/^([^.!?]{3,80})(?:\s+[\-:]\s+)(.+)$/);
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
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});
  const [query, setQuery] = useState('');

  const total = displaySections.length;

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

        return {
          id: authored?.id ?? `outline-${lessonSlug}-${index + 1}`,
          title,
          keyPoints,
          check: authored?.check ?? [],
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

    return () => {
      cancelled = true;
      if (retryTimer !== null) window.clearTimeout(retryTimer);
    };
  }, [lessonSlug, sections]);

  const syncProgress = () => {
    const progress = getSectionProgress(lessonSlug);
    setCompletedMap(progress);
    const completedCount = displaySections.filter((section) => progress[section.id]).length;
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
    () => displaySections.filter((section) => completedMap[section.id]).length,
    [displaySections, completedMap]
  );

  const filteredSections = useMemo(() => {
    const needle = normalize(query);
    if (!needle) return displaySections;
    return displaySections.filter((section) => {
      const text = normalize([section.title, ...section.keyPoints].join(' '));
      return text.includes(needle);
    });
  }, [query, displaySections]);

  const markDone = (sectionId: string) => {
    markSectionComplete(lessonSlug, sectionId);
    setCompletedMap((prev) => ({ ...prev, [sectionId]: true }));
    dispatchSectionSync(lessonSlug);
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
      <div className="outline-tools">
        <label className="outline-search" htmlFor={`outline-search-${lessonSlug}`}>
          <span>Search outline</span>
          <input
            id={`outline-search-${lessonSlug}`}
            type="search"
            placeholder="Filter section titles and key points"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </label>
        <div className="outline-meta">{completedCount} / {total} complete</div>
      </div>

      <ol className="outline-list">
        {filteredSections.map((section, index) => {
          const isDone = Boolean(completedMap[section.id]);
          return (
            <li key={section.id} className={`outline-item ${isDone ? 'is-done' : ''}`}>
              <div className="outline-head">
                <div className="outline-title-wrap">
                  <span className="outline-num">{String(index + 1).padStart(2, '0')}</span>
                  <h3>{section.title}</h3>
                </div>
                <span className={`outline-state ${isDone ? 'is-done' : 'is-open'}`}>
                  {isDone ? 'Done' : 'Open'}
                </span>
              </div>

              <ul className="outline-points">
                {section.keyPoints.map((point, i) => (
                  <li key={i}>{point}</li>
                ))}
              </ul>

              <div className="outline-actions">
                <button type="button" className="outline-btn is-ghost" onClick={() => jumpToReading(section.title)}>
                  Jump to reading
                </button>
                <button
                  type="button"
                  className="outline-btn is-primary"
                  onClick={() => markDone(section.id)}
                  disabled={isDone}
                >
                  {isDone ? 'Marked complete' : 'Mark complete'}
                </button>
              </div>
            </li>
          );
        })}
      </ol>

      {filteredSections.length === 0 ? (
        <div className="outline-empty">No sections match that search.</div>
      ) : null}

      <style>{`
        .outline-root {
          display: grid;
          gap: var(--space-4);
        }
        .outline-tools {
          display: flex;
          justify-content: space-between;
          gap: var(--space-3);
          flex-wrap: wrap;
          align-items: end;
        }
        .outline-search {
          display: grid;
          gap: var(--space-1);
          color: var(--color-text-muted);
          font-size: var(--text-xs);
          text-transform: uppercase;
          letter-spacing: 0.05em;
          min-width: min(520px, 100%);
        }
        .outline-search input {
          border: 1px solid var(--color-border);
          background: var(--color-surface);
          border-radius: var(--radius-sm);
          color: var(--color-text);
          font: inherit;
          font-size: var(--text-sm);
          padding: var(--space-2) var(--space-3);
        }
        .outline-meta {
          color: var(--color-text-muted);
          font-size: var(--text-sm);
          white-space: nowrap;
        }
        .outline-list {
          list-style: none;
          margin: 0;
          padding: 0;
          display: grid;
          gap: var(--space-3);
        }
        .outline-item {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-md);
          background: var(--color-surface);
          padding: var(--space-4);
          display: grid;
          gap: var(--space-3);
        }
        .outline-item.is-done {
          border-color: var(--color-accent);
        }
        .outline-head {
          display: flex;
          justify-content: space-between;
          gap: var(--space-3);
          align-items: flex-start;
          flex-wrap: wrap;
        }
        .outline-title-wrap {
          display: flex;
          align-items: baseline;
          gap: var(--space-3);
          min-width: 0;
        }
        .outline-title-wrap h3 {
          margin: 0;
          color: var(--color-text);
          font-size: var(--text-lg);
        }
        .outline-num {
          font-family: var(--font-mono);
          color: var(--color-text-muted);
          font-size: var(--text-sm);
        }
        .outline-state {
          border-radius: var(--radius-pill);
          border: 1px solid var(--color-border);
          padding: var(--space-1) var(--space-3);
          font-size: var(--text-xs);
          color: var(--color-text-muted);
          background: var(--color-surface-2);
        }
        .outline-state.is-done {
          border-color: var(--color-accent);
          color: var(--color-accent);
        }
        .outline-points {
          margin: 0;
          padding-left: 1.2rem;
          display: grid;
          gap: var(--space-2);
          color: var(--color-text-soft);
          line-height: var(--leading-normal);
        }
        .outline-actions {
          display: flex;
          gap: var(--space-2);
          flex-wrap: wrap;
        }
        .outline-btn {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-sm);
          background: var(--color-surface-2);
          color: var(--color-text);
          font: inherit;
          font-size: var(--text-sm);
          padding: var(--space-2) var(--space-3);
          cursor: pointer;
        }
        .outline-btn:disabled {
          cursor: not-allowed;
          opacity: 0.6;
        }
        .outline-btn.is-primary {
          border-color: var(--color-primary);
          color: var(--color-primary);
        }
        .outline-btn.is-ghost:hover:not(:disabled),
        .outline-btn.is-primary:hover:not(:disabled) {
          border-color: var(--color-primary);
        }
        .outline-empty {
          border: 1px dashed var(--color-border);
          border-radius: var(--radius-md);
          color: var(--color-text-muted);
          padding: var(--space-4);
        }
      `}</style>
    </div>
  );
}
