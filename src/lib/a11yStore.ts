/**
 * Accessibility / sensory preferences.
 *
 * Stored locally per student (no account needed) and applied as data-attributes
 * on <html> so plain CSS can respond. Written to match the local-first model
 * used by progressStore/checksStore.
 *
 * Defaults are deliberately conservative: the app looks as it does today until
 * a student opts into a calmer presentation.
 */

export const A11Y_KEY = 'beattie_a11y_v1';

export type TextSize = 'default' | 'large' | 'larger';
export type MotionPref = 'system' | 'reduced' | 'full';

export type A11yState = {
  version: 1;
  /** Overrides prefers-reduced-motion when set to 'reduced' or 'full'. */
  motion: MotionPref;
  /** Lower visual density: muted accents, flatter surfaces, no glow/shadow. */
  calmMode: boolean;
  /** Collapse long catalogs by default so pages open small, not overwhelming. */
  collapseCatalogs: boolean;
  /** Root font scale. */
  textSize: TextSize;
  /** Wider spacing between lines, for dyslexia and tracking difficulty. */
  readableSpacing: boolean;
  /** Always underline links rather than relying on color alone. */
  underlineLinks: boolean;
};

export const A11Y_DEFAULTS: A11yState = {
  version: 1,
  motion: 'system',
  calmMode: false,
  collapseCatalogs: true,
  textSize: 'default',
  readableSpacing: false,
  underlineLinks: false,
};

const oneOf = <T extends string>(value: unknown, allowed: readonly T[], fallback: T): T =>
  typeof value === 'string' && (allowed as readonly string[]).includes(value) ? (value as T) : fallback;

/** Never throws: corrupt or stale storage degrades to defaults. */
export const safeParseA11y = (raw: string | null): A11yState => {
  if (!raw) return { ...A11Y_DEFAULTS };
  try {
    const parsed = JSON.parse(raw) as Partial<A11yState>;
    return {
      version: 1,
      motion: oneOf(parsed.motion, ['system', 'reduced', 'full'] as const, A11Y_DEFAULTS.motion),
      calmMode: typeof parsed.calmMode === 'boolean' ? parsed.calmMode : A11Y_DEFAULTS.calmMode,
      collapseCatalogs:
        typeof parsed.collapseCatalogs === 'boolean' ? parsed.collapseCatalogs : A11Y_DEFAULTS.collapseCatalogs,
      textSize: oneOf(parsed.textSize, ['default', 'large', 'larger'] as const, A11Y_DEFAULTS.textSize),
      readableSpacing:
        typeof parsed.readableSpacing === 'boolean' ? parsed.readableSpacing : A11Y_DEFAULTS.readableSpacing,
      underlineLinks:
        typeof parsed.underlineLinks === 'boolean' ? parsed.underlineLinks : A11Y_DEFAULTS.underlineLinks,
    };
  } catch {
    return { ...A11Y_DEFAULTS };
  }
};

export const readA11y = (): A11yState => {
  if (typeof window === 'undefined') return { ...A11Y_DEFAULTS };
  return safeParseA11y(window.localStorage.getItem(A11Y_KEY));
};

/** Mirrors state onto <html> as data-attributes for CSS to key off. */
export const applyA11yToDocument = (state: A11yState) => {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  root.dataset.motion = state.motion;
  root.dataset.calm = state.calmMode ? 'on' : 'off';
  root.dataset.textSize = state.textSize;
  root.dataset.spacing = state.readableSpacing ? 'readable' : 'default';
  root.dataset.underlineLinks = state.underlineLinks ? 'on' : 'off';
};

export const writeA11y = (state: A11yState) => {
  if (typeof window === 'undefined') return;
  window.localStorage.setItem(A11Y_KEY, JSON.stringify(state));
  applyA11yToDocument(state);
  window.dispatchEvent(new CustomEvent('beattie:a11ychange', { detail: state }));
};

export const setA11y = (patch: Partial<A11yState>): A11yState => {
  const next = { ...readA11y(), ...patch, version: 1 as const };
  writeA11y(next);
  return next;
};

export const subscribeA11y = (fn: (state: A11yState) => void) => {
  if (typeof window === 'undefined') return () => {};
  const handler = (event: Event) => fn((event as CustomEvent).detail as A11yState);
  window.addEventListener('beattie:a11ychange', handler);
  return () => window.removeEventListener('beattie:a11ychange', handler);
};
