export const PROGRESS_KEY = 'beattie_progress_v1';

export type LessonProgress = {
  completed: boolean;
  completedAt: string | null;
  xpEarned: number;
};

export type LabProgress = {
  startedAt: string | null;
  lastStepIndex: number;
  completedStepIds: string[];
  completed: boolean;
  completedAt: string | null;
  xpAwarded: boolean;
  xpEarned: number;
};

export type TourProgress = {
  completedSteps: string[];
  totalSteps: number;
  completed: boolean;
  lastStep: string | null;
  updatedAt: string | null;
};

export type ProgressState = {
  version: 1;
  xpTotal: number;
  streak: {
    current: number;
    lastActiveDate: string | null;
  };
  lessons: Record<string, LessonProgress>;
  labs: Record<string, LabProgress>;
  tour: Record<string, TourProgress>;
  quizzes: Record<
    string,
    {
      attempts: number;
      bestScore: number;
      lastScore: number;
      lastAttemptAt: string | null;
      lastXpAwardDate: string | null;
    }
  >;
};

type LessonMeta = {
  difficulty?: string;
  estMinutes?: number;
};

type StorageLike = Pick<Storage, 'getItem' | 'setItem'>;

const defaultState = (): ProgressState => ({
  version: 1,
  xpTotal: 0,
  streak: {
    current: 0,
    lastActiveDate: null,
  },
  lessons: {},
  labs: {},
  tour: {},
  quizzes: {},
});

const defaultLabProgress = (): LabProgress => ({
  startedAt: null,
  lastStepIndex: 0,
  completedStepIds: [],
  completed: false,
  completedAt: null,
  xpAwarded: false,
  xpEarned: 0,
});

const getStorage = (): StorageLike | null => {
  if (typeof window === 'undefined') return null;
  return window.localStorage;
};

const safeParse = (raw: string | null): ProgressState => {
  if (!raw) return defaultState();
  try {
    const parsed = JSON.parse(raw) as ProgressState;
    if (!parsed || typeof parsed !== 'object') return defaultState();
    const parsedLabs = parsed.labs ?? {};
    const normalizedLabs = Object.fromEntries(
      Object.entries(parsedLabs).map(([slug, entry]) => {
        const lab = (entry ?? {}) as Partial<LabProgress>;
        return [
          slug,
          {
            startedAt: lab.startedAt ?? null,
            lastStepIndex: typeof lab.lastStepIndex === 'number' ? lab.lastStepIndex : 0,
            completedStepIds: Array.isArray(lab.completedStepIds)
              ? lab.completedStepIds.filter((id): id is string => typeof id === 'string')
              : [],
            completed: Boolean(lab.completed),
            completedAt: lab.completedAt ?? null,
            xpAwarded: typeof lab.xpAwarded === 'boolean' ? lab.xpAwarded : Boolean(lab.completed),
            xpEarned: typeof lab.xpEarned === 'number' ? lab.xpEarned : 0,
          } satisfies LabProgress,
        ];
      })
    );

    return {
      version: 1,
      xpTotal: parsed.xpTotal ?? 0,
      streak: {
        current: parsed.streak?.current ?? 0,
        lastActiveDate: parsed.streak?.lastActiveDate ?? null,
      },
      lessons: parsed.lessons ?? {},
      labs: normalizedLabs,
      tour: parsed.tour ?? {},
      quizzes: parsed.quizzes ?? {},
    };
  } catch {
    return defaultState();
  }
};

const writeState = (storage: StorageLike, state: ProgressState) => {
  storage.setItem(PROGRESS_KEY, JSON.stringify(state));
};

const normalizeDifficulty = (value?: string) => {
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

const xpForLesson = (meta: LessonMeta) => {
  const difficulty = normalizeDifficulty(meta.difficulty);
  const base = difficulty === 'Beginner' ? 10 : difficulty === 'Advanced' ? 30 : 20;
  const bonus = Math.min(15, Math.floor((meta.estMinutes ?? 0) / 30) * 5);
  return base + bonus;
};

const dateKey = (date: Date) => date.toISOString().slice(0, 10);

export const getProgress = (storage: StorageLike | null = getStorage()) => {
  if (!storage) return defaultState();
  return safeParse(storage.getItem(PROGRESS_KEY));
};

export const setProgress = (
  updater: (state: ProgressState) => ProgressState,
  storage: StorageLike | null = getStorage()
) => {
  if (!storage) return defaultState();
  const next = updater(getProgress(storage));
  writeState(storage, next);
  return next;
};

export const getLessonStatus = (slug: string, storage: StorageLike | null = getStorage()) => {
  const state = getProgress(storage);
  return state.lessons[slug] ?? { completed: false, completedAt: null, xpEarned: 0 };
};

const recalcXpTotal = (state: ProgressState) => {
  const lessonXp = Object.values(state.lessons).reduce((sum, entry) => sum + (entry.xpEarned ?? 0), 0);
  const labXp = Object.values(state.labs).reduce((sum, entry) => sum + (entry.xpEarned ?? 0), 0);
  return lessonXp + labXp;
};

export const markLessonComplete = (
  slug: string,
  meta: LessonMeta = {},
  storage: StorageLike | null = getStorage()
) =>
  setProgress((state) => {
    const existing = state.lessons[slug];
    if (existing?.completed) {
      return state;
    }
    const xpEarned = xpForLesson(meta);
    const lessons = {
      ...state.lessons,
      [slug]: {
        completed: true,
        completedAt: new Date().toISOString(),
        xpEarned,
      },
    };
    return {
      ...state,
      lessons,
      xpTotal: recalcXpTotal({ ...state, lessons }),
    };
  }, storage);

export const markLessonIncomplete = (slug: string, storage: StorageLike | null = getStorage()) =>
  setProgress((state) => {
    if (!state.lessons[slug]?.completed) return state;
    const lessons = {
      ...state.lessons,
      [slug]: {
        completed: false,
        completedAt: null,
        xpEarned: 0,
      },
    };
    return {
      ...state,
      lessons,
      xpTotal: recalcXpTotal({ ...state, lessons }),
    };
  }, storage);

export const getLabStatus = (slug: string, storage: StorageLike | null = getStorage()) => {
  const state = getProgress(storage);
  const lab = state.labs[slug] ?? defaultLabProgress();
  return { completed: lab.completed, completedAt: lab.completedAt, xpEarned: lab.xpEarned };
};

export const getLabState = (slug: string, storage: StorageLike | null = getStorage()) => {
  const state = getProgress(storage);
  return state.labs[slug] ?? defaultLabProgress();
};

export const saveLabState = (
  slug: string,
  partial: Partial<LabProgress>,
  storage: StorageLike | null = getStorage()
) =>
  setProgress((state) => {
    const existing = state.labs[slug] ?? defaultLabProgress();
    const merged: LabProgress = {
      ...existing,
      ...partial,
      completedStepIds: partial.completedStepIds ?? existing.completedStepIds,
    };
    return {
      ...state,
      labs: {
        ...state.labs,
        [slug]: merged,
      },
      xpTotal: recalcXpTotal({
        ...state,
        labs: {
          ...state.labs,
          [slug]: merged,
        },
      }),
    };
  }, storage);

const withRecordedActivity = (state: ProgressState, now: Date = new Date()): ProgressState => {
  const today = dateKey(now);
  const last = state.streak.lastActiveDate;
  if (!last) {
    return {
      ...state,
      streak: { current: 1, lastActiveDate: today },
    };
  }
  if (last === today) {
    return state;
  }
  const lastDate = new Date(`${last}T00:00:00Z`);
  const diffDays = Math.floor((now.getTime() - lastDate.getTime()) / 86400000);
  if (diffDays === 1) {
    return {
      ...state,
      streak: { current: state.streak.current + 1, lastActiveDate: today },
    };
  }
  return {
    ...state,
    streak: { current: 1, lastActiveDate: today },
  };
};

export const markLabCompleted = (
  slug: string,
  xp: number,
  storage: StorageLike | null = getStorage()
) =>
  setProgress((state) => {
    const existing = state.labs[slug] ?? defaultLabProgress();
    if (existing.completed && existing.xpAwarded) {
      return state;
    }

    const normalizedXp = Number.isFinite(xp) ? Math.max(0, xp) : 0;

    const nowIso = new Date().toISOString();
    const updatedLab: LabProgress = {
      ...existing,
      startedAt: existing.startedAt ?? nowIso,
      completed: true,
      completedAt: nowIso,
      xpAwarded: true,
      xpEarned: existing.xpAwarded ? existing.xpEarned : normalizedXp,
    };

    const withLab = {
      ...state,
      labs: {
        ...state.labs,
        [slug]: updatedLab,
      },
    };

    const withXp = {
      ...withLab,
      xpTotal: recalcXpTotal(withLab),
    };

    return withRecordedActivity(withXp);
  }, storage);

export const computeTrackLabProgress = (
  labSlugs: string[],
  storage: StorageLike | null = getStorage()
) => {
  const state = getProgress(storage);
  const total = labSlugs.length;
  const completed = labSlugs.filter((slug) => state.labs[slug]?.completed).length;
  const xpEarned = labSlugs.reduce((sum, slug) => sum + (state.labs[slug]?.xpEarned ?? 0), 0);
  const percent = total ? Math.round((completed / total) * 100) : 0;
  return { total, completed, xpEarned, percent };
};

export const markLabComplete = (
  slug: string,
  meta: LessonMeta = {},
  storage: StorageLike | null = getStorage()
) =>
  markLabCompleted(slug, xpForLesson(meta), storage);

export const markLabIncomplete = (slug: string, storage: StorageLike | null = getStorage()) =>
  setProgress((state) => {
    if (!state.labs[slug]?.completed) return state;
    const existing = state.labs[slug] ?? defaultLabProgress();
    const labs = {
      ...state.labs,
      [slug]: {
        ...existing,
        completed: false,
        completedAt: null,
        xpAwarded: false,
        xpEarned: 0,
      },
    };
    return {
      ...state,
      labs,
      xpTotal: recalcXpTotal({ ...state, labs }),
    };
  }, storage);

export const recordActivity = (
  storage: StorageLike | null = getStorage(),
  now: Date = new Date()
) =>
  setProgress((state) => withRecordedActivity(state, now), storage);

export const getTrackProgress = (
  lessonSlugs: string[],
  storage: StorageLike | null = getStorage()
) => {
  const state = getProgress(storage);
  const total = lessonSlugs.length;
  const completed = lessonSlugs.filter((slug) => state.lessons[slug]?.completed).length;
  const xpEarned = lessonSlugs.reduce((sum, slug) => sum + (state.lessons[slug]?.xpEarned ?? 0), 0);
  const percent = total ? Math.round((completed / total) * 100) : 0;
  return { total, completed, xpEarned, percent };
};

export const getLevel = (xpTotal: number) => Math.floor(xpTotal / 100) + 1;

const xpForQuiz = (score: number) => {
  let xp = 10;
  if (score >= 80) xp += 10;
  if (score === 100) xp += 10;
  return xp;
};

export const recordQuizAttempt = (
  quizSlug: string,
  score: number,
  today: string = dateKey(new Date()),
  storage: StorageLike | null = getStorage()
) =>
  setProgress((state) => {
    const existing = state.quizzes[quizSlug] ?? {
      attempts: 0,
      bestScore: 0,
      lastScore: 0,
      lastAttemptAt: null,
      lastXpAwardDate: null,
    };

    const lastXpAwardDate = existing.lastXpAwardDate ?? null;
    const shouldAward = lastXpAwardDate !== today;
    const quizXp = shouldAward ? xpForQuiz(score) : 0;

    const nextQuiz = {
      attempts: existing.attempts + 1,
      bestScore: Math.max(existing.bestScore, score),
      lastScore: score,
      lastAttemptAt: new Date().toISOString(),
      lastXpAwardDate: shouldAward ? today : lastXpAwardDate,
    };

    const quizzes = {
      ...state.quizzes,
      [quizSlug]: nextQuiz,
    };

    return {
      ...state,
      quizzes,
      xpTotal: state.xpTotal + quizXp,
    };
  }, storage);

export const getQuizStats = (quizSlug: string, storage: StorageLike | null = getStorage()) => {
  const state = getProgress(storage);
  return state.quizzes[quizSlug] ?? {
    attempts: 0,
    bestScore: 0,
    lastScore: 0,
    lastAttemptAt: null,
    lastXpAwardDate: null,
  };
};

export const getTourProgress = (tourSlug: string, storage: StorageLike | null = getStorage()) => {
  const state = getProgress(storage);
  return (
    state.tour[tourSlug] ?? {
      completedSteps: [],
      totalSteps: 0,
      completed: false,
      lastStep: null,
      updatedAt: null,
    }
  );
};

export const markTourStepComplete = (
  tourSlug: string,
  stepSlug: string,
  totalSteps: number,
  storage: StorageLike | null = getStorage()
) =>
  setProgress((state) => {
    const existing =
      state.tour[tourSlug] ?? {
        completedSteps: [],
        totalSteps: 0,
        completed: false,
        lastStep: null,
        updatedAt: null,
      };
    const stepSet = new Set(existing.completedSteps);
    stepSet.add(stepSlug);
    const completedSteps = Array.from(stepSet);
    const completed = totalSteps > 0 && completedSteps.length >= totalSteps;
    return {
      ...state,
      tour: {
        ...state.tour,
        [tourSlug]: {
          completedSteps,
          totalSteps,
          completed,
          lastStep: stepSlug,
          updatedAt: new Date().toISOString(),
        },
      },
    };
  }, storage);

export const resetTourProgress = (tourSlug: string, storage: StorageLike | null = getStorage()) =>
  setProgress((state) => {
    const nextTour = { ...state.tour };
    delete nextTour[tourSlug];
    return {
      ...state,
      tour: nextTour,
    };
  }, storage);

export const getTourPercent = (tourSlug: string, storage: StorageLike | null = getStorage()) => {
  const progress = getTourProgress(tourSlug, storage);
  if (!progress.totalSteps) return 0;
  return Math.round((progress.completedSteps.length / progress.totalSteps) * 100);
};
