export const BASE_PROGRESS_KEY = 'beattie_progress';
export const PROGRESS_KEY = 'beattie_progress_v1';

/**
 * Resolves the authenticated student/teacher username from the global session context
 * or DOM attribute. Falls back to 'guest' when unauthenticated.
 */
export function getCurrentUsername(): string {
  if (typeof window === 'undefined') return 'guest';
  if ((window as any).__BEATTIE_USER__?.username) {
    return (window as any).__BEATTIE_USER__.username;
  }
  const el = document.querySelector('[data-current-user]');
  if (el) {
    const user = el.getAttribute('data-current-user');
    if (user && user !== 'guest') return user;
  }
  return 'guest';
}

/**
 * Returns the user-scoped localStorage key so multiple students or teachers
 * sharing the same physical browser profile never overwrite or inherit each other's progress.
 */
export function getProgressKey(username = getCurrentUsername()): string {
  if (!username || username === 'guest') {
    return PROGRESS_KEY;
  }
  return `${BASE_PROGRESS_KEY}_${username}_v1`;
}

/**
 * Purges legacy un-scoped test progress (which belonged to the instructor during setup)
 * from student workstations so students always start with a clean record.
 */
export function clearLegacyTestData(storage: StorageLike | null = getStorage()): void {
  if (!storage || typeof window === 'undefined') return;
  const username = getCurrentUsername();
  if (username && username !== 'guest' && username !== 'mbeattie') {
    try {
      window.localStorage.removeItem(PROGRESS_KEY);
    } catch {}
  }
}

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

export type SectionProgress = Record<string, boolean>;

export type GuidedPreferences = {
  autoReveal: boolean;
  autoSeconds: number;
  narrationRate: number;
  syncWithReading: boolean;
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
  lessonSections: Record<string, SectionProgress>;
  guided: GuidedPreferences;
};

export type WaivedContentItem = {
  contentId: string;
  contentType: string;
  domainId: string;
  reason: string;
};

export type WaivedContentState = {
  waivedContent: WaivedContentItem[];
  waivedContentIds: string[];
  lastFetchedAt: string;
};

export const WAIVED_CONTENT_KEY_PREFIX = 'beattie_waived';

export function getWaivedContentKey(username = getCurrentUsername()): string {
  return `${WAIVED_CONTENT_KEY_PREFIX}_${username}_v1`;
}

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
  quizzes: {},
  lessonSections: {},
  guided: {
    autoReveal: false,
    autoSeconds: 5,
    narrationRate: 1,
    syncWithReading: true,
  },
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
      quizzes: parsed.quizzes ?? {},
      lessonSections: parsed.lessonSections ?? {},
      // guided.narrationRate is still used, by the Read-aloud control in
      // Reading mode. autoReveal / autoSeconds / syncWithReading are legacy:
      // they belonged to the retired Guided view and no longer drive any UI.
      // Left in place because this shape is persisted per student.
      guided: {
        autoReveal: Boolean(parsed.guided?.autoReveal),
        autoSeconds:
          typeof parsed.guided?.autoSeconds === 'number'
          && Number.isFinite(parsed.guided.autoSeconds)
          ? Math.min(10, Math.max(2, parsed.guided.autoSeconds))
          : 5,
        narrationRate:
          typeof parsed.guided?.narrationRate === 'number'
          && Number.isFinite(parsed.guided.narrationRate)
          ? Math.min(2, Math.max(0.75, parsed.guided.narrationRate))
          : 1,
        syncWithReading:
          typeof parsed.guided?.syncWithReading === 'boolean'
            ? parsed.guided.syncWithReading
            : true,
      },
    };
  } catch {
    return defaultState();
  }
};

const writeState = (storage: StorageLike, state: ProgressState, key = getProgressKey()) => {
  storage.setItem(key, JSON.stringify(state));
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

export const getProgress = (storage: StorageLike | null = getStorage(), key = getProgressKey()) => {
  if (!storage) return defaultState();
  clearLegacyTestData(storage);
  const username = getCurrentUsername();
  if (username && username !== 'guest') {
    const userSpecific = storage.getItem(key);
    if (userSpecific) {
      return safeParse(userSpecific);
    }
    // Clean slate for newly logged-in student
    const initial = defaultState();
    storage.setItem(key, JSON.stringify(initial));
    return initial;
  }
  return safeParse(storage.getItem(PROGRESS_KEY));
};

export const setProgress = (
  updater: (state: ProgressState) => ProgressState,
  storage: StorageLike | null = getStorage()
) => {
  if (!storage) return defaultState();
  const key = getProgressKey();
  const next = updater(getProgress(storage, key));
  writeState(storage, next, key);
  return next;
};

export function getWaivedContentState(storage: StorageLike | null = getStorage()): WaivedContentState {
  if (!storage) {
    return { waivedContent: [], waivedContentIds: [], lastFetchedAt: '' };
  }
  try {
    const raw = storage.getItem(getWaivedContentKey());
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed?.waivedContentIds)) return parsed;
    }
  } catch {}
  return { waivedContent: [], waivedContentIds: [], lastFetchedAt: '' };
}

export function isContentWaived(contentId: string, storage: StorageLike | null = getStorage()): boolean {
  if (!contentId) return false;
  const state = getWaivedContentState(storage);
  return state.waivedContentIds.includes(contentId);
}

export function getWaivedReason(contentId: string, storage: StorageLike | null = getStorage()): string | null {
  if (!contentId) return null;
  const state = getWaivedContentState(storage);
  const found = state.waivedContent.find((w) => w.contentId === contentId);
  return found?.reason ?? (state.waivedContentIds.includes(contentId) ? 'Certification Credit' : null);
}

export async function fetchWaivedContent(
  apiUrl = 'https://api.beattietech.local',
  storage: StorageLike | null = getStorage()
): Promise<WaivedContentState> {
  const username = getCurrentUsername();
  if (!username || username === 'guest') {
    return { waivedContent: [], waivedContentIds: [], lastFetchedAt: '' };
  }

  try {
    const res = await fetch(`${apiUrl}/api/cis/me/waived-content`, {
      credentials: 'include',
    });
    if (!res.ok) {
      return getWaivedContentState(storage);
    }
    const data = await res.json();
    const nextState: WaivedContentState = {
      waivedContent: Array.isArray(data?.waivedContent) ? data.waivedContent : [],
      waivedContentIds: Array.isArray(data?.waivedContentIds) ? data.waivedContentIds : [],
      lastFetchedAt: new Date().toISOString(),
    };
    if (storage) {
      try {
        storage.setItem(getWaivedContentKey(username), JSON.stringify(nextState));
      } catch {}
    }
    return nextState;
  } catch (err) {
    console.warn('[progressStore] Failed to fetch waived content:', err);
    return getWaivedContentState(storage);
  }
}

export const getLessonStatus = (slug: string, storage: StorageLike | null = getStorage()) => {
  const state = getProgress(storage);
  const waived = isContentWaived(slug, storage);
  const reason = waived ? getWaivedReason(slug, storage) : null;
  const lesson = state.lessons[slug];
  return {
    completed: Boolean(lesson?.completed || waived),
    completedAt: lesson?.completedAt ?? (waived ? new Date().toISOString() : null),
    xpEarned: lesson?.xpEarned ?? 0,
    waived,
    reason,
  };
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
  const waived = isContentWaived(slug, storage);
  const reason = waived ? getWaivedReason(slug, storage) : null;
  return {
    completed: Boolean(lab.completed || waived),
    completedAt: lab.completedAt ?? (waived ? new Date().toISOString() : null),
    xpEarned: lab.xpEarned,
    waived,
    reason,
  };
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

export type TrackProgressItem =
  | string
  | {
      slug: string;
      type?: 'lesson' | 'lab' | 'quiz' | 'activity';
    };

const xpForQuiz = (score: number) => {
  let xp = 10;
  if (score >= 80) xp += 10;
  if (score === 100) xp += 10;
  return xp;
};

export const getTrackProgress = (
  items: TrackProgressItem[],
  storage: StorageLike | null = getStorage()
) => {
  const state = getProgress(storage);
  const total = items.length;
  const completed = items.filter((item) => {
    const slug = typeof item === 'string' ? item : item.slug;
    const type = typeof item === 'string' ? undefined : item.type;

    if (isContentWaived(slug, storage)) {
      return true;
    }

    if (type === 'quiz') {
      return (state.quizzes[slug]?.bestScore ?? 0) >= 70;
    }
    if (type === 'lesson') {
      const lessonEntry = state.lessons[slug];
      if (!lessonEntry?.completed) return false;
      const sectionChecks = state.lessonSections?.[slug];
      if (sectionChecks && Object.keys(sectionChecks).length > 0) {
        return Object.values(sectionChecks).every(Boolean);
      }
      return true;
    }
    if (type === 'lab') {
      return Boolean(state.labs[slug]?.completed);
    }
    if (type === 'activity') {
      return Boolean(state.labs[slug]?.completed || state.lessons[slug]?.completed);
    }

    // Fallback for legacy untyped string entries
    if (state.lessons[slug]?.completed) return true;
    if (state.labs[slug]?.completed) return true;
    if ((state.quizzes[slug]?.bestScore ?? 0) >= 70) return true;
    return false;
  }).length;

  const xpEarned = items.reduce((sum, item) => {
    const slug = typeof item === 'string' ? item : item.slug;
    const type = typeof item === 'string' ? undefined : item.type;

    if (type === 'quiz') {
      const quizBest = state.quizzes[slug]?.bestScore ?? 0;
      return sum + (quizBest >= 70 ? xpForQuiz(quizBest) : 0);
    }
    if (type === 'lesson') {
      return sum + (state.lessons[slug]?.xpEarned ?? 0);
    }
    if (type === 'lab') {
      return sum + (state.labs[slug]?.xpEarned ?? 0);
    }
    if (type === 'activity') {
      return sum + (state.labs[slug]?.xpEarned ?? 0) + (state.lessons[slug]?.xpEarned ?? 0);
    }

    const lessonXp = state.lessons[slug]?.xpEarned ?? 0;
    const labXp = state.labs[slug]?.xpEarned ?? 0;
    return sum + lessonXp + labXp;
  }, 0);

  const percent = total ? Math.round((completed / total) * 100) : 0;
  return { total, completed, xpEarned, percent };
};

export const getLevel = (xpTotal: number) => Math.floor(xpTotal / 100) + 1;

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
  const waived = isContentWaived(quizSlug, storage);
  const reason = waived ? getWaivedReason(quizSlug, storage) : null;
  const existing = state.quizzes[quizSlug] ?? {
    attempts: 0,
    bestScore: 0,
    lastScore: 0,
    lastAttemptAt: null,
    lastXpAwardDate: null,
  };
  return {
    ...existing,
    bestScore: waived ? Math.max(existing.bestScore, 100) : existing.bestScore,
    waived,
    reason,
  };
};

export const getSectionProgress = (
  lessonSlug: string,
  storage: StorageLike | null = getStorage()
): SectionProgress => {
  const state = getProgress(storage);
  return state.lessonSections[lessonSlug] ?? {};
};

export const getGuidedPreferences = (storage: StorageLike | null = getStorage()): GuidedPreferences => {
  const state = getProgress(storage);
  return state.guided;
};

export const setGuidedPreferences = (
  partial: Partial<GuidedPreferences>,
  storage: StorageLike | null = getStorage()
) =>
  setProgress((state) => ({
    ...state,
    guided: {
      autoReveal:
        typeof partial.autoReveal === 'boolean'
          ? partial.autoReveal
          : state.guided.autoReveal,
      autoSeconds:
        typeof partial.autoSeconds === 'number' && Number.isFinite(partial.autoSeconds)
          ? Math.min(10, Math.max(2, partial.autoSeconds))
          : state.guided.autoSeconds,
      narrationRate:
        typeof partial.narrationRate === 'number' && Number.isFinite(partial.narrationRate)
          ? Math.min(2, Math.max(0.75, partial.narrationRate))
          : state.guided.narrationRate,
      syncWithReading:
        typeof partial.syncWithReading === 'boolean'
          ? partial.syncWithReading
          : state.guided.syncWithReading,
    },
  }), storage);

export const isSectionComplete = (
  lessonSlug: string,
  sectionId: string,
  storage: StorageLike | null = getStorage()
): boolean => {
  const sections = getSectionProgress(lessonSlug, storage);
  return Boolean(sections[sectionId]);
};

export const markSectionComplete = (
  lessonSlug: string,
  sectionId: string,
  storage: StorageLike | null = getStorage()
) =>
  setProgress((state) => {
    const existing = state.lessonSections[lessonSlug] ?? {};
    if (existing[sectionId]) return state;
    return {
      ...state,
      lessonSections: {
        ...state.lessonSections,
        [lessonSlug]: {
          ...existing,
          [sectionId]: true,
        },
      },
    };
  }, storage);
