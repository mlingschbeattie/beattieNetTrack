import type { WorkspaceResultPayload } from './workspaceResultContract.ts';

export const referenceChecksPayloadForAction = (
  slug: string,
  action: 'run' | 'check' | 'submit' | 'reset'
): WorkspaceResultPayload => {
  if (action === 'run') {
    return {
      slug,
      action,
      passed: true,
      progress: 0.25,
      message: 'Reference run complete',
    };
  }

  if (action === 'check') {
    return {
      slug,
      action,
      passed: false,
      progress: 0.5,
      message: 'Reference checks found one failing condition',
      checks: [
        {
          id: 'ref-check-1',
          label: 'Primary invariant',
          pass: true,
          message: 'Invariant met',
        },
        {
          id: 'ref-check-2',
          label: 'Secondary invariant',
          pass: false,
          message: 'Invariant not met',
        },
      ],
    };
  }

  if (action === 'submit') {
    return {
      slug,
      action,
      passed: true,
      progress: 1,
      message: 'Reference submit complete',
    };
  }

  return {
    slug,
    action,
    passed: false,
    progress: 0,
    message: 'Reference state reset',
  };
};
