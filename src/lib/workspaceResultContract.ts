export type WorkspaceResultAction = 'run' | 'check' | 'submit' | 'reset';

export type WorkspaceCheck = {
  id: string;
  label: string;
  pass: boolean;
  message?: string;
};

export type WorkspaceResultPayload = {
  slug: string;
  action: WorkspaceResultAction;
  passed: boolean;
  progress: number;
  message?: string;
  difficulty?: string;
  estMinutes?: number;
  score?: number;
  checks?: WorkspaceCheck[];
};

const allowedActions: readonly WorkspaceResultAction[] = ['run', 'check', 'submit', 'reset'];

const allowedKeys = new Set<keyof WorkspaceResultPayload>([
  'slug',
  'action',
  'passed',
  'progress',
  'message',
  'difficulty',
  'estMinutes',
  'score',
  'checks',
]);

const isPlainObject = (input: unknown): input is Record<string, unknown> => {
  if (!input || typeof input !== 'object' || Array.isArray(input)) return false;
  const proto = Object.getPrototypeOf(input);
  return proto === Object.prototype || proto === null;
};

const isWorkspaceCheck = (input: unknown): input is WorkspaceCheck => {
  if (!isPlainObject(input)) return false;
  const keys = Object.keys(input);
  for (const key of keys) {
    if (key !== 'id' && key !== 'label' && key !== 'pass' && key !== 'message') return false;
  }
  if (typeof input.id !== 'string') return false;
  if (typeof input.label !== 'string') return false;
  if (typeof input.pass !== 'boolean') return false;
  if ('message' in input && typeof input.message !== 'string') return false;
  return true;
};

export function validateWorkspaceResultPayload(input: unknown): input is WorkspaceResultPayload {
  if (!isPlainObject(input)) return false;

  const inputKeys = Object.keys(input);
  for (const key of inputKeys) {
    if (!allowedKeys.has(key as keyof WorkspaceResultPayload)) return false;
    if (key === 'timestamp' || key === 'time' || key === 'now' || key === 'date') return false;
  }

  if (typeof input.slug !== 'string') return false;
  if (typeof input.action !== 'string' || !allowedActions.includes(input.action as WorkspaceResultAction)) return false;
  if (typeof input.passed !== 'boolean') return false;
  if (typeof input.progress !== 'number' || !Number.isFinite(input.progress)) return false;

  if ('message' in input && typeof input.message !== 'string') return false;
  if ('difficulty' in input && typeof input.difficulty !== 'string') return false;
  if ('estMinutes' in input && typeof input.estMinutes !== 'number') return false;
  if ('score' in input && typeof input.score !== 'number') return false;
  if ('checks' in input) {
    if (!Array.isArray(input.checks)) return false;
    if (!input.checks.every(isWorkspaceCheck)) return false;
  }

  return true;
}

export function coerceWorkspaceResultPayload(input: unknown): WorkspaceResultPayload | null {
  return validateWorkspaceResultPayload(input) ? input : null;
}
