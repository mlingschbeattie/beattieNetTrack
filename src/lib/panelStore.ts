export type RightPanelTab = 'checks' | 'hints' | 'notes' | 'coach';

export type PanelState = {
  isOpen: boolean;
  activeTab: RightPanelTab;
  width: number;
};

type Subscriber = (state: PanelState) => void;

const STORAGE_KEY = 'beattie_right_panel_v1';
const DEFAULT_STATE: PanelState = {
  isOpen: false,
  activeTab: 'checks',
  width: 340,
};

const subscribers = new Set<Subscriber>();

const isBrowser = () => typeof window !== 'undefined';

const clampWidth = (value: number) => Math.max(320, Math.min(360, Math.round(value)));

const readState = (): PanelState => {
  if (!isBrowser()) return DEFAULT_STATE;
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) return DEFAULT_STATE;
  try {
    const parsed = JSON.parse(raw) as Partial<PanelState>;
    const activeTab = parsed.activeTab === 'hints' || parsed.activeTab === 'notes' || parsed.activeTab === 'coach' || parsed.activeTab === 'checks'
      ? parsed.activeTab
      : DEFAULT_STATE.activeTab;
    return {
      isOpen: typeof parsed.isOpen === 'boolean' ? parsed.isOpen : DEFAULT_STATE.isOpen,
      activeTab,
      width: typeof parsed.width === 'number' ? clampWidth(parsed.width) : DEFAULT_STATE.width,
    };
  } catch {
    return DEFAULT_STATE;
  }
};

const writeState = (state: PanelState) => {
  if (!isBrowser()) return;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
};

const notify = (state: PanelState) => {
  subscribers.forEach((subscriber) => subscriber(state));
};

export const getPanelState = () => readState();

export const setPanelState = (patch: Partial<PanelState>) => {
  const current = readState();
  const next: PanelState = {
    ...current,
    ...patch,
    width: typeof patch.width === 'number' ? clampWidth(patch.width) : current.width,
  };
  writeState(next);
  notify(next);
  return next;
};

export const subscribePanel = (listener: Subscriber) => {
  subscribers.add(listener);
  listener(readState());
  return () => {
    subscribers.delete(listener);
  };
};
