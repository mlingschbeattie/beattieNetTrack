import { useEffect, useMemo, useState } from 'react';
import { getSectionProgress, markSectionComplete } from '../../lib/progressStore';

interface LessonSection {
  id: string;
  title: string;
  keyPoints: string[];
  check: Array<{ prompt: string; options: string[]; correct: number }>;
}

interface ReadingProgressRailProps {
  lessonSlug: string;
  sections: LessonSection[];
}

type HeadingItem = {
  id: string;
  title: string;
  sectionId: string | null;
};

const dispatchProgress = (lessonSlug: string, completed: number, total: number) => {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(
    new CustomEvent('outline-progress', {
      detail: { lessonSlug, completed, total },
    })
  );
};

const dispatchReadingActiveSection = (lessonSlug: string, item: HeadingItem) => {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(
    new CustomEvent('reading-active-section', {
      detail: {
        lessonSlug,
        headingId: item.id,
        title: item.title,
        sectionId: item.sectionId,
      },
    })
  );
};

const normalize = (value: string) => value.trim().toLowerCase();

export default function ReadingProgressRail({ lessonSlug, sections }: ReadingProgressRailProps) {
  const [headings, setHeadings] = useState<HeadingItem[]>([]);
  const [activeId, setActiveId] = useState<string>('');
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});

  const sectionByTitle = useMemo(() => {
    const map = new Map<string, string>();
    for (const section of sections) {
      map.set(normalize(section.title), section.id);
    }
    return map;
  }, [sections]);

  const syncProgress = () => {
    const progress = getSectionProgress(lessonSlug);
    setCompletedMap(progress);
    const completedCount = sections.filter((s) => progress[s.id]).length;
    dispatchProgress(lessonSlug, completedCount, sections.length);
  };

  useEffect(() => {
    syncProgress();
    const root = document.querySelector('[data-reading-content]');
    if (!root) return;

    const headingEls = Array.from(root.querySelectorAll('h2')) as HTMLHeadingElement[];
    const parsed = headingEls.map((heading, index) => {
      const text = heading.textContent?.trim() || `Section ${index + 1}`;
      const existingId = heading.id?.trim();
      const id = existingId || `lesson-heading-${index + 1}`;
      if (!existingId) heading.id = id;
      return {
        id,
        title: text,
        sectionId: sectionByTitle.get(normalize(text)) ?? null,
      } satisfies HeadingItem;
    });

    setHeadings(parsed);
    if (parsed[0]) {
      setActiveId(parsed[0].id);
      dispatchReadingActiveSection(lessonSlug, parsed[0]);
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
        if (visible[0]?.target instanceof HTMLHeadingElement) {
          const nextId = visible[0].target.id;
          setActiveId(nextId);
          const nextItem = parsed.find((item) => item.id === nextId);
          if (nextItem) {
            dispatchReadingActiveSection(lessonSlug, nextItem);
          }
        }
      },
      {
        rootMargin: '-90px 0px -55% 0px',
        threshold: [0.1, 0.35, 0.6],
      }
    );

    for (const heading of headingEls) {
      observer.observe(heading);
    }

    return () => observer.disconnect();
  }, [lessonSlug, sectionByTitle]);

  useEffect(() => {
    const handler = (event: Event) => {
      const detail = (event as CustomEvent<{ lessonSlug?: string }>).detail;
      if (!detail || detail.lessonSlug !== lessonSlug) return;
      syncProgress();
    };
    window.addEventListener('section-progress-updated', handler);
    return () => window.removeEventListener('section-progress-updated', handler);
  }, [lessonSlug, sections]);

  const markUnderstood = (item: HeadingItem) => {
    if (!item.sectionId) return;
    markSectionComplete(lessonSlug, item.sectionId);
    syncProgress();
    window.dispatchEvent(
      new CustomEvent('section-progress-updated', {
        detail: { lessonSlug },
      })
    );
  };

  const scrollToHeading = (id: string) => {
    const target = document.getElementById(id);
    if (!target) return;
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  if (!headings.length) return null;

  return (
    <aside className="reading-rail">
      <h4>Reading Progress</h4>
      <ol>
        {headings.map((item) => {
          const isActive = item.id === activeId;
          const isDone = item.sectionId ? Boolean(completedMap[item.sectionId]) : false;
          return (
            <li key={item.id} className={isActive ? 'is-active' : ''}>
              <button type="button" className="reading-rail__jump" onClick={() => scrollToHeading(item.id)}>
                {item.title}
              </button>
              {item.sectionId ? (
                <button
                  type="button"
                  className={`reading-rail__mark ${isDone ? 'is-done' : ''}`}
                  onClick={() => markUnderstood(item)}
                  disabled={isDone}
                >
                  {isDone ? 'Understood' : 'Mark understood'}
                </button>
              ) : null}
            </li>
          );
        })}
      </ol>

      <style>{`
        .reading-rail {
          position: sticky;
          top: calc(var(--siteHeaderH) + var(--space-4));
          border: 1px solid var(--color-border);
          background: var(--color-surface);
          border-radius: var(--radius-md);
          padding: var(--space-3);
          display: grid;
          gap: var(--space-2);
        }
        .reading-rail h4 {
          margin: 0;
          font-size: var(--text-sm);
          color: var(--color-text-muted);
          text-transform: uppercase;
          letter-spacing: 0.08em;
        }
        .reading-rail ol {
          list-style: none;
          margin: 0;
          padding: 0;
          display: grid;
          gap: var(--space-2);
        }
        .reading-rail li {
          border-left: 2px solid transparent;
          padding-left: var(--space-2);
          display: grid;
          gap: var(--space-1);
        }
        .reading-rail li.is-active {
          border-left-color: var(--color-primary);
        }
        .reading-rail__jump {
          border: 0;
          background: transparent;
          color: var(--color-text-soft);
          text-align: left;
          font: inherit;
          cursor: pointer;
          padding: 0;
          line-height: var(--leading-normal);
        }
        .reading-rail li.is-active .reading-rail__jump {
          color: var(--color-text);
        }
        .reading-rail__mark {
          width: max-content;
          border: 1px solid var(--color-border);
          border-radius: var(--radius-pill);
          background: var(--color-surface-2);
          color: var(--color-primary);
          font: inherit;
          font-size: var(--text-xs);
          padding: var(--space-1) var(--space-2);
          cursor: pointer;
        }
        .reading-rail__mark.is-done {
          color: var(--color-accent);
          border-color: var(--color-accent);
        }
        .reading-rail__mark:disabled {
          cursor: default;
        }
      `}</style>
    </aside>
  );
}
