import { LAB_TIER_VALUES, engineTier, shippedEngines } from './labEngines.js';

export type LabTier = (typeof LAB_TIER_VALUES)[number];
export type LabEngine = ReturnType<typeof shippedEngines>[number];

export type ValidationIssueCode =
  | 'LAB_MISSING_TIER'
  | 'LAB_INVALID_TIER'
  | 'LAB_MISSING_ENGINE'
  | 'LAB_INVALID_ENGINE'
  | 'LAB_ENGINE_TIER_MISMATCH';

export type ValidationIssue = {
  code: ValidationIssueCode;
  slug: string;
  message: string;
};

type LabMetadataInput = {
  tier?: unknown;
  engine?: unknown;
};

const allowedTiers: LabTier[] = [...LAB_TIER_VALUES];
const allowedEngines = shippedEngines();

const allowedTiersText = allowedTiers.join(' | ');
const allowedEnginesText = allowedEngines.join(' | ');

export const issueCodeOrder: Record<ValidationIssueCode, number> = {
  LAB_MISSING_TIER: 1,
  LAB_MISSING_ENGINE: 2,
  LAB_INVALID_TIER: 3,
  LAB_INVALID_ENGINE: 4,
  LAB_ENGINE_TIER_MISMATCH: 5,
};

export const compareValidationIssues = (a: ValidationIssue, b: ValidationIssue): number => {
  const slugCompare = a.slug.localeCompare(b.slug);
  if (slugCompare !== 0) return slugCompare;
  return (issueCodeOrder[a.code] ?? Number.MAX_SAFE_INTEGER) - (issueCodeOrder[b.code] ?? Number.MAX_SAFE_INTEGER);
};

const missingTierMessage = (slug: string) =>
  `[LAB_MISSING_TIER] Lab "${slug}" is missing required field "tier".\n` +
  `Allowed values: ${allowedTiersText}.\n` +
  `Action: Add \`tier\` to src/content/labs/${slug}.mdx frontmatter.`;

const invalidTierMessage = (slug: string, value: string) =>
  `[LAB_INVALID_TIER] Lab "${slug}" has invalid tier "${value}".\n` +
  `Allowed values: ${allowedTiersText}.\n` +
  'Action: Correct `tier` in frontmatter.';

const missingEngineMessage = (slug: string) =>
  `[LAB_MISSING_ENGINE] Lab "${slug}" is missing required field "engine".\n` +
  `Allowed values: ${allowedEnginesText}.\n` +
  `Action: Add \`engine\` to src/content/labs/${slug}.mdx frontmatter.`;

const invalidEngineMessage = (slug: string, value: string) =>
  `[LAB_INVALID_ENGINE] Lab "${slug}" declares engine "${value}" which is not currently supported.\n` +
  `Allowed values: ${allowedEnginesText}.\n` +
  'Action: Use a shipped engine or implement and register the new engine before declaring it.';

const mismatchMessage = (slug: string, engine: string, tier: string, requiredTier: string) =>
  `[LAB_ENGINE_TIER_MISMATCH] Lab "${slug}" declares engine "${engine}" but tier "${tier}".\n` +
  `Rule: engine "${engine}" requires tier "${requiredTier}".\n` +
  `Action: Either change tier to "${requiredTier}" or implement and register a matching engine.`;

const isTier = (value: string): value is LabTier => allowedTiers.includes(value as LabTier);
const isEngine = (value: string): value is LabEngine => allowedEngines.includes(value as LabEngine);

export const validateLabMetadata = (
  slug: string,
  data: LabMetadataInput,
  _fileHint?: string
): ValidationIssue[] => {
  const issues: ValidationIssue[] = [];

  const rawTier = typeof data.tier === 'string' ? data.tier.trim() : '';
  const rawEngine = typeof data.engine === 'string' ? data.engine.trim() : '';

  const tierMissing = rawTier.length === 0;
  const engineMissing = rawEngine.length === 0;

  if (tierMissing) {
    issues.push({
      code: 'LAB_MISSING_TIER',
      slug,
      message: missingTierMessage(slug),
    });
  }

  if (engineMissing) {
    issues.push({
      code: 'LAB_MISSING_ENGINE',
      slug,
      message: missingEngineMessage(slug),
    });
  }

  const tierIsValid = !tierMissing && isTier(rawTier);
  const engineIsValid = !engineMissing && isEngine(rawEngine);

  if (!tierMissing && !tierIsValid) {
    issues.push({
      code: 'LAB_INVALID_TIER',
      slug,
      message: invalidTierMessage(slug, rawTier),
    });
  }

  if (!engineMissing && !engineIsValid) {
    issues.push({
      code: 'LAB_INVALID_ENGINE',
      slug,
      message: invalidEngineMessage(slug, rawEngine),
    });
  }

  if (tierIsValid && engineIsValid) {
    const requiredTier = engineTier(rawEngine);
    if (rawTier === requiredTier) {
      return issues;
    }

    issues.push({
      code: 'LAB_ENGINE_TIER_MISMATCH',
      slug,
      message: mismatchMessage(slug, rawEngine, rawTier, requiredTier),
    });
  }

  return issues;
};

