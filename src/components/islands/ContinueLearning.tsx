import { useEffect, useMemo, useState } from 'react';
import { PROGRESS_KEY } from '../../lib/progressStore';

type TrackMeta = {
  slug: string;
  title: string;
  activityCount: number;
};

type ActivityMeta = {
  type: 'lesson' | 'lab' | 'quiz';
  slug: string;
};

type ContinueLearningProps = {
  tracks?: TrackMeta[];
  activityMap?: Record<string, ActivityMeta[]>;
};

type ProgressState = {
  lessons?: Record<string, { completed?: boolean; completedAt?: string | null }>;
  labs?: Record<string, { completed?: boolean; completedAt?: string | null }>;
  quizzes?: Record<string, { attempts?: number; lastAttemptAt?: string | null }>;
};

type TouchedActivity = {
  slug: string;
  type: ActivityMeta['type'];
  touchedAt: string;
};

type Recommendation = {
  track: TrackMeta;
  activity: ActivityMeta;
  lastTouched: TouchedActivity | null;
};

const activityHref = (activity: ActivityMeta) => {
  if (activity.type === 'lab') return `/labs/${activity.slug}`;
  if (activity.type === 'quiz') return `/quizzes/${activity.slug}`;
  return `/lessons/${activity.slug}`;
};

const humanizeSlug = (value: string) =>
  value
    .replace(/[-_]+/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase());

const isCompleted = (state: ProgressState | null, activity: ActivityMeta) => {
  if (!state) return false;
  if (activity.type === 'lesson') return Boolean(state.lessons?.[activity.slug]?.completed);
  if (activity.type === 'lab') return Boolean(state.labs?.[activity.slug]?.completed);
  return Boolean((state.quizzes?.[activity.slug]?.attempts ?? 0) > 0);
};

const findRecommendation = (
  tracks: TrackMeta[],
  activityMap: Record<string, ActivityMeta[]>,
  state: ProgressState | null
): Recommendation | null => {
  const availableTracks = tracks.filter((track) => (activityMap[track.slug]?.length ?? 0) > 0);
  if (!availableTracks.length) return null;

  const touched: TouchedActivity[] = [];
  for (const [slug, entry] of Object.entries(state?.lessons ?? {})) {
    if (entry?.completed && entry.completedAt) {
      touched.push({ slug, type: 'lesson', touchedAt: entry.completedAt });
    }
  }
  for (const [slug, entry] of Object.entries(state?.labs ?? {})) {
    if (entry?.completed && entry.completedAt) {
      touched.push({ slug, type: 'lab', touchedAt: entry.completedAt });
    }
  }
  for (const [slug, entry] of Object.entries(state?.quizzes ?? {})) {
    if ((entry?.attempts ?? 0) > 0 && entry.lastAttemptAt) {
      touched.push({ slug, type: 'quiz', touchedAt: entry.lastAttemptAt });
    }
  }

  touched.sort((a, b) => b.touchedAt.localeCompare(a.touchedAt));
  const lastTouched = touched[0] ?? null;

  const resolveFromTrack = (trackSlug: string, startIndex = 0) => {
    const activities = activityMap[trackSlug] ?? [];
    for (let index = startIndex; index < activities.length; index += 1) {
      const activity = activities[index];
      if (!isCompleted(state, activity)) {
        return { trackSlug, activity };
      }
    }
    return null;
  };

  if (lastTouched) {
    for (const track of availableTracks) {
      const activities = activityMap[track.slug] ?? [];
      const lastIndex = activities.findIndex((activity) => activity.slug === lastTouched.slug);
      if (lastIndex === -1) continue;

      if (lastTouched.type === 'quiz') {
        return { track, activity: activities[lastIndex], lastTouched };
      }

      const sameTrackNext = resolveFromTrack(track.slug, lastIndex + 1);
      if (sameTrackNext) {
        return { track, activity: sameTrackNext.activity, lastTouched };
      }

      const nextTrackIndex = availableTracks.findIndex((entry) => entry.slug === track.slug) + 1;
      for (let index = nextTrackIndex; index < availableTracks.length; index += 1) {
        const fallback = resolveFromTrack(availableTracks[index].slug, 0);
        if (fallback) {
          return { track: availableTracks[index], activity: fallback.activity, lastTouched };
        }
      }

      return { track, activity: activities[lastIndex], lastTouched };
    }
  }

  for (const track of availableTracks) {
    const fallback = resolveFromTrack(track.slug, 0);
    if (fallback) {
      return {
        track,
        activity: fallback.activity,
        lastTouched,
      };
    }
  }

  const firstTrack = availableTracks[0];
  const firstActivity = activityMap[firstTrack.slug]?.[0];
  if (!firstActivity) return null;

  return {
    track: firstTrack,
    activity: firstActivity,
    lastTouched,
  };
};

export default function ContinueLearning({ tracks = [], activityMap = {} }: ContinueLearningProps) {
  const [state, setState] = useState<ProgressState | null>(null);

  useEffect(() => {
    const update = () => {
      if (typeof window === 'undefined') {
        setState(null);
        return;
      }

      try {
        const raw = window.localStorage.getItem(PROGRESS_KEY);
        setState(raw ? (JSON.parse(raw) as ProgressState) : null);
      } catch {
        setState(null);
      }
    };

    update();
    window.addEventListener('progress-updated', update);
    window.addEventListener('storage', update);
    return () => {
      window.removeEventListener('progress-updated', update);
      window.removeEventListener('storage', update);
    };
  }, []);

  const recommendation = useMemo(
    () => findRecommendation(tracks, activityMap, state),
    [activityMap, state, tracks]
  );

  if (!recommendation) {
    return (
      <div className="continue-learning-strip">
        <div className="continue-learning__left">
          <div className="continue-learning__icon-badge" aria-hidden="true">✦</div>
          <div className="continue-learning__text-group">
            <div className="continue-learning__track-title">Ready to Begin</div>
            <div className="continue-learning__meta">Pick a certification track to get started.</div>
          </div>
        </div>
        <div className="continue-learning__actions">
          <a className="btn-link" href="/tracks">Browse tracks →</a>
        </div>
      </div>
    );
  }

  const { track, activity, lastTouched } = recommendation;
  const nextHref = activityHref(activity);
  const nextLabel = activity.type === 'lab' ? 'Resume lab' : activity.type === 'quiz' ? 'Resume quiz' : 'Resume lesson';
  const lastLabel = lastTouched ? humanizeSlug(lastTouched.slug) : 'No completed activity yet';

  return (
    <div className="continue-learning-strip">
      <div className="continue-learning__left">
        <div className="continue-learning__icon-badge" aria-hidden="true">▶</div>
        <div className="continue-learning__text-group">
          <div className="continue-learning__primary-row">
            <span className="continue-learning__track-title">{track.title}</span>
            <span className="continue-learning__step-pill">Next: {humanizeSlug(activity.slug)}</span>
          </div>
          <div className="continue-learning__meta">Last completed: {lastLabel}</div>
        </div>
      </div>
      <div className="continue-learning__actions">
        <a className="btn-link" href={nextHref}>{nextLabel} →</a>
        <a className="btn-ghost btn-sm" href={`/tracks/${track.slug}`} style={{ padding: '6px 14px', borderRadius: 'var(--radius-full)', border: '1px solid var(--beattie-border)', fontSize: '13px', color: 'var(--beattie-text)', textDecoration: 'none' }}>Open track</a>
      </div>
    </div>
  );
}