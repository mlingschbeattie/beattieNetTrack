/**
 * Hub event bus client.
 *
 * Every meaningful action a student takes must be reported to the hub so the
 * CIS scoring engine can accumulate competency data. Events are fire-and-forget:
 * emission failures never interrupt the student experience.
 *
 * CIS event contract (per cis-build-bible.md §5):
 *   - All scoring events must include `domains`, `contentType`, `contentId`
 *   - Time events (beacon) also include `sessionId`
 *   - Mastery events also include `score` and `maxScore`
 */

const isBrowser = () => typeof window !== 'undefined';

// ─── Types ────────────────────────────────────────────────────────────────────

export interface CISDomainTag {
  /** e.g. 'aplus1.networking', 'sec+.3.0' */
  domainId: string;
  /** 0.0–1.0 — how strongly this event maps to this domain */
  weight: number;
}

export interface CISEventPayload {
  domains: CISDomainTag[];
  contentType: string;  // 'lab' | 'question' | 'quiz' | 'journal' | etc.
  contentId: string;
  sessionId?: string;
  score?: number;       // 0–100
  maxScore?: number;    // default 100
  [key: string]: unknown;
}

export interface HubEvent {
  appId: string;        // 'lms' | 'quests' | 'journal' | 'game'
  eventType: string;    // e.g. 'lms.lab_started', 'lms.lab_completed'
  payload: CISEventPayload;
}

// ─── Core emitter ─────────────────────────────────────────────────────────────

/**
 * Post a hub event. Fire-and-forget — always returns void, never throws.
 * Call this from browser-side code only (guards against SSR).
 */
export function emitEvent(event: HubEvent, apiUrl: string): void {
  if (!isBrowser() || !apiUrl) return;
  fetch(`${apiUrl}/api/events`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(event),
  }).catch(() => {}); // silent — beacon loss is acceptable
}

// ─── Convenience helpers for LMS events ──────────────────────────────────────

const LS_STARTED_PREFIX = 'lms_started_date_';
const LS_COMPLETED_PREFIX = 'lms_completed_';
const LS_QUIZ_COMPLETED_PREFIX = 'lms_quiz_completed_';
const LS_LESSON_STARTED_PREFIX = 'lms_lesson_started_';
const LS_LESSON_COMPLETED_PREFIX = 'lms_lesson_completed_';

/**
 * Emit `lms.lab_started` — gated to fire at most once per calendar day per lab.
 */
export function emitLabStarted(
  labId: string,
  labTitle: string,
  domains: CISDomainTag[],
  apiUrl: string,
): void {
  if (!isBrowser()) return;

  const storageKey = `${LS_STARTED_PREFIX}${labId}`;
  const today = new Date().toISOString().slice(0, 10); // 'YYYY-MM-DD'
  const lastDate = window.localStorage.getItem(storageKey);
  if (lastDate === today) return; // already emitted today

  window.localStorage.setItem(storageKey, today);
  emitEvent(
    {
      appId: 'lms',
      eventType: 'lms.lab_started',
      payload: {
        domains,
        contentType: 'lab',
        contentId: labId,
        sessionId: crypto.randomUUID(),
        labTitle,
      },
    },
    apiUrl,
  );
}

/**
 * Emit `lms.lab_completed` — fires exactly once per lab (guarded by a
 * permanent localStorage flag so refreshes don't re-emit).
 */
export function emitLabCompleted(
  labId: string,
  answerCount: number,
  domains: CISDomainTag[],
  apiUrl: string,
): void {
  if (!isBrowser()) return;

  const storageKey = `${LS_COMPLETED_PREFIX}${labId}`;
  if (window.localStorage.getItem(storageKey)) return; // already emitted

  window.localStorage.setItem(storageKey, '1');
  emitEvent(
    {
      appId: 'lms',
      eventType: 'lms.lab_completed',
      payload: {
        domains,
        contentType: 'lab',
        contentId: labId,
        score: 100,
        maxScore: 100,
        answerCount,
      },
    },
    apiUrl,
  );
}

/**
 * Emit `lms.quiz_completed` — fires when a quiz is submitted.
 */
export function emitQuizCompleted(
  quizId: string,
  score: number,
  maxScore: number = 100,
  domains: CISDomainTag[],
  apiUrl: string,
): void {
  if (!isBrowser() || !apiUrl || domains.length === 0) return;

  emitEvent(
    {
      appId: 'lms',
      eventType: 'lms.quiz_completed',
      payload: {
        domains,
        contentType: 'quiz',
        contentId: quizId,
        score,
        maxScore,
        submittedAt: new Date().toISOString(),
      },
    },
    apiUrl,
  );
}

/**
 * Emit `lms.lesson_started` — fires at most once per calendar day per lesson.
 */
export function emitLessonStarted(
  lessonId: string,
  lessonTitle: string,
  domains: CISDomainTag[],
  apiUrl: string,
): void {
  if (!isBrowser() || !apiUrl || domains.length === 0) return;

  const storageKey = `${LS_LESSON_STARTED_PREFIX}${lessonId}`;
  const today = new Date().toISOString().slice(0, 10);
  const lastDate = window.localStorage.getItem(storageKey);
  if (lastDate === today) return;

  window.localStorage.setItem(storageKey, today);
  emitEvent(
    {
      appId: 'lms',
      eventType: 'lms.lesson_started',
      payload: {
        domains,
        contentType: 'lesson',
        contentId: lessonId,
        sessionId: crypto.randomUUID(),
        lessonTitle,
      },
    },
    apiUrl,
  );
}

/**
 * Emit `lms.lesson_completed` — fires once when a lesson reading is completed.
 */
export function emitLessonCompleted(
  lessonId: string,
  domains: CISDomainTag[],
  apiUrl: string,
): void {
  if (!isBrowser() || !apiUrl || domains.length === 0) return;

  const storageKey = `${LS_LESSON_COMPLETED_PREFIX}${lessonId}`;
  if (window.localStorage.getItem(storageKey)) return;

  window.localStorage.setItem(storageKey, '1');
  emitEvent(
    {
      appId: 'lms',
      eventType: 'lms.lesson_completed',
      payload: {
        domains,
        contentType: 'lesson',
        contentId: lessonId,
        score: 100,
        maxScore: 100,
      },
    },
    apiUrl,
  );
}

