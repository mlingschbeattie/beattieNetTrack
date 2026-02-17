import fs from 'node:fs/promises';
import path from 'node:path';

const args = process.argv.slice(2);
const getArg = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};

const inputPath = getArg('--input');
const outputPath = getArg('--output');
const titleArg = getArg('--title');
const slugArg = getArg('--slug');

if (!inputPath || !outputPath) {
  console.error('Usage: node scripts/legacy-html-to-mdx.mjs --input path/to/file.html --output src/content/lessons/slug.mdx [--title "Title"] [--slug "slug"]');
  process.exit(1);
}

const html = await fs.readFile(inputPath, 'utf-8');
const slug = slugArg ?? path.basename(inputPath, path.extname(inputPath));
const title = titleArg ?? slug.replace(/[-_]/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase());

const mdx = `---\n` +
  `title: ${title}\n` +
  `description: TODO\n` +
  `slug: ${slug}\n` +
  `track: TODO\n` +
  `order: 0\n` +
  `difficulty: Beginner\n` +
  `estMinutes: 10\n` +
  `tags: []\n` +
  `legacyUrl: /${path.basename(inputPath)}\n` +
  `---\n\n` +
  `<!-- TODO: Replace legacy HTML below with structured MDX content. -->\n\n` +
  '```html\n' +
  html.trim() +
  '\n```\n';

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, mdx, 'utf-8');

console.log(`Wrote ${outputPath}`);
