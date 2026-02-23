import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

type MappedCollection = 'labs' | 'quizzes' | 'activities' | 'lessons';

type Violation = {
  track: string;
  moduleKey: string;
  collection: MappedCollection;
  slug: string;
  message: string;
};

const normalize = (value: unknown) => (typeof value === 'string' ? value.trim() : '');

const contentRoot = fileURLToPath(new URL('../../content/', import.meta.url));

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
      if (entry.isFile() && /\.mdx?$/i.test(entry.name)) {
        results.push(fullPath);
      }
    }
  }
  return results;
};

const stripQuotes = (value: string) => value.replace(/^['\"]|['\"]$/g, '').trim();

type Frontmatter = Record<string, string>;

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

type ContentEntry = {
  slug: string;
  data: Frontmatter;
};

const readCollection = (name: MappedCollection | 'modules'): ContentEntry[] => {
  const dir = path.join(contentRoot, name);
  return listMdxFiles(dir).map((filePath) => {
    const data = readFrontmatter(filePath);
    const relative = path.relative(dir, filePath).replace(/\\/g, '/');
    const fallbackSlug = relative.replace(/\.mdx?$/i, '');
    const slug = normalize(data.slug) || fallbackSlug;
    return { slug, data };
  });
};

const sortViolations = (a: Violation, b: Violation) => {
  return (
    a.track.localeCompare(b.track) ||
    a.moduleKey.localeCompare(b.moduleKey) ||
    a.collection.localeCompare(b.collection) ||
    a.slug.localeCompare(b.slug) ||
    a.message.localeCompare(b.message)
  );
};

export const assertModuleInvariants = async (): Promise<void> => {
  const modules = readCollection('modules');
  const labs = readCollection('labs');
  const quizzes = readCollection('quizzes');
  const activities = readCollection('activities');
  const lessons = readCollection('lessons');

  const allowedModulesByTrack = new Map<string, Set<string>>();

  for (const moduleEntry of modules) {
    const track = normalize(moduleEntry.data.track);
    if (!track) continue;

    const keys = [normalize(moduleEntry.slug), normalize(moduleEntry.data.moduleId)].filter(Boolean);
    if (!allowedModulesByTrack.has(track)) {
      allowedModulesByTrack.set(track, new Set<string>());
    }
    const set = allowedModulesByTrack.get(track)!;
    for (const key of keys) set.add(key);
  }

  const violations: Violation[] = [];

  const pushViolation = (
    collection: MappedCollection,
    slug: string,
    track: string,
    moduleKey: string,
    message: string
  ) => {
    violations.push({
      collection,
      slug,
      track,
      moduleKey,
      message,
    });
  };

  const validateMapped = (collection: Exclude<MappedCollection, 'lessons'>, entries: ContentEntry[]) => {
    for (const entry of entries) {
      const track = normalize(entry.data.track);
      const moduleId = normalize(entry.data.moduleId);
      const module = normalize(entry.data.module);
      const moduleKey = moduleId || module;

      if (!track) {
        pushViolation(collection, entry.slug, '', moduleKey, 'track is required');
        continue;
      }

      if (!moduleKey) {
        pushViolation(collection, entry.slug, track, '', 'moduleId/module is required');
        continue;
      }

      const allowed = Array.from(allowedModulesByTrack.get(track) ?? []).sort();
      if (!allowed.includes(moduleKey)) {
        pushViolation(
          collection,
          entry.slug,
          track,
          moduleKey,
          `moduleId=${moduleKey} not found in track modules: [${allowed.join(', ')}]`
        );
      }
    }
  };

  validateMapped('labs', labs);
  validateMapped('quizzes', quizzes);
  validateMapped('activities', activities);

  for (const lesson of lessons) {
    const track = normalize(lesson.data.track);
    if (!track) continue;

    const moduleId = normalize(lesson.data.moduleId);
    const module = normalize(lesson.data.module);
    const moduleKey = moduleId || module;
    if (!moduleKey) continue;

    const allowed = Array.from(allowedModulesByTrack.get(track) ?? []).sort();
    if (!allowed.includes(moduleKey)) {
      pushViolation(
        'lessons',
        lesson.slug,
        track,
        moduleKey,
        `moduleId=${moduleKey} not found in track modules: [${allowed.join(', ')}]`
      );
    }
  }

  if (violations.length === 0) return;

  const lines = violations.sort(sortViolations).map((violation) => {
    const track = violation.track || '<missing>';
    const moduleKey = violation.moduleKey || '<missing>';
    return `[track=${track}] slug=${violation.collection}/${violation.slug} moduleId=${moduleKey} ${violation.message}`;
  });

  throw new Error(`Module invariants failed (${lines.length}):\n${lines.join('\n')}`);
};
