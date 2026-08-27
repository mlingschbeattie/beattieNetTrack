import { useEffect, useState } from 'react';
import { getTrackProgress } from '../../lib/progressStore';

type TrackProgressSummaryProps = {
  activitySlugs?: string[];
  lessonSlugs?: string[];
};

const PROGRESS_MESSAGES = [
  "Just getting started — your journey begins here.",
  "First checkpoint! Keep that momentum.",
  "Two down. You're building something real.",
  "Halfway through — nobody quits at the halfway point.",
  "More than half! The cert is within reach.",
  "Almost there — don't stop now.",
  "One more activity and you're done.",
  "🎉 Track complete! Time to attempt the real exam.",
];

export default function TrackProgressSummary({ activitySlugs, lessonSlugs }: TrackProgressSummaryProps) {
  const items = activitySlugs ?? lessonSlugs ?? [];
  const [percent, setPercent] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [total, setTotal] = useState(items.length);
  const [earnedXp, setEarnedXp] = useState(0);
  const [displayPct, setDisplayPct] = useState(0);

  useEffect(() => {
    const update = () => {
      const stats = getTrackProgress(items);
      setPercent(stats.percent);
      setCompleted(stats.completed);
      setTotal(stats.total);
      setEarnedXp(stats.xpEarned);
    };

    update();
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, [items]);

  useEffect(() => {
    const t = setTimeout(() => setDisplayPct(percent), 100);
    return () => clearTimeout(t);
  }, [percent]);

  const pct = Math.round((completed / Math.max(total, 1)) * 100);
  const message = PROGRESS_MESSAGES[Math.min(completed, PROGRESS_MESSAGES.length - 1)];

  return (
    <div className="track-progress-strip">
      <div className="progress-strip__info">
        <div className="progress-strip__title" data-testid="track-completed-count">
          {completed} of {total} Activities Completed
        </div>
        <div className="progress-strip__subtitle">{message}</div>
      </div>
      <div className="progress-strip__bar-wrap">
        <div
          className="progress-bar-track"
          role="progressbar"
          aria-valuenow={completed}
          aria-valuemin={0}
          aria-valuemax={total}
          aria-label={`Track progress: ${pct}%`}
        >
          <div className="progress-bar-fill" style={{ width: `${displayPct}%` }}></div>
        </div>
        <div className="progress-strip__percent" data-testid="track-percent">{pct}%</div>
      </div>
      <div className="progress-strip__xp">
        <span className="progress-strip__xp-val" data-testid="track-xp">+{earnedXp}</span>
        <span className="progress-strip__xp-label">XP</span>
      </div>
    </div>
  );
}
