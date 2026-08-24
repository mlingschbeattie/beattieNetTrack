import { useEffect, useMemo, useRef, useState } from 'react';
import {
  getGuidedPreferences,
  getSectionProgress,
  markSectionComplete,
  setGuidedPreferences,
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

type NarrationState = 'idle' | 'playing' | 'paused' | 'unsupported';

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
  const [revealedCount, setRevealedCount] = useState<Record<string, number>>({});
  const [autoReveal, setAutoReveal] = useState(false);
  const [autoRevealPaused, setAutoRevealPaused] = useState(false);
  const [autoSeconds, setAutoSeconds] = useState(5);
  const [syncWithReading, setSyncWithReading] = useState(true);
  const [narrationRate, setNarrationRate] = useState(1);
  const [narrationState, setNarrationState] = useState<NarrationState>('idle');
  const [liveMessage, setLiveMessage] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const lastManualChangeAtRef = useRef(0);

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
    const prefs = getGuidedPreferences();
    setAutoReveal(prefs.autoReveal);
    setAutoSeconds(prefs.autoSeconds);
    setSyncWithReading(prefs.syncWithReading);
    setNarrationRate(prefs.narrationRate);
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setNarrationState('unsupported');
    }
  }, []);

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
      setRevealedCount((prev) => {
        const next: Record<string, number> = {};
        for (const section of nextSections) {
          next[section.id] = Math.max(1, prev[section.id] ?? 1);
        }
        return next;
      });
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

    return () => {
      cancelled = true;
      if (retryTimer !== null) window.clearTimeout(retryTimer);
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

  useEffect(() => {
    if (!activeSection) return;
    setLiveMessage(`Step ${activeIndex + 1} of ${readingSections.length}: ${activeSection.title}`);
    setRevealedCount((prev) => ({
      ...prev,
      [activeSection.id]: Math.max(1, prev[activeSection.id] ?? 1),
    }));
  }, [activeIndex, activeSection, readingSections.length]);

  useEffect(() => {
    if (!activeSection || !autoReveal || autoRevealPaused) return;
    const totalBlocks = Math.max(1, activeSection.focusPoints.length + 1);
    const currentReveal = Math.max(1, revealedCount[activeSection.id] ?? 1);
    if (currentReveal >= totalBlocks) return;

    const timer = window.setTimeout(() => {
      setRevealedCount((prev) => ({
        ...prev,
        [activeSection.id]: Math.min(totalBlocks, (prev[activeSection.id] ?? 1) + 1),
      }));
    }, autoSeconds * 1000);

    return () => window.clearTimeout(timer);
  }, [autoReveal, autoRevealPaused, autoSeconds, activeSection, revealedCount]);

  useEffect(() => {
    if (!activeSection || !autoReveal || autoRevealPaused) return;
    const totalBlocks = Math.max(1, activeSection.focusPoints.length + 1);
    const currentReveal = Math.max(1, revealedCount[activeSection.id] ?? 1);
    if (currentReveal < totalBlocks) return;
    if (activeIndex >= readingSections.length - 1) return;

    const advanceTimer = window.setTimeout(() => {
      lastManualChangeAtRef.current = Date.now();
      setActiveIndex((idx) => Math.min(readingSections.length - 1, idx + 1));
    }, autoSeconds * 1000);

    return () => window.clearTimeout(advanceTimer);
  }, [autoReveal, autoRevealPaused, autoSeconds, activeSection, revealedCount, activeIndex, readingSections.length]);

  useEffect(() => {
    setGuidedPreferences({ autoReveal });
  }, [autoReveal]);

  useEffect(() => {
    setGuidedPreferences({ autoSeconds });
  }, [autoSeconds]);

  useEffect(() => {
    setGuidedPreferences({ syncWithReading });
  }, [syncWithReading]);

  useEffect(() => {
    setGuidedPreferences({ narrationRate });
  }, [narrationRate]);

  useEffect(() => {
    return () => {
      if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      utteranceRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    utteranceRef.current = null;
    if (narrationState !== 'unsupported') {
      setNarrationState('idle');
    }
  }, [activeIndex]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (!event.altKey || event.key.toLowerCase() !== 'p') return;
      event.preventDefault();
      if (narrationState === 'playing' || narrationState === 'paused') {
        if (!('speechSynthesis' in window)) return;
        if (narrationState === 'playing') {
          window.speechSynthesis.pause();
          setNarrationState('paused');
          setLiveMessage('Narration paused.');
          return;
        }
        window.speechSynthesis.resume();
        setNarrationState('playing');
        setLiveMessage('Narration resumed.');
        return;
      }
      if (narrationState !== 'unsupported') {
        startNarration();
      }
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [narrationState, activeSection, narrationRate]);

  useEffect(() => {
    const handler = (
      event: Event
    ) => {
      if (!syncWithReading) return;
      const detail = (event as CustomEvent<{
        lessonSlug?: string;
        headingId?: string;
        title?: string;
        sectionId?: string | null;
      }>).detail;
      if (!detail || detail.lessonSlug !== lessonSlug) return;

      const now = Date.now();
      if (now - lastManualChangeAtRef.current < 1500) return;

      let nextIndex = -1;
      if (typeof detail.sectionId === 'string' && detail.sectionId) {
        nextIndex = readingSections.findIndex((section) => section.sectionId === detail.sectionId);
      }

      if (nextIndex < 0 && typeof detail.headingId === 'string' && detail.headingId) {
        nextIndex = readingSections.findIndex(
          (section) => section.id === `${detail.headingId}-guided`
        );
      }

      if (nextIndex < 0 && typeof detail.title === 'string' && detail.title) {
        const normalizedTitle = normalize(detail.title);
        nextIndex = readingSections.findIndex((section) => normalize(section.title) === normalizedTitle);
      }

      if (nextIndex >= 0 && nextIndex !== activeIndex) {
        setActiveIndex(nextIndex);
      }
    };

    window.addEventListener('reading-active-section', handler);
    return () => window.removeEventListener('reading-active-section', handler);
  }, [lessonSlug, readingSections, activeIndex, syncWithReading]);

  const completedCount = useMemo(
    () => readingSections.filter((section) => completedMap[section.sectionId]).length,
    [readingSections, completedMap]
  );

  const totalRevealBlocks = Math.max(1, (activeSection?.focusPoints.length ?? 0) + 1);
  const revealedBlocks = activeSection ? Math.max(1, revealedCount[activeSection.id] ?? 1) : 1;
  const visibleFocusCount = activeSection
    ? Math.min(activeSection.focusPoints.length, revealedBlocks)
    : 0;
  const showExcerpt = activeSection
    ? activeSection.focusPoints.length === 0 || revealedBlocks > activeSection.focusPoints.length
    : true;

  const stopNarration = () => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    utteranceRef.current = null;
    if (narrationState !== 'unsupported') {
      setNarrationState('idle');
      setLiveMessage('Narration stopped.');
    }
  };

  const startNarration = () => {
    if (!activeSection) return;
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setNarrationState('unsupported');
      setLiveMessage('Narration is not supported in this browser.');
      return;
    }

    const text = [
      activeSection.title,
      `Focus points. ${activeSection.focusPoints.join('. ')}`,
      `Quick read. ${activeSection.excerpt}`,
    ].join('. ');

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = narrationRate;
    utterance.onend = () => {
      utteranceRef.current = null;
      setNarrationState('idle');
      setLiveMessage('Narration complete.');
    };
    utterance.onerror = () => {
      utteranceRef.current = null;
      setNarrationState('idle');
      setLiveMessage('Narration stopped due to an audio error.');
    };

    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
    setNarrationState('playing');
    setLiveMessage(`Narration started for ${activeSection.title}.`);
  };

  const toggleNarration = () => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setNarrationState('unsupported');
      setLiveMessage('Narration is not supported in this browser.');
      return;
    }

    if (narrationState === 'playing') {
      window.speechSynthesis.pause();
      setNarrationState('paused');
      setLiveMessage('Narration paused.');
      return;
    }

    if (narrationState === 'paused') {
      window.speechSynthesis.resume();
      setNarrationState('playing');
      setLiveMessage('Narration resumed.');
      return;
    }

    startNarration();
  };

  const goToReading = (title: string) => {
    stopNarration();
    lastManualChangeAtRef.current = Date.now();
    window.dispatchEvent(
      new CustomEvent('lesson:jump-reading', {
        detail: { title },
      })
    );
  };

  const moveSection = (delta: number) => {
    stopNarration();
    lastManualChangeAtRef.current = Date.now();
    setActiveIndex((idx) => Math.min(readingSections.length - 1, Math.max(0, idx + delta)));
  };

  const revealNext = () => {
    if (!activeSection) return;
    setRevealedCount((prev) => ({
      ...prev,
      [activeSection.id]: Math.min(totalRevealBlocks, (prev[activeSection.id] ?? 1) + 1),
    }));
  };

  const revealFull = () => {
    if (!activeSection) return;
    setRevealedCount((prev) => ({
      ...prev,
      [activeSection.id]: totalRevealBlocks,
    }));
  };

  const markDone = () => {
    if (!activeSection) return;
    lastManualChangeAtRef.current = Date.now();
    markSectionComplete(lessonSlug, activeSection.sectionId);
    setCompletedMap((prev) => ({ ...prev, [activeSection.sectionId]: true }));
    dispatchSectionSync(lessonSlug);
    if (activeIndex < readingSections.length - 1) {
      setActiveIndex((idx) => idx + 1);
    }
    setLiveMessage('Section marked complete.');
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
        <div className="guided-head-right">
          <button
            type="button"
            className={`guided-settings-toggle ${showSettings ? 'is-open' : ''}`}
            onClick={() => setShowSettings((s) => !s)}
            aria-expanded={showSettings}
            aria-controls="guided-settings-panel"
            aria-label="Settings"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M6.5 1L7 3l-1.3.8L4 2.5 2.5 4l1.3 1.7L3 7l-2 .5v2L3 10l.8 1.3L2.5 13 4 14.5l1.7-1.3L7 14l.5 2h2l.5-2 1.3-.8 1.7 1.3L14.5 13l-1.3-1.7L14 10l2-.5v-2L14 7l-.8-1.3L14.5 4 13 2.5l-1.7 1.3L10 3l-.5-2h-2zM8 5.5a2.5 2.5 0 110 5 2.5 2.5 0 010-5z"
                stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round" />
            </svg>
          </button>
          <div className="guided-state">
            {completedCount} / {readingSections.length}
          </div>
        </div>
      </div>

      {showSettings && (
        <div className="guided-settings" id="guided-settings-panel" role="group" aria-label="Guided view settings">
          <fieldset className="guided-settings-group">
            <legend>Pacing</legend>
            <label className="guided-control">
              <input
                type="checkbox"
                checked={autoReveal}
                onChange={(event) => {
                  setAutoReveal(event.target.checked);
                  setAutoRevealPaused(false);
                }}
              />
              <span>Auto reveal & advance</span>
            </label>
            <label className="guided-control">
              <input
                type="checkbox"
                checked={syncWithReading}
                onChange={(event) => setSyncWithReading(event.target.checked)}
              />
              <span>Sync with reading</span>
            </label>
          </fieldset>
          <fieldset className="guided-settings-group">
            <legend>Narration</legend>
            <button
              type="button"
              className="guided-btn guided-btn--sm"
              onClick={toggleNarration}
              disabled={narrationState === 'unsupported'}
              aria-keyshortcuts="Alt+P"
              aria-pressed={narrationState === 'playing' || narrationState === 'paused'}
              aria-label={
                narrationState === 'playing'
                  ? 'Pause narration'
                  : narrationState === 'paused'
                  ? 'Resume narration'
                  : 'Play narration'
              }
            >
              {narrationState === 'playing' ? 'Pause' : narrationState === 'paused' ? 'Resume' : 'Play'}
            </button>
            {(narrationState === 'playing' || narrationState === 'paused') && (
              <button type="button" className="guided-btn guided-btn--sm" onClick={stopNarration}>
                Stop
              </button>
            )}
            <label className="guided-control">
              Speed
              <select
                className="guided-select"
                value={String(narrationRate)}
                onChange={(event) => setNarrationRate(Number(event.target.value))}
                aria-label="Narration speed"
              >
                <option value="0.9">0.9x</option>
                <option value="1">1.0x</option>
                <option value="1.15">1.15x</option>
                <option value="1.3">1.3x</option>
              </select>
            </label>
          </fieldset>
        </div>
      )}

      {autoReveal && (
        <div className="guided-transport" aria-label="Auto-reveal controls">
          <button
            type="button"
            className="guided-transport__btn"
            onClick={() => setAutoRevealPaused((p) => !p)}
            aria-label={autoRevealPaused ? 'Resume auto-reveal' : 'Pause auto-reveal'}
          >
            {autoRevealPaused ? '▶' : '⏸'}
          </button>
          <select
            className="guided-select"
            value={autoSeconds}
            onChange={(event) => setAutoSeconds(Number(event.target.value))}
            aria-label="Auto reveal pace"
          >
            <option value={3}>Fast</option>
            <option value={5}>Normal</option>
            <option value={7}>Slow</option>
          </select>
          <div className="guided-transport__track">
            <div
              className="guided-transport__fill"
              style={{ width: `${(revealedBlocks / totalRevealBlocks) * 100}%` }}
            />
          </div>
          <span className="guided-transport__count">{revealedBlocks}/{totalRevealBlocks}</span>
        </div>
      )}

      <section className="guided-focus">
        <h4>Focus Points</h4>
        <ul>
          {activeSection.focusPoints.slice(0, visibleFocusCount).map((point, idx) => (
            <li key={idx}>{point}</li>
          ))}
        </ul>
      </section>

      <section className="guided-excerpt">
        <h4>Quick Read</h4>
        <p>{showExcerpt ? activeSection.excerpt : 'Show more to read this section.'}</p>
      </section>

      <div className="guided-actions">
        <button type="button" className="guided-btn" onClick={() => moveSection(-1)} disabled={activeIndex === 0}>
          Previous
        </button>
        <button type="button" className="guided-btn" onClick={() => moveSection(1)} disabled={activeIndex === readingSections.length - 1}>
          Next
        </button>
        {!autoReveal && revealedBlocks < totalRevealBlocks && (
          <button type="button" className="guided-btn" onClick={revealNext}>
            Reveal next
          </button>
        )}
        {!autoReveal && revealedBlocks < totalRevealBlocks && (
          <button type="button" className="guided-btn" onClick={revealFull}>
            Reveal all
          </button>
        )}
        <button type="button" className="guided-btn is-ghost" onClick={() => goToReading(activeSection.title)}>
          Open in reading
        </button>
        <button type="button" className="guided-btn is-primary" onClick={markDone} disabled={isDone}>
          {isDone ? 'Completed' : 'Mark complete'}
        </button>
      </div>

      <p className="sr-only" role="status" aria-live="polite" aria-atomic="true">{liveMessage}</p>

      <ol className="guided-index" aria-label="Guided section list">
        {readingSections.map((section, index) => {
          const active = index === activeIndex;
          const done = Boolean(completedMap[section.sectionId]);
          return (
            <li key={section.id}>
              <button
                type="button"
                className={`guided-index__item ${active ? 'is-active' : ''} ${done ? 'is-done' : ''}`}
                onClick={() => {
                  lastManualChangeAtRef.current = Date.now();
                  setActiveIndex(index);
                }}
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
          gap: var(--space-3);
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
        .guided-head-right {
          display: flex;
          align-items: center;
          gap: var(--space-2);
        }
        .guided-settings-toggle {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          border: 1px solid var(--color-border);
          border-radius: var(--radius-sm);
          background: var(--color-surface-2);
          color: var(--color-text-muted);
          cursor: pointer;
          transition: color 0.15s, border-color 0.15s;
        }
        .guided-settings-toggle:hover,
        .guided-settings-toggle.is-open {
          color: var(--color-primary);
          border-color: var(--color-primary);
        }
        .guided-state {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-pill);
          padding: var(--space-1) var(--space-3);
          color: var(--color-text-muted);
          font-size: var(--text-sm);
          background: var(--color-surface-2);
          white-space: nowrap;
        }
        .guided-settings {
          display: flex;
          gap: var(--space-3);
          flex-wrap: wrap;
          border: 1px solid var(--color-border);
          border-radius: var(--radius-sm);
          background: var(--color-surface-2);
          padding: var(--space-3);
        }
        .guided-settings-group {
          display: flex;
          align-items: center;
          gap: var(--space-3);
          flex-wrap: wrap;
          border: none;
          margin: 0;
          padding: 0;
        }
        .guided-settings-group legend {
          font-size: var(--text-xs);
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--color-text-muted);
          margin-bottom: var(--space-1);
        }
        .guided-transport {
          display: flex;
          align-items: center;
          gap: var(--space-2);
        }
        .guided-transport__btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 28px;
          height: 28px;
          border: 1px solid var(--color-border);
          border-radius: var(--radius-sm);
          background: var(--color-surface-2);
          color: var(--color-text);
          font-size: var(--text-sm);
          cursor: pointer;
          flex-shrink: 0;
        }
        .guided-transport__btn:hover {
          border-color: var(--color-primary);
          color: var(--color-primary);
        }
        .guided-transport__track {
          flex: 1;
          height: 6px;
          border-radius: 3px;
          background: var(--color-surface-2);
          overflow: hidden;
          position: relative;
          min-width: 60px;
        }
        .guided-transport__fill {
          position: absolute;
          inset: 0;
          width: 0;
          background: var(--color-primary);
          border-radius: 3px;
          transition: width 0.4s ease;
        }
        .guided-transport__count {
          color: var(--color-text-muted);
          font-size: var(--text-xs);
          white-space: nowrap;
          flex-shrink: 0;
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
        .guided-control {
          display: inline-flex;
          align-items: center;
          gap: var(--space-2);
          color: var(--color-text-soft);
          font-size: var(--text-sm);
        }
        .guided-select {
          border: 1px solid var(--color-border);
          border-radius: var(--radius-sm);
          background: var(--color-surface);
          color: var(--color-text);
          font: inherit;
          font-size: var(--text-sm);
          padding: var(--space-1) var(--space-2);
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
        .guided-btn--sm {
          padding: var(--space-1) var(--space-2);
          font-size: var(--text-xs);
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
        .guided-btn:focus-visible,
        .guided-select:focus-visible,
        .guided-index__item:focus-visible,
        .guided-settings-toggle:focus-visible,
        .guided-control input:focus-visible {
          outline: 2px solid rgba(56, 189, 248, 0.55);
          outline-offset: 2px;
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
