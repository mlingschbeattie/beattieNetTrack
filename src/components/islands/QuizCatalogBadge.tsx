import { useEffect, useState } from 'react';
import { getQuizStats } from '../../lib/progressStore';

type QuizCatalogBadgeProps = {
  quizSlug: string;
};

export default function QuizCatalogBadge({ quizSlug }: QuizCatalogBadgeProps) {
  const [bestScore, setBestScore] = useState(0);

  useEffect(() => {
    const update = () => {
      const stats = getQuizStats(quizSlug);
      setBestScore(stats.bestScore ?? 0);
    };

    update();
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, [quizSlug]);

  if (!bestScore) return null;

  return <span className="pill pill--success">Best: {bestScore}%</span>;
}
