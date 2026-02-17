import { useEffect, useState } from 'react';
import { getTrackProgress } from '../../lib/progressStore';

type TrackProgressSummaryProps = {
  lessonSlugs: string[];
};

export default function TrackProgressSummary({ lessonSlugs }: TrackProgressSummaryProps) {
  const [percent, setPercent] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [total, setTotal] = useState(lessonSlugs.length);
  const [earnedXp, setEarnedXp] = useState(0);

  useEffect(() => {
    const update = () => {
      const stats = getTrackProgress(lessonSlugs);
      setPercent(stats.percent);
      setCompleted(stats.completed);
      setTotal(stats.total);
      setEarnedXp(stats.xpEarned);
    };

    update();
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, [lessonSlugs]);

  return (
    <div className="track-progress">
      <div className="track-progress__row">
        <span>
          <span data-testid="track-completed-count">{completed}/{total}</span> completed
        </span>
        <span data-testid="track-xp">{earnedXp} XP</span>
      </div>
      <div className="progress progress--thin" aria-hidden="true">
        <div className="progress__bar" style={{ width: `${percent}%` }}></div>
      </div>
      <div className="track-progress__label">
        <span data-testid="track-percent">{percent}%</span> complete
      </div>
    </div>
  );
}
