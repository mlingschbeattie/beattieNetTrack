import { useEffect, useMemo, useState } from 'react';
import { getProgress, getTrackProgress } from '../../lib/progressStore';

type SidebarItem = {
  slug: string;
  title: string;
  type?: 'lesson' | 'lab' | 'quiz';
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
        if (entry.completed) map[slug] = true;
      }
      for (const [slug, entry] of Object.entries(state.labs ?? {})) {
        if (entry.completed) map[slug] = true;
      }
      for (const [slug, entry] of Object.entries(state.quizzes ?? {})) {
        if ((entry.bestScore ?? 0) >= 80) map[slug] = true;
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
      {sections.map((section) => (
        <div className="sidebar__group" key={section.title}>
          <div className="sidebar__group-title">{section.title}</div>
          {(!section.lessons || section.lessons.length === 0) ? (
            <div className="sidebar__empty-group" style={{ padding: '4px 8px', fontSize: '12px', opacity: 0.5 }}>
              No activities in section
            </div>
          ) : (
            section.lessons.map((item) => {
              const isActive = activeLesson === item.slug;
              const isCompleted = Boolean(completedMap[item.slug]);
              const href = item.href || (item.type === 'lab' ? `/labs/${item.slug}` : item.type === 'quiz' ? `/quizzes/${item.slug}` : `/lessons/${item.slug}`);
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
      ))}
    </div>
  );
}
