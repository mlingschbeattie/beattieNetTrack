import { useEffect, useMemo, useState } from 'react';
import { getProgress, getTrackProgress } from '../../lib/progressStore';

type SidebarLesson = {
  slug: string;
  title: string;
};

type SidebarSection = {
  title: string;
  lessons: SidebarLesson[];
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
  const lessonSlugs = useMemo(
    () => sections.flatMap((section) => section.lessons.map((lesson) => lesson.slug)),
    [sections]
  );

  useEffect(() => {
    const update = () => {
      const state = getProgress();
      const stats = getTrackProgress(lessonSlugs);
      setProgress(stats);
      setCompletedMap(
        Object.fromEntries(
          Object.entries(state.lessons ?? {})
            .filter(([, entry]) => entry.completed)
            .map(([slug]) => [slug, true])
        )
      );
    };

    update();
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, [lessonSlugs]);

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
          {section.lessons.map((lesson) => {
            const isActive = activeLesson === lesson.slug;
            const isCompleted = Boolean(completedMap[lesson.slug]);
            return (
              <a
                key={lesson.slug}
                className={`sidebar__lesson-link ${isActive ? 'sidebar__lesson-link--active' : ''} ${
                  isCompleted ? 'sidebar__lesson-link--completed' : ''
                }`}
                href={`/lessons/${lesson.slug}`}
              >
                <span className="sidebar__lesson-title">{lesson.title}</span>
                {isCompleted && (
                  <span className="sidebar__lesson-check" aria-hidden="true">
                    ✓
                  </span>
                )}
              </a>
            );
          })}
        </div>
      ))}
    </div>
  );
}
