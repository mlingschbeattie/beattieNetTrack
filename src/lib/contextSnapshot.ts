import { getProgress } from './progressStore';
import { getChecksState } from './checksStore';

export type ContextSnapshot = {
  route: {
    path: string;
    trackSlug?: string;
    lessonSlug?: string;
    labSlug?: string;
    quizSlug?: string;
    tourSlug?: string;
  };
  progress: ReturnType<typeof getProgress>;
  lastCheck?: unknown;
  optional?: {
    codeText?: string;
    lastTerminalCommand?: string;
  };
};

const parseRoute = (path: string) => {
  const parts = path.split('/').filter(Boolean);
  const route: ContextSnapshot['route'] = { path };

  if (parts[0] === 'tracks' && parts[1]) route.trackSlug = parts[1];
  if (parts[0] === 'lessons' && parts[1]) route.lessonSlug = parts[1];
  if (parts[0] === 'labs' && parts[1]) route.labSlug = parts[1];
  if (parts[0] === 'quizzes' && parts[1]) route.quizSlug = parts[1];
  if (parts[0] === 'tour' && parts[1]) route.tourSlug = parts[1];
  if (parts[0] === 'workspace' && parts[1] && parts[2]) {
    if (parts[1] === 'lesson') route.lessonSlug = parts[2];
    if (parts[1] === 'lab') route.labSlug = parts[2];
    if (parts[1] === 'quiz') route.quizSlug = parts[2];
  }

  return route;
};

export const getContextSnapshot = (): ContextSnapshot => {
  const path = typeof window === 'undefined' ? '/' : window.location.pathname;
  const route = parseRoute(path);
  const checks = getChecksState();
  const slug = route.labSlug ?? route.quizSlug ?? route.lessonSlug ?? route.tourSlug;
  const codeEditor = typeof document === 'undefined' ? null : document.querySelector('[data-testid="code-editor"]') as HTMLTextAreaElement | null;
  const terminalLines = typeof document === 'undefined' ? [] : Array.from(document.querySelectorAll('.terminal-sim__line'));
  const lastTerminalCommand = terminalLines
    .map((line) => (line.textContent ?? '').trim())
    .filter((line) => line.includes('$'))
    .at(-1);

  return {
    route,
    progress: getProgress(),
    lastCheck: slug ? checks.records[slug] : undefined,
    optional: {
      codeText: codeEditor?.value,
      lastTerminalCommand,
    },
  };
};
