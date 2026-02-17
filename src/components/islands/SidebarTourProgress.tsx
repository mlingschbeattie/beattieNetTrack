import { useEffect, useState } from 'react';
import { getTourPercent } from '../../lib/progressStore';

export default function SidebarTourProgress() {
  const [percent, setPercent] = useState(0);

  useEffect(() => {
    const sync = () => setPercent(getTourPercent('hands-on-tour'));
    sync();
    window.addEventListener('progress-updated', sync);
    return () => window.removeEventListener('progress-updated', sync);
  }, []);

  return <span className="badge badge--muted">Tour {percent}%</span>;
}
