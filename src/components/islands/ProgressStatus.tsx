import { useEffect, useState } from 'react';
import { getLevel, getProgress } from '../../lib/progressStore';

type Status = {
  level: number;
  xpTotal: number;
  streak: number;
};

export default function ProgressStatus() {
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
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, []);

  return (
    <>
      <div className="status-pill">
        <span className="status-pill__icon">⚡</span>
        <div>
          <div className="status-pill__label">Level</div>
          <div className="status-pill__value" data-testid="status-level">{status.level}</div>
        </div>
      </div>
      <div className="status-pill">
        <span className="status-pill__icon">⭐</span>
        <div>
          <div className="status-pill__label">XP</div>
          <div className="status-pill__value" data-testid="status-xp">{status.xpTotal}</div>
        </div>
      </div>
      <div className="status-pill">
        <span className="status-pill__icon">🔥</span>
        <div>
          <div className="status-pill__label">Streak</div>
          <div className="status-pill__value" data-testid="status-streak">
            {status.streak} {status.streak === 1 ? 'day' : 'days'}
          </div>
        </div>
      </div>
    </>
  );
}
