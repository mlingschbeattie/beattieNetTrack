import { useEffect, useState } from 'react';
import { getLevel, getProgress } from '../../lib/progressStore';

type Status = {
  level: number;
  xpTotal: number;
  streak: number;
};

export default function ProgressStatus() {
  const [isMounted, setIsMounted] = useState(false);
  const [status, setStatus] = useState<Status>({ level: 1, xpTotal: 0, streak: 0 });

  useEffect(() => {
    const update = () => {
      const progress = getProgress();
      setStatus({
        level: getLevel(progress.xpTotal),
        xpTotal: progress.xpTotal,
        streak: progress.streak.current,
      });
    };

    update();
    setIsMounted(true);
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, []);

  if (!isMounted) {
    return (
      <div className="progress-status-skeleton">
        <div className="progress-status-skeleton__pill" />
        <div className="progress-status-skeleton__pill" />
        <div className="progress-status-skeleton__pill" />
      </div>
    );
  }

  return (
    <div className="competency-dash__stats">
      <div className="competency-dash__stat-card">
        <span className="competency-dash__stat-num" data-testid="status-level">{status.level}</span>
        <span className="competency-dash__stat-label">Level</span>
      </div>
      <div className="competency-dash__stat-card">
        <span className="competency-dash__stat-num" data-testid="status-xp">{status.xpTotal}</span>
        <span className="competency-dash__stat-label">XP</span>
      </div>
      <div className="competency-dash__stat-card">
        <span className="competency-dash__stat-num" data-testid="status-streak">
          {status.streak}
        </span>
        <span className="competency-dash__stat-label">Day Streak</span>
      </div>
    </div>
  );
}
