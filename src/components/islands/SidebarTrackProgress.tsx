import { useEffect, useMemo, useState } from 'react';
import { getProgress, getTrackProgress } from '../../lib/progressStore';

type SidebarItem = {
  slug: string;
  title: string;
  type?: 'lesson' | 'lab' | 'quiz' | 'activity';
  href?: string;
};

type SidebarSection = {
  title: string;
  lessons: SidebarItem[];
};

type SidebarTrackProgressProps = {
  sections: SidebarSection[];
  activeLesson?: string;
};

type TrackProgress = ReturnType<typeof getTrackProgress>;

export default function SidebarTrackProgress({ sections, activeLesson }: SidebarTrackProgressProps) {
  const [progress, setProgress] = useState<TrackProgress>({
    percent: 0,
    completed: 0,
    total: 0,
    xpEarned: 0,
  });
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});
  const [displayPct, setDisplayPct] = useState(0);
  const itemSlugs = useMemo(
    () => sections.flatMap((section) => (section.lessons || []).map((item) => item.slug)),
    [sections]
  );

  useEffect(() => {
    // Immediately signal readiness to the page shell upon hydration
    if (typeof document !== 'undefined') {
      document.documentElement.classList.add('sidebar-ready');
    }

    const update = () => {
      const state = getProgress();
      const stats = getTrackProgress(itemSlugs);
      setProgress(stats);

      const map: Record<string, boolean> = {};
      for (const [slug, entry] of Object.entries(state.lessons ?? {})) {
        if (entry.completed) {
          const sectionChecks = state.lessonSections?.[slug];
          if (sectionChecks && Object.keys(sectionChecks).length > 0) {
            const isComplete = Object.values(sectionChecks).every(Boolean);
            map[`lesson:${slug}`] = isComplete;
          } else {
            map[`lesson:${slug}`] = true;
          }
        }
      }
      for (const [slug, entry] of Object.entries(state.labs ?? {})) {
        if (entry.completed) {
          map[`lab:${slug}`] = true;
          map[`activity:${slug}`] = true;
        }
      }
      for (const [slug, entry] of Object.entries(state.quizzes ?? {})) {
        if ((entry.bestScore ?? 0) >= 70) {
          map[`quiz:${slug}`] = true;
        }
      }
      setCompletedMap(map);
    };

    update();
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, [itemSlugs]);

  useEffect(() => {
    const t = setTimeout(() => setDisplayPct(progress.percent), 100);
    return () => clearTimeout(t);
  }, [progress.percent]);

  // Section gating: Section 0 is always unlocked. Section i (i >= 1) unlocks when section i-1 has >= 80% completion.
  const sectionStats = sections.map((sec) => {
    const items = sec.lessons || [];
    const total = items.length;
    const completed = items.filter((item) => {
      const key = `${item.type ?? 'lesson'}:${item.slug}`;
      return Boolean(completedMap[key]);
    }).length;
    const isPassing = total === 0 || (completed / total) >= 0.8;
    return { total, completed, isPassing };
  });

  const isUnlockedList: boolean[] = [];
  for (let i = 0; i < sections.length; i++) {
    if (i === 0) {
      isUnlockedList.push(true);
    } else {
      const prev = sectionStats[i - 1];
      isUnlockedList.push(Boolean(prev && prev.isPassing));
    }
  }

  return (
    <div className="sidebar-progress">
      <div className="sidebar-progress__row">
        <span>{progress.completed}/{progress.total} done</span>
        <span className="xp-display">
          <span className="xp-display__icon">⚡</span>
          <span className="xp-display__value" style={{ fontSize: '13px' }}>{progress.xpEarned}</span>
          <span className="xp-display__label">XP</span>
        </span>
      </div>
      <div className="progress-bar-track" aria-hidden="true">
        <div className="progress-bar-fill" style={{ width: `${displayPct}%` }}></div>
      </div>
      {sections.map((section, index) => {
        const isUnlocked = isUnlockedList[index];

        return (
          <div className={`sidebar__group ${!isUnlocked ? 'sidebar__group--locked' : ''}`} key={section.title}>
            <div className="sidebar__group-title" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span>{section.title}</span>
              {!isUnlocked && <span title="Section locked" aria-hidden="true">🔒</span>}
            </div>
            {(!section.lessons || section.lessons.length === 0) ? (
              <div className="sidebar__empty-group" style={{ padding: '4px 8px', fontSize: '12px', opacity: 0.5 }}>
                No activities in section
              </div>
            ) : (
              section.lessons.map((item) => {
                const isActive = activeLesson === item.slug;
                const key = `${item.type ?? 'lesson'}:${item.slug}`;
                const isCompleted = Boolean(completedMap[key]);
                const href = item.href || (item.type === 'lab' ? `/labs/${item.slug}` : item.type === 'quiz' ? `/quizzes/${item.slug}` : `/lessons/${item.slug}`);

                if (!isUnlocked) {
                  return (
                    <span
                      key={item.slug}
                      className="sidebar__lesson-link sidebar__lesson-link--locked"
                      aria-disabled="true"
                      role="link"
                      tabIndex={0}
                      aria-label={`Locked: ${item.title} — Complete previous section to unlock`}
                    >
                      <span className="sidebar__lesson-title">{item.title}</span>
                      <span style={{ fontSize: '11px', opacity: 0.7 }} aria-hidden="true">🔒</span>
                    </span>
                  );
                }

                return (
                  <a
                    key={item.slug}
                    className={`sidebar__lesson-link ${isActive ? 'sidebar__lesson-link--active' : ''} ${
                      isCompleted ? 'sidebar__lesson-link--completed' : ''
                    }`}
                    href={href}
                  >
                    <span className="sidebar__lesson-title">{item.title}</span>
                    {isCompleted && (
                      <span className="sidebar__lesson-check" aria-hidden="true">
                        ✓
                      </span>
                    )}
                  </a>
                );
              })
            )}
          </div>
        );
      })}
    </div>
  );
}
