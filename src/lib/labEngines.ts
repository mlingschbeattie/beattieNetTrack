export const LAB_TIER_VALUES = ['guided', 'state-machine', 'sandbox'] as const;
export type LabTier = (typeof LAB_TIER_VALUES)[number];

export const LAB_ENGINES = {
  'sim-reference-checks': {
    tier: 'sandbox',
    label: 'Reference Checks Simulator',
    shipped: true,
  },
  'sim-sandbox-terminal': {
    tier: 'sandbox',
    label: 'Terminal Sandbox Simulator',
    shipped: true,
  },
  steps: {
    tier: 'guided',
    label: 'Guided Runner (step validator)',
    shipped: true,
  },
} as const;

export type LabEngine = keyof typeof LAB_ENGINES;

export function shippedEngines(): LabEngine[] {
  return (Object.keys(LAB_ENGINES) as LabEngine[])
    .filter((engine) => LAB_ENGINES[engine].shipped)
    .sort((a, b) => a.localeCompare(b));
}

export function engineTier(engine: LabEngine): LabTier {
  return LAB_ENGINES[engine].tier;
}