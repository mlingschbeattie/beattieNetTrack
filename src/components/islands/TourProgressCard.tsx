import { useEffect, useState } from 'react';
import { getTourPercent, getTourProgress } from '../../lib/progressStore';

type TourProgressCardProps = {
  tourSlug: string;
  firstStepSlug: string;
};

export default function TourProgressCard({ tourSlug, firstStepSlug }: TourProgressCardProps) {
  const [percent, setPercent] = useState(0);
  const [continueSlug, setContinueSlug] = useState(firstStepSlug);

  useEffect(() => {
    const sync = () => {
      const progress = getTourProgress(tourSlug);
      setPercent(getTourPercent(tourSlug));
      setContinueSlug(progress.lastStep ?? firstStepSlug);
    };

    sync();
    window.addEventListener('progress-updated', sync);
    return () => window.removeEventListener('progress-updated', sync);
  }, [tourSlug, firstStepSlug]);

  return (
    <div className="card" data-testid="tour-progress-card">
      <h3>Continue Tour</h3>
      <p data-testid="tour-percent">{percent}% complete</p>
      <a className="btn-link" href={`/tour/${continueSlug}`} data-testid="tour-continue-link">
        Continue →
      </a>
    </div>
  );
}
