import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MARKER = '<!-- AUTO-GENERATED: migrate-batch.mjs -->';

const args = process.argv.slice(2);
const getArg = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};

const hasFlag = (flag) => args.includes(flag);

const inputDirArg = getArg('--inputDir');
const globPattern = getArg('--glob') ?? '**/*';
const outDirArg = getArg('--outDir');
const dryRun = hasFlag('--dryRun');
const force = hasFlag('--force');
const forceRoot = hasFlag('--forceRoot');
const forceAutoOnly = hasFlag('--forceAutoOnly');

const outDir = outDirArg ?? path.join('src', 'content', 'lessons');
const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRootDefault = path.resolve(scriptDir, '..', '..');
const inputDir = inputDirArg ?? repoRootDefault;
const resolvedInput = path.resolve(inputDir);
const resolvedOut = path.resolve(outDir);
const mappingPath = path.resolve('scripts', 'migration-map.json');

const escapeHtml = (value) => value.replace(/</g, '&lt;').replace(/>/g, '&gt;');

const extractTitleFromHtml = (html, fallback) => {
  const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
  if (titleMatch?.[1]) return titleMatch[1].trim();
  const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1Match?.[1]) {
    const text = h1Match[1].replace(/<[^>]+>/g, '').trim();
    if (text) return text;
  }
  return fallback;
};

const extractTitleFromMarkdown = (markdown, fallback) => {
  const match = markdown.match(/^#\s+(.+)$/m);
  return match?.[1]?.trim() || fallback;
};

const looksLikeMarkdown = (sample) =>
  /^#\s+/m.test(sample) ||
  /```/.test(sample) ||
  /^\s*[-*]\s+/m.test(sample) ||
  /\[[^\]]+\]\([^\)]+\)/.test(sample);

const globToRegex = (pattern) => {
  const escaped = pattern
    .replace(/[.+^${}()|[\]\\]/g, '\\$&')
    .replace(/\*\*/g, '.*')
    .replace(/\*/g, '[^/]*')
    .replace(/\?/g, '.');
  return new RegExp(`^${escaped}$`, 'i');
};

const escapeTemplateLiteral = (value) =>
  value
    .replace(/\\/g, '\\\\')
    .replace(/`/g, '\\`')
    .replace(/\$\{/g, '\\${');

const sanitizeSlug = (value) =>
  value
    .toLowerCase()
    .replace(/[^a-z0-9-_]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/--+/g, '-');

const ensureDir = async (dir) => {
  await fs.mkdir(dir, { recursive: true });
};

const loadMapping = async () => {
  try {
    const raw = await fs.readFile(mappingPath, 'utf-8');
    return JSON.parse(raw);
  } catch {
    return {};
  }
};

const saveMapping = async (mapping) => {
  await ensureDir(path.dirname(mappingPath));
  await fs.writeFile(mappingPath, JSON.stringify(mapping, null, 2));
};

const ignoredDirs = new Set([
  '$Recycle.Bin',
  'System Volume Information',
  'Recovery',
  'Windows',
  'Program Files',
  'Program Files (x86)',
  '.git',
  'node_modules',
  '.venv',
  'dist',
  'build',
  '.astro',
  '.next',
]);

const shouldIgnore = (entryName) =>
  ignoredDirs.has(entryName) || entryName.startsWith('.') || entryName.startsWith('_');

const isDriveRoot = (dir) => {
  const resolved = path.resolve(dir);
  const parsed = path.parse(resolved);
  if (process.platform === 'win32') {
    return parsed.root.toLowerCase() === resolved.toLowerCase();
  }
  return resolved === parsed.root;
};

const readSample = async (filePath) => {
  const handle = await fs.open(filePath, 'r');
  const buffer = Buffer.alloc(2048);
  const { bytesRead } = await handle.read(buffer, 0, 2048, 0);
  await handle.close();
  return buffer.subarray(0, bytesRead).toString('utf-8');
};

const walkFiles = async (dir, matcher, skipReasons) => {
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch (error) {
    if (error?.code === 'EPERM' || error?.code === 'EACCES') {
      skipReasons.ignored += 1;
      return [];
    }
    throw error;
  }

  const results = [];
  for (const entry of entries) {
    if (shouldIgnore(entry.name)) {
      skipReasons.ignored += 1;
      continue;
    }
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...(await walkFiles(fullPath, matcher, skipReasons)));
      continue;
    }
    if (!entry.isFile()) continue;
    const relativePosix = path.relative(resolvedInput, fullPath).replace(/\\/g, '/');
    if (!matcher.test(relativePosix)) {
      continue;
    }
    results.push({ fullPath, relativePosix });
  }
  return results;
};

const generateSlug = (relativePosixPath, usedSlugs) => {
  const withoutExt = relativePosixPath.replace(/\.[^/.]+$/, '');
  const raw = withoutExt.replace(/\//g, '-');
  let slug = sanitizeSlug(raw);
  let counter = 2;
  while (usedSlugs.has(slug)) {
    slug = `${sanitizeSlug(raw)}-${counter}`;
    counter += 1;
  }
  usedSlugs.add(slug);
  return slug;
};

const run = async () => {
  if (isDriveRoot(resolvedInput) && !forceRoot) {
    console.error(
      `Refusing to scan drive root: ${resolvedInput}. Use --forceRoot to proceed intentionally.`
    );
    process.exit(1);
  }

  const matcher = globToRegex(globPattern);
  const skipReasons = { exists: 0, ignored: 0, unknownNoExt: 0, manual: 0 };
  const matched = await walkFiles(resolvedInput, matcher, skipReasons);
  const mapping = await loadMapping();
  const summary = { matched: matched.length, migrated: 0, skipped: 0, errors: 0 };
  const usedSlugs = new Set();

  await ensureDir(resolvedOut);

  for (const { fullPath, relativePosix } of matched) {
    const ext = path.extname(fullPath).toLowerCase();
    const hasExt = Boolean(ext);
    const isMarkdown = ext === '.md' || ext === '.markdown';
    const isHtml = ext === '.html';

    let treatAsMarkdown = isMarkdown;
    if (!hasExt) {
      try {
        const sample = await readSample(fullPath);
        treatAsMarkdown = looksLikeMarkdown(sample);
      } catch {
        treatAsMarkdown = false;
      }
      if (!treatAsMarkdown) {
        skipReasons.unknownNoExt += 1;
        summary.skipped += 1;
        continue;
      }
    }

    if (!isHtml && !treatAsMarkdown) {
      summary.skipped += 1;
      continue;
    }

    const rawSlugBase = relativePosix.replace(/\.[^/.]+$/, '');
    const slug = generateSlug(rawSlugBase, usedSlugs);
    const outputPath = path.resolve(resolvedOut, `${slug}.mdx`);
    const legacyUrl = `/${relativePosix}`;

    try {
      if (!outputPath.startsWith(resolvedOut)) {
        summary.errors += 1;
        continue;
      }

      const exists = await fs
        .access(outputPath)
        .then(() => true)
        .catch(() => false);

      if (exists && !force) {
        if (forceAutoOnly) {
          const existing = await fs.readFile(outputPath, 'utf-8');
          if (!existing.includes(MARKER)) {
            skipReasons.manual += 1;
            summary.skipped += 1;
            continue;
          }
        } else {
          skipReasons.exists += 1;
          summary.skipped += 1;
          continue;
        }
      }

      const rawContent = await fs.readFile(fullPath, 'utf-8');
      const fallbackTitle = path.basename(relativePosix, path.extname(relativePosix));
      const title = isHtml
        ? extractTitleFromHtml(rawContent, fallbackTitle)
        : extractTitleFromMarkdown(rawContent, fallbackTitle);

      let body = rawContent;
      if (isHtml) {
        const escaped = escapeTemplateLiteral(rawContent.trim());
        body = `import LegacyHtml from '../../components/LegacyHtml.astro';\n\n` +
          `<LegacyHtml>\n` +
          `{\`${escaped}\`}\n` +
          `</LegacyHtml>\n`;
      }

      const content = `---\n` +
        `title: ${escapeHtml(title)}\n` +
        `slug: ${slug}\n` +
        `sourcePath: "${relativePosix}"\n` +
        `legacyUrl: "${legacyUrl}"\n` +
        `difficulty: "medium"\n` +
        `estimatedMinutes: 15\n` +
        `---\n\n` +
        `${MARKER}\n\n` +
        `${body.trim()}\n`;

      if (!dryRun) {
        await fs.writeFile(outputPath, content, 'utf-8');
      }

      mapping[legacyUrl] = slug;
      summary.migrated += 1;
    } catch (error) {
      summary.errors += 1;
      console.error(`Error migrating ${relativePosix}:`, error);
    }
  }

  if (!dryRun) {
    await saveMapping(mapping);
  }

  console.log(`Matched files: ${summary.matched}`);
  console.table(summary);
  console.table(
    Object.entries(skipReasons).map(([reason, count]) => ({ reason, count }))
  );
};

run().catch((error) => {
  console.error('Migration failed:', error);
  process.exit(1);
});
