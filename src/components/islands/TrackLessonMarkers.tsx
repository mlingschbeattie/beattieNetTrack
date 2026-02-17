import { useEffect } from 'react';
import { getProgress } from '../../lib/progressStore';

type TrackLessonMarkersProps = {
  lessonSlugs: string[];
};

export default function TrackLessonMarkers({ lessonSlugs }: TrackLessonMarkersProps) {
  useEffect(() => {
    const update = () => {
      const progress = getProgress();
      lessonSlugs.forEach((slug) => {
        const el = document.querySelector(`[data-lesson-status="${slug}"]`);
        if (!el) return;
        const completed = Boolean(progress.lessons[slug]?.completed);
        if (completed) {
          el.removeAttribute('hidden');
        } else {
          el.setAttribute('hidden', 'true');
        }
      });
    };

    update();
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, [lessonSlugs]);

  return null;
}
