import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');
const contentRoot = path.join(repoRoot, 'src', 'content');
const legacyRoot = path.join(repoRoot, 'public', 'legacy');

const requiredCollectionDirs = ['labs', 'quizzes', 'activities', 'lessons'];
const optionalCollectionDirs = ['terminal', 'code', 'tour', 'tours', 'assessments'];

const stripQuotes = (value) => value.replace(/^['"]|['"]$/g, '').trim();

const readFrontmatter = (filePath) => {
  const raw = fs.readFileSync(filePath, 'utf8');
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;
  const block = match[1];
  const frontmatter = {};
  const lines = block.split(/\r?\n/);
  for (const line of lines) {
    if (!line || /^\s/.test(line)) continue;
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;
    const key = line.slice(0, colonIndex).trim();
    const value = line.slice(colonIndex + 1).trim();
    frontmatter[key] = stripQuotes(value);
  }
  return frontmatter;
};

const listMdxFiles = (dirPath) => {
  if (!fs.existsSync(dirPath)) return [];
  const results = [];
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

const tracksDir = path.join(contentRoot, 'tracks');
const modulesDir = path.join(contentRoot, 'modules');

export const validateTrackModuleMappings = () => {
  const trackFiles = listMdxFiles(tracksDir).sort((a, b) => a.localeCompare(b));
  const moduleFiles = listMdxFiles(modulesDir).sort((a, b) => a.localeCompare(b));

  const trackSlugs = new Set();
  for (const filePath of trackFiles) {
    const fm = readFrontmatter(filePath);
    if (!fm) continue;
    const slug = fm.slug;
    if (slug) trackSlugs.add(slug);
  }

  const modulesById = new Map();
  const moduleIdCollisions = [];
  for (const filePath of moduleFiles) {
    const fm = readFrontmatter(filePath);
    if (!fm) continue;
    const moduleId = fm.moduleId;
    const moduleTrack = fm.track;
    if (!moduleId || !moduleTrack) continue;
    if (modulesById.has(moduleId)) {
      moduleIdCollisions.push({ moduleId, first: modulesById.get(moduleId).filePath, second: filePath });
    }
    modulesById.set(moduleId, { track: moduleTrack, filePath });
  }

  const collectionsToCheck = [
    ...requiredCollectionDirs.map((name) => ({ name, path: path.join(contentRoot, name) })),
    ...optionalCollectionDirs
      .map((name) => ({ name, path: path.join(contentRoot, name) }))
      .filter((entry) => fs.existsSync(entry.path)),
  ];

  const errors = [];
  const warnings = [];
  const checkedEntries = [];

  for (const collection of collectionsToCheck) {
    const files = listMdxFiles(collection.path).sort((a, b) => a.localeCompare(b));
    for (const filePath of files) {
      const fm = readFrontmatter(filePath);
      if (!fm) {
        errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} missing frontmatter block.`);
        continue;
      }

      const track = fm.track;
      const moduleId = fm.moduleId || fm.module;
      const orderRaw = fm.order;

      if (!track) {
        errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} missing required track.`);
      } else if (!trackSlugs.has(track)) {
        errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} track '${track}' does not match any track slug.`);
      }

      if (!moduleId) {
        errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} missing required moduleId.`);
      } else if (!modulesById.has(moduleId)) {
        errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} moduleId '${moduleId}' does not exist in modules collection.`);
      } else if (track && modulesById.get(moduleId).track !== track) {
        errors.push(
          `[${collection.name}] ${path.relative(repoRoot, filePath)} moduleId '${moduleId}' belongs to track '${modulesById.get(moduleId).track}', but entry track is '${track}'.`
        );
      }

      // Order is required for activities/quizzes/labs; optional for lessons
      if (collection.name !== 'lessons') {
        if (typeof orderRaw === 'undefined' || orderRaw === '') {
          errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} missing required order.`);
        } else if (!/^-?\d+$/.test(String(orderRaw))) {
          errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} order '${orderRaw}' is not an integer.`);
        }
      } else if (typeof orderRaw !== 'undefined' && orderRaw !== '' && !/^-?\d+$/.test(String(orderRaw))) {
        errors.push(`[${collection.name}] ${path.relative(repoRoot, filePath)} order '${orderRaw}' is not an integer.`);
      }


      const labPath = fm.labPath;
      if (labPath && /^\/legacy\//.test(labPath)) {
        const relativeLegacyPath = labPath.replace(/^\/legacy\//, '');
        const diskPath = path.join(legacyRoot, relativeLegacyPath);
        if (!fs.existsSync(diskPath)) {
          errors.push(
            `[${collection.name}] ${path.relative(repoRoot, filePath)} references missing legacy file '${labPath}' (expected ${path.relative(
              repoRoot,
              diskPath
            )}).`
          );
        }
      }

      const quizJsonPath = fm.quizJsonPath;
      if (quizJsonPath) {
        const quizDiskPath = path.join(repoRoot, 'public', quizJsonPath.replace(/^\//, ''));
        if (!fs.existsSync(quizDiskPath)) {
          errors.push(
            `[${collection.name}] ${path.relative(repoRoot, filePath)} references missing quizJsonPath '${quizJsonPath}' (expected ${path.relative(
              repoRoot,
              quizDiskPath
            )}).`
          );
        }
      }

      checkedEntries.push({ collection: collection.name, filePath });
    }
  }

  for (const collision of moduleIdCollisions) {
    errors.push(
      `[modules] moduleId collision '${collision.moduleId}' found in ${path.relative(repoRoot, collision.first)} and ${path.relative(repoRoot, collision.second)}.`
    );
  }

  const sortedWarnings = warnings.sort((a, b) => a.localeCompare(b));
  const sortedErrors = errors.sort((a, b) => a.localeCompare(b));
  if (sortedErrors.length > 0) {
    throw new Error(sortedErrors.join('\n'));
  }

  return {
    tracksDiscovered: trackSlugs.size,
    modulesDiscovered: modulesById.size,
    collectionsChecked: collectionsToCheck.map((item) => item.name),
    checked: checkedEntries.length,
    warnings: sortedWarnings,
  };
};

const isDirectRun = process.argv[1] ? path.resolve(process.argv[1]) === __filename : false;

if (isDirectRun) {
  try {
    const result = validateTrackModuleMappings();
    console.log('Track validation report');
    console.log('======================');
    console.log(`Tracks discovered: ${result.tracksDiscovered}`);
    console.log(`Modules discovered: ${result.modulesDiscovered}`);
    console.log(`Collections checked: ${result.collectionsChecked.join(', ')}`);
    console.log(`Entries checked: ${result.checked}`);

    if (result.warnings.length > 0) {
      console.log('\nWarnings:');
      for (const warning of result.warnings) {
        console.log(`- ${warning}`);
      }
    }

    console.log('\nValidation passed: all activity content is correctly mapped to track + moduleId.');
  } catch (error) {
    console.error('\nErrors:');
    const message = error instanceof Error ? error.message : String(error);
    for (const line of message.split('\n').filter(Boolean)) {
      console.error(`- ${line}`);
    }
    process.exit(1);
  }
}
