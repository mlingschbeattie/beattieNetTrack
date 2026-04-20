import { useEffect, useState } from 'react';
import { getProgress } from '../../lib/progressStore';

type TrackMeta = { slug: string; title: string; activityCount: number };
type ActivityItem = { type: string; slug: string };

interface Props {
  tracks: TrackMeta[];
  activityMap: Record<string, ActivityItem[]>;
}

type ActiveTrack = TrackMeta & { completed: number };

export default function ContinueLearning({ tracks, activityMap }: Props) {
  const [isMounted, setIsMounted] = useState(false);
  const [active, setActive] = useState<ActiveTrack | null>(null);

  useEffect(() => {
    const progress = getProgress();
    let best: ActiveTrack | null = null;

    for (const track of tracks) {
      const activities = activityMap[track.slug] ?? [];
      const completed = activities.filter(({ type, slug }) => {
        const col = type === 'lab' ? 'labs' : type === 'quiz' ? 'quizzes' : 'lessons';
        return Boolean(
          (progress[col as 'labs' | 'quizzes' | 'lessons'] as Record<string, { completed?: boolean }>)?.[slug]
            ?.completed
        );
      }).length;
      if (!best || completed > best.completed) {
        best = { ...track, completed };
      }
    }

    setActive(best ?? (tracks[0] ? { ...tracks[0], completed: 0 } : null));
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return (
      <div
        className="progress-status-skeleton"
        style={{ height: '140px', borderRadius: '12px', width: '100%', alignItems: 'center', justifyContent: 'center' }}
      >
        <div className="progress-status-skeleton__pill" style={{ width: '60%', height: '20px' }} />
      </div>
    );
  }

  if (!active) return null;

  const isNew = active.completed === 0;
  const pct = active.activityCount > 0 ? Math.round((active.completed / active.activityCount) * 100) : 0;

  return (
    <article className="card card--track">
      <span className={`track-badge track-badge--${isNew ? 'available' : 'in-progress'}`}>
        {isNew ? 'Start Here' : 'In Progress'}
      </span>
      <h3>{active.title}</h3>
      <p>
        {active.completed} of {active.activityCount} activities complete
      </p>
      {!isNew && (
        <div className="progress-bar-track">
          <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
        </div>
      )}
      <div className="card__footer">
        <a className="card__cta" href={`/tracks/${active.slug}`}>
          {isNew ? 'Start →' : 'Continue →'}
        </a>
      </div>
    </article>
  );
}
