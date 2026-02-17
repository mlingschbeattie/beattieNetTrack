export type CheckItem = {
  id: string;
  label: string;
  pass: boolean;
  message?: string;
};

export type LastCheckResult = {
  passed: boolean;
  score: number | null;
  checks: CheckItem[];
  timestamp: number;
  action?: 'check' | 'submit' | 'run' | 'reset';
  message?: string;
};

export type CheckRecord = LastCheckResult;

export type RequirementItem = {
  id: string;
  label: string;
  pass?: boolean;
  message?: string;
};

const STORAGE_KEY = 'beattie_checks_v2';

export type ChecksState = {
  records: Record<string, LastCheckResult>;
  requirements: Record<string, RequirementItem[]>;
};

type Subscriber = (state: ChecksState) => void;
const subscribers = new Set<Subscriber>();

const isBrowser = () => typeof window !== 'undefined';

const defaultState = (): ChecksState => ({ records: {}, requirements: {} });

const readState = (): ChecksState => {
  if (!isBrowser()) return defaultState();
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) return defaultState();
  try {
    const parsed = JSON.parse(raw) as ChecksState;
    if (!parsed || typeof parsed !== 'object' || typeof parsed.records !== 'object') {
      return defaultState();
    }
    return {
      records: parsed.records,
      requirements: typeof parsed.requirements === 'object' && parsed.requirements ? parsed.requirements : {},
    };
  } catch {
    return defaultState();
  }
};

const writeState = (state: ChecksState) => {
  if (!isBrowser()) return;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
};

const notify = (state: ChecksState) => {
  subscribers.forEach((subscriber) => subscriber(state));
};

export const getChecksState = () => readState();

export const setLastResult = (itemSlug: string, resultObject: LastCheckResult) => {
  const state = readState();
  state.records[itemSlug] = resultObject;
  writeState(state);
  notify(state);
  return resultObject;
};

export const getLastResult = (itemSlug: string) => readState().records[itemSlug] ?? null;

export const setRequirementChecklist = (itemSlug: string, checklist: RequirementItem[]) => {
  const state = readState();
  state.requirements[itemSlug] = checklist;
  writeState(state);
  notify(state);
  return checklist;
};

export const getRequirementChecklist = (itemSlug: string) => readState().requirements[itemSlug] ?? [];

export const clearCheckRecord = (itemSlug: string) => {
  const state = readState();
  delete state.records[itemSlug];
  writeState(state);
  notify(state);
  return state;
};

export const clearAllChecks = () => {
  const state = defaultState();
  writeState(state);
  notify(state);
};

export const clearRequirementChecklist = (itemSlug: string) => {
  const state = readState();
  delete state.requirements[itemSlug];
  writeState(state);
  notify(state);
};

export const subscribeChecks = (listener: Subscriber) => {
  subscribers.add(listener);
  listener(readState());
  return () => {
    subscribers.delete(listener);
  };
};

export const setCheckRecord = (record: {
  slug: string;
  action?: 'check' | 'submit' | 'run' | 'reset';
  status?: 'pass' | 'fail' | 'idle';
  message?: string;
  progress?: number;
  score?: number;
  ts?: number;
  details?: unknown;
}) => {
  return setLastResult(record.slug, {
    passed: record.status === 'pass' || (typeof record.score === 'number' ? record.score >= 70 : false),
    score: typeof record.score === 'number' ? record.score : null,
    checks: [
      {
        id: 'legacy-result',
        label: record.message ?? 'Result updated',
        pass: record.status === 'pass',
        message: typeof record.details === 'string' ? record.details : undefined,
      },
    ],
    timestamp: record.ts ?? Date.now(),
    action: record.action,
    message: record.message,
  });
};

export const getCheckRecord = (slug: string) => getLastResult(slug);
