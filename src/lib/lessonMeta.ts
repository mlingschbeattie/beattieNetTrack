type LessonMetaInput = {
  description?: string;
  difficulty?: string;
  estMinutes?: number;
  estimatedMinutes?: number;
};

export type LessonDifficulty = 'Beginner' | 'Intermediate' | 'Advanced';

const normalizeDifficulty = (value?: string): LessonDifficulty => {
  if (!value) return 'Intermediate';
  const lower = value.toLowerCase();
  if (lower === 'easy') return 'Beginner';
  if (lower === 'medium') return 'Intermediate';
  if (lower === 'hard') return 'Advanced';
  if (lower === 'beginner') return 'Beginner';
  if (lower === 'intermediate') return 'Intermediate';
  if (lower === 'advanced') return 'Advanced';
  return 'Intermediate';
};

export const normalizeLessonMeta = (entryData: LessonMetaInput) => {
  return {
    description: entryData.description ?? 'Legacy page - being upgraded.',
    difficulty: normalizeDifficulty(entryData.difficulty),
    estMinutes: entryData.estMinutes ?? entryData.estimatedMinutes ?? 15,
  };
};
