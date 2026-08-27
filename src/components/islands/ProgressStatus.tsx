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
      <div className="dashboard-stats-strip dashboard-stats-strip--skeleton" aria-hidden="true">
        <div className="dash-stat-item-skeleton" />
        <div className="dash-stat-divider" />
        <div className="dash-stat-item-skeleton" />
        <div className="dash-stat-divider" />
        <div className="dash-stat-item-skeleton" />
      </div>
    );
  }

  return (
    <div className="dashboard-stats-strip" role="region" aria-label="Student Progress Summary">
      <div className="dash-stat-item">
        <span className="dash-stat-icon dash-stat-icon--level" aria-hidden="true">◈</span>
        <div className="dash-stat-content">
          <span className="dash-stat-val" data-testid="status-level">Level {status.level}</span>
          <span className="dash-stat-lbl">Student Rank</span>
        </div>
      </div>

      <div className="dash-stat-divider" aria-hidden="true"></div>

      <div className="dash-stat-item">
        <span className="dash-stat-icon dash-stat-icon--xp" aria-hidden="true">⚡</span>
        <div className="dash-stat-content">
          <span className="dash-stat-val" data-testid="status-xp">{status.xpTotal} XP</span>
          <span className="dash-stat-lbl">Total Earned</span>
        </div>
      </div>

      <div className="dash-stat-divider" aria-hidden="true"></div>

      <div className="dash-stat-item">
        <span className="dash-stat-icon dash-stat-icon--streak" aria-hidden="true">🔥</span>
        <div className="dash-stat-content">
          <span className="dash-stat-val" data-testid="status-streak">{status.streak} Day{status.streak === 1 ? '' : 's'}</span>
          <span className="dash-stat-lbl">Activity Streak</span>
        </div>
      </div>
    </div>
  );
}
