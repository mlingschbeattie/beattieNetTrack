import { useEffect, useState } from 'react';
import {
  getLessonStatus,
  markLessonComplete,
  markLessonIncomplete,
  recordActivity,
} from '../../lib/progressStore';

type LessonProgressControlsProps = {
  lessonSlug: string;
  difficulty?: string;
  estMinutes?: number;
};

export default function LessonProgressControls({
  lessonSlug,
  difficulty,
  estMinutes,
}: LessonProgressControlsProps) {
  const [completed, setCompleted] = useState(false);
  const [xpEarned, setXpEarned] = useState(0);

  const refresh = () => {
    const status = getLessonStatus(lessonSlug);
    setCompleted(status.completed);
    setXpEarned(status.xpEarned);
  };

  useEffect(() => {
    refresh();
    window.addEventListener('progress-updated', refresh);
    return () => window.removeEventListener('progress-updated', refresh);
  }, [lessonSlug]);

  const handleComplete = () => {
    markLessonComplete(lessonSlug, { difficulty, estMinutes });
    recordActivity();
    window.dispatchEvent(new CustomEvent('progress-updated'));
  };

  const handleIncomplete = () => {
    markLessonIncomplete(lessonSlug);
    window.dispatchEvent(new CustomEvent('progress-updated'));
  };

  const handleCheckIn = () => {
    recordActivity();
    window.dispatchEvent(new CustomEvent('progress-updated'));
  };

  return (
    <div className="lesson-actions" data-testid="lesson-actions">
      <button className="btn-primary" type="button" onClick={handleComplete} data-testid="mark-complete">
        Mark Complete
      </button>
      {completed && (
        <button className="btn-secondary" type="button" onClick={handleIncomplete} data-testid="mark-incomplete">
          Mark Incomplete
        </button>
      )}
      <button className="btn-ghost" type="button" onClick={handleCheckIn} data-testid="check-in">
        Check-in
      </button>
      {completed && (
        <span className="pill pill--success" data-testid="xp-earned">XP earned: {xpEarned}</span>
      )}
    </div>
  );
}
