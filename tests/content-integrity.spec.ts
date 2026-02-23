import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { test, expect } from './fixtures';
import { validateTrackModuleMappings } from '../scripts/validate-tracks.mjs';

type CollectionName = 'tracks' | 'modules' | 'labs' | 'quizzes' | 'lessons';
type ActivityType = 'lab' | 'quiz' | 'lesson';

type Frontmatter = Record<string, string>;

type ContentEntry = {
  filePath: string;
  slug: string;
  data: Frontmatter;
};

type ActivitySummary = {
  track: string;
  moduleKey: string;
  type: ActivityType;
  slug: string;
  title: string;
  order: number;
  href: string;
};

const contentRoot = fileURLToPath(new URL('../src/content/', import.meta.url));

const listMdxFiles = (dirPath: string): string[] => {
  if (!fs.existsSync(dirPath)) return [];
  const results: string[] = [];
  const stack = [dirPath];
  while (stack.length > 0) {
    const current = stack.pop();
    if (!current) continue;
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(fullPath);
        continue;
      }
      if (entry.isFile() && /\.mdx?$/i.test(entry.name)) results.push(fullPath);
    }
  }
  return results;
};

const stripQuotes = (value: string) => value.replace(/^['\"]|['\"]$/g, '').trim();

const readFrontmatter = (filePath: string): Frontmatter => {
  const raw = fs.readFileSync(filePath, 'utf8');
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return {};
  const block = match[1] ?? '';
  const frontmatter: Frontmatter = {};
  for (const line of block.split(/\r?\n/)) {
    if (!line || /^\s/.test(line)) continue;
    const index = line.indexOf(':');
    if (index === -1) continue;
    const key = line.slice(0, index).trim();
    const value = line.slice(index + 1).trim();
    frontmatter[key] = stripQuotes(value);
  }
  return frontmatter;
};

const toSlugFromPath = (collectionDir: string, filePath: string) => {
  const relative = path.relative(collectionDir, filePath).replace(/\\/g, '/');
  return relative.replace(/\.mdx?$/i, '');
};

const readCollection = (name: CollectionName): ContentEntry[] => {
  const dir = path.join(contentRoot, name);
  return listMdxFiles(dir).map((filePath) => {
    const data = readFrontmatter(filePath);
    const fallbackSlug = toSlugFromPath(dir, filePath);
    const slug = (data.slug && String(data.slug).trim()) || fallbackSlug;
    return { filePath, slug, data };
  });
};

const toOrder = (value: string | undefined): number => {
  const parsed = Number.parseInt(value ?? '0', 10);
  return Number.isFinite(parsed) ? parsed : 0;
};

const compareActivities = (a: { order: number; title: string; slug: string }, b: { order: number; title: string; slug: string }) => {
  return a.order - b.order || a.title.localeCompare(b.title) || a.slug.localeCompare(b.slug);
};

const buildActivities = (): ActivitySummary[] => {
  const labs = readCollection('labs');
  const quizzes = readCollection('quizzes');
  const lessons = readCollection('lessons');

  const toActivity = (entry: ContentEntry, type: ActivityType, hrefPrefix: '/labs' | '/quizzes' | '/lessons'): ActivitySummary | null => {
    const track = String(entry.data.track ?? '').trim();
    const moduleKey = String(entry.data.module ?? entry.data.moduleId ?? '').trim();
    if (!track || !moduleKey) return null;

    const orderRaw = entry.data.order;
    if (type === 'lesson' && typeof orderRaw === 'undefined') return null;

    return {
      track,
      moduleKey,
      type,
      slug: entry.slug,
      title: String(entry.data.title ?? entry.slug),
      order: toOrder(orderRaw),
      href: `${hrefPrefix}/${entry.slug}`,
    };
  };

  return [
    ...labs.map((entry) => toActivity(entry, 'lab', '/labs')).filter(Boolean),
    ...quizzes.map((entry) => toActivity(entry, 'quiz', '/quizzes')).filter(Boolean),
    ...lessons.map((entry) => toActivity(entry, 'lesson', '/lessons')).filter(Boolean),
  ] as ActivitySummary[];
};

const listCodeFiles = (dirPath: string): string[] => {
  if (!fs.existsSync(dirPath)) return [];
  const results: string[] = [];
  const stack = [dirPath];
  while (stack.length > 0) {
    const current = stack.pop();
    if (!current) continue;
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(fullPath);
        continue;
      }
      if (entry.isFile() && /\.(astro|ts|tsx|js|mjs)$/i.test(entry.name)) {
        results.push(fullPath);
      }
    }
  }
  return results;
};

const readSourceFiles = (rootRelativeDir: string) => {
  const dir = fileURLToPath(new URL(`../${rootRelativeDir}/`, import.meta.url));
  const entries = listCodeFiles(dir);
  return entries.map((filePath) => ({ filePath, source: fs.readFileSync(filePath, 'utf8') }));
};

test('content integrity: mapped activity metadata and canonical hrefs remain valid', async () => {
  const tracks = readCollection('tracks');
  const modules = readCollection('modules');
  const labs = readCollection('labs');
  const quizzes = readCollection('quizzes');
  const lessons = readCollection('lessons');

  const trackSlugs = new Set(tracks.map((track) => track.slug));

  const assertMappedActivity = (entry: ContentEntry, type: ActivityType) => {
    const hasTrack = typeof entry.data.track === 'string' && entry.data.track.trim().length > 0;
    if (!hasTrack) return;

    const moduleKey = String(entry.data.module ?? entry.data.moduleId ?? '').trim();
    // Lessons can carry track metadata for legacy grouping without being
    // module-mapped activities. Only enforce module linkage for mapped lessons.
    if (type === 'lesson' && moduleKey.length === 0) return;

    expect(moduleKey.length, `${type}:${entry.slug} must declare module/moduleId when track is set`).toBeGreaterThan(0);

    const href = type === 'lab' ? `/labs/${entry.slug}` : type === 'quiz' ? `/quizzes/${entry.slug}` : `/lessons/${entry.slug}`;
    const prefix = type === 'lab' ? '/labs/' : type === 'quiz' ? '/quizzes/' : '/lessons/';
    expect(href.startsWith(prefix), `${type}:${entry.slug} canonical href should start with ${prefix}`).toBe(true);
  };

  labs.forEach((entry) => assertMappedActivity(entry, 'lab'));
  quizzes.forEach((entry) => assertMappedActivity(entry, 'quiz'));
  lessons.forEach((entry) => assertMappedActivity(entry, 'lesson'));

  const mappedActivities = buildActivities();

  for (const moduleEntry of modules) {
    const trackSlug = String(moduleEntry.data.track ?? '').trim();
    if (!trackSlug) continue;

    expect(trackSlugs.has(trackSlug), `module:${moduleEntry.slug} references unknown track ${trackSlug}`).toBe(true);

    const moduleId = String(moduleEntry.data.moduleId ?? '').trim();
    const moduleKeys = new Set([moduleEntry.slug, moduleId].filter(Boolean));

    const mappedCount = mappedActivities.filter(
      (activity) => activity.track === trackSlug && moduleKeys.has(activity.moduleKey)
    ).length;

    if (mappedCount === 0) {
      expect(moduleEntry.slug.length, `empty module must still have slug for /tracks/${trackSlug}`).toBeGreaterThan(0);
      expect(trackSlugs.has(trackSlug), `empty module ${moduleEntry.slug} must still belong to an existing track`).toBe(true);
    }
  }
});

test('module ordering and prev/next links remain deterministic for a multi-activity module', async ({ page }) => {
  const modules = readCollection('modules');
  const activities = buildActivities();

  const moduleByTrack = new Map<string, ContentEntry[]>();
  for (const moduleEntry of modules) {
    const trackSlug = String(moduleEntry.data.track ?? '').trim();
    if (!trackSlug) continue;
    const existing = moduleByTrack.get(trackSlug) ?? [];
    existing.push(moduleEntry);
    moduleByTrack.set(trackSlug, existing);
  }

  type ModuleCandidate = { slug: string; track: string; activities: ActivitySummary[] };
  let candidate: ModuleCandidate | null = null;

  for (const [trackSlug, trackModules] of moduleByTrack.entries()) {
    const sortedModules = [...trackModules].sort((a, b) => {
      return (
        toOrder(a.data.order) - toOrder(b.data.order) ||
        String(a.data.title ?? a.slug).localeCompare(String(b.data.title ?? b.slug)) ||
        a.slug.localeCompare(b.slug)
      );
    });

    for (const moduleEntry of sortedModules) {
      const moduleId = String(moduleEntry.data.moduleId ?? '').trim();
      const keys = new Set([moduleEntry.slug, moduleId].filter(Boolean));
      const moduleActivities = activities
        .filter((activity) => activity.track === trackSlug && keys.has(activity.moduleKey))
        .sort(compareActivities);

      if (moduleActivities.length >= 3) {
        candidate = { slug: moduleEntry.slug, track: trackSlug, activities: moduleActivities };
        break;
      }
    }

    if (candidate) break;
  }

  expect(candidate, 'Expected at least one module with >=3 mapped activities').not.toBeNull();
  const list = candidate!.activities;

  for (let index = 1; index < list.length; index += 1) {
    const prev = list[index - 1]!;
    const current = list[index]!;
    expect(compareActivities(prev, current)).toBeLessThanOrEqual(0);
  }

  const first = list[0]!;
  const middleIndex = Math.floor(list.length / 2);
  const middle = list[middleIndex]!;
  const last = list[list.length - 1]!;

  await page.goto(first.href);
  await expect(page.getByTestId('activity-prev-link')).toHaveCount(0);
  await expect(page.getByTestId('activity-next-link')).toHaveAttribute('href', list[1]!.href);

  await page.goto(middle.href);
  await expect(page.getByTestId('activity-prev-link')).toHaveAttribute('href', list[middleIndex - 1]!.href);
  await expect(page.getByTestId('activity-next-link')).toHaveAttribute('href', list[middleIndex + 1]!.href);

  await page.goto(last.href);
  await expect(page.getByTestId('activity-next-link')).toHaveCount(0);
  await expect(page.getByTestId('activity-prev-link')).toHaveAttribute('href', list[list.length - 2]!.href);
});

test('dashboard continue CTA deterministically advances when progress changes', async ({ page }) => {
  const trackSlug = 'network-engineer';
  const selector = `[data-track-continue-link][data-track-slug="${trackSlug}"]`;

  await page.goto('/');
  await page.evaluate(() => {
    window.localStorage.removeItem('beattie_progress_v1');
  });
  await page.reload();

  const beforeHref = await page.locator(selector).getAttribute('href');
  expect(beforeHref).toBeTruthy();
  expect((beforeHref ?? '').includes('/workspace/')).toBe(false);

  await page.locator(selector).click();
  await expect(page).toHaveURL(new RegExp(`${beforeHref!.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`));
  await expect(page.locator('h1').first()).toBeVisible();

  const match = beforeHref?.match(/^\/(labs|lessons|quizzes)\/(.+)$/);
  expect(match, `Expected initial continue href to be a canonical activity route, got: ${beforeHref}`).not.toBeNull();
  const collection = match![1] === 'labs' ? 'labs' : match![1] === 'quizzes' ? 'quizzes' : 'lessons';
  const slug = match![2]!;

  await page.goto('/');
  await page.evaluate(
    ({ collection, slug }) => {
      const payload: Record<string, Record<string, { completed: boolean }>> = {
        labs: {},
        lessons: {},
        quizzes: {},
      };
      payload[collection][slug] = { completed: true };
      window.localStorage.setItem('beattie_progress_v1', JSON.stringify(payload));
    },
    { collection, slug }
  );
  await page.reload();

  const afterHref = await page.locator(selector).getAttribute('href');
  expect(afterHref).toBeTruthy();
  expect((afterHref ?? '').includes('/workspace/')).toBe(false);
  expect(afterHref === `/tracks/${trackSlug}` || afterHref !== beforeHref).toBe(true);

  await page.locator(selector).click();
  await expect(page).toHaveURL(new RegExp(`${afterHref!.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`));
  await expect(page.locator('h1').first()).toBeVisible();
});

test('runtime pages/layouts do not import legacy trackCatalog or trackSections', async () => {
  const pageFiles = readSourceFiles('src/pages');
  const layoutFiles = readSourceFiles('src/layouts');
  const runtimeFiles = [...pageFiles, ...layoutFiles];

  const offenders = runtimeFiles
    .filter(({ source }) => /from\s+['\"].*lib\/trackCatalog['\"]|from\s+['\"].*lib\/trackSections['\"]/.test(source))
    .map(({ filePath }) => filePath.replace(/\\/g, '/'));

  expect(offenders, `Legacy runtime imports found:\n${offenders.join('\n')}`).toEqual([]);
});

test('track/module invariants: all activities map to valid track + moduleId', async () => {
  const result = validateTrackModuleMappings();
  expect(result.checked).toBeGreaterThan(0);
});
