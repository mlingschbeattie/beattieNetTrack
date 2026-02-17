import fs from 'node:fs/promises';
import path from 'node:path';

const MARKER = '<!-- AUTO-GENERATED: generate-tracks-from-lessons.mjs -->';

const args = process.argv.slice(2);
const hasFlag = (flag) => args.includes(flag);
const dryRun = hasFlag('--dryRun');
const forceAutoOnly = hasFlag('--forceAutoOnly');

const lessonsDir = path.resolve('src', 'content', 'lessons');
const tracksDir = path.resolve('src', 'content', 'tracks');

const parseFrontmatter = (content) => {
  const match = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  if (!match) return {};
  const body = match[1];
  const lines = body.split('\n');
  const data = {};
  for (const line of lines) {
    const [key, ...rest] = line.split(':');
    if (!key || rest.length === 0) continue;
    const value = rest.join(':').trim();
    data[key.trim()] = value.replace(/^"|"$/g, '');
  }
  return data;
};

const readLessonSlugs = async () => {
  const entries = await fs.readdir(lessonsDir, { withFileTypes: true });
  const files = entries.filter((entry) => entry.isFile() && entry.name.endsWith('.mdx'));
  const slugs = [];

  for (const entry of files) {
    const filePath = path.join(lessonsDir, entry.name);
    const raw = await fs.readFile(filePath, 'utf-8');
    const fm = parseFrontmatter(raw);
    const fallbackSlug = path.basename(entry.name, path.extname(entry.name));
    const slug = fm.slug ? fm.slug.replace(/^"|"$/g, '') : fallbackSlug;
    slugs.push(slug);
  }

  return slugs.sort((a, b) => a.localeCompare(b));
};

const buildTrackContent = ({ slug, title, description, order, sections }) => {
  const sectionsYaml = sections
    .map((section) => {
      const lessons = section.lessons.map((lesson) => `      - ${lesson}`).join('\n');
      return `  - title: ${section.title}\n    lessons:\n${lessons}`;
    })
    .join('\n');

  return `---\n` +
    `title: ${title}\n` +
    `description: ${description}\n` +
    `slug: ${slug}\n` +
    `order: ${order}\n` +
    `sections:\n${sectionsYaml}\n` +
    `---\n\n` +
    `${MARKER}\n`;
};

const writeTrack = async (fileName, content) => {
  const outPath = path.join(tracksDir, fileName);
  const exists = await fs
    .access(outPath)
    .then(() => true)
    .catch(() => false);

  if (exists && forceAutoOnly) {
    const existing = await fs.readFile(outPath, 'utf-8');
    if (!existing.includes(MARKER)) {
      return 'skipped-manual';
    }
  } else if (exists && !forceAutoOnly && !dryRun) {
    return 'skipped-exists';
  }

  if (!dryRun) {
    await fs.mkdir(tracksDir, { recursive: true });
    await fs.writeFile(outPath, content, 'utf-8');
  }

  return 'written';
};

const run = async () => {
  const lessonSlugs = await readLessonSlugs();
  const grouped = lessonSlugs.reduce((acc, slug) => {
    const key = slug.includes('-') ? slug.split('-')[0] : 'other';
    acc[key] ??= [];
    acc[key].push(slug);
    return acc;
  }, {});

  const groupedSections = Object.entries(grouped)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, lessons]) => ({ title: key, lessons: lessons.sort((a, b) => a.localeCompare(b)) }));

  const allTrackContent = buildTrackContent({
    slug: 'legacy',
    title: 'Legacy Pages',
    description: 'Auto-generated index of legacy HTML pages while migration is in progress.',
    order: 999,
    sections: [{ title: 'All Pages', lessons: lessonSlugs }],
  });

  const groupedTrackContent = buildTrackContent({
    slug: 'legacy-grouped',
    title: 'Legacy Pages (Grouped)',
    description: 'Auto-generated grouping of legacy pages by prefix.',
    order: 998,
    sections: groupedSections,
  });

  const results = {
    legacy: await writeTrack('legacy.mdx', allTrackContent),
    grouped: await writeTrack('legacy-grouped.mdx', groupedTrackContent),
  };

  console.table(results);
};

run().catch((error) => {
  console.error('Track generation failed:', error);
  process.exit(1);
});
