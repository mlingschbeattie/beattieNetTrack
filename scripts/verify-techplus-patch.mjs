import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

// 1. Check content files
const repoRoot = path.resolve('.');
const lessonsDir = path.join(repoRoot, 'src', 'content', 'lessons');
const quizzesDir = path.join(repoRoot, 'src', 'content', 'quizzes', 'tech-plus');

const tpLessons = fs.readdirSync(lessonsDir).filter(f => f.startsWith('tech-plus-'));
const tpQuizzes = fs.readdirSync(quizzesDir).filter(f => f.startsWith('tech-plus-'));

console.log('=== Tech+ Content Verification ===');
console.log(`Lessons found: ${tpLessons.length} (expected 58)`);
console.log(`Quizzes found: ${tpQuizzes.length} (expected 58)`);

if (tpLessons.length !== 58 || tpQuizzes.length !== 58) {
  console.error('FAIL: Expected 58 lessons and 58 quizzes');
  process.exit(1);
}

const lessonSlugs = new Set(tpLessons.map(f => f.replace('.mdx', '')));
const quizSlugs = new Set(tpQuizzes.map(f => f.replace('.mdx', '')));

// Check 1-to-1 match
for (const slug of quizSlugs) {
  if (!lessonSlugs.has(slug)) {
    console.error(`FAIL: Orphaned quiz found without lesson: ${slug}`);
    process.exit(1);
  }
}
console.log('PASS: All 58 quizzes have an exact matching lesson.');

// Specifically check Storage Units and Troubleshooting Methodology
const storageLesson = 'tech-plus-1-3-1-storage-units';
const storageQuiz = 'tech-plus-1-3-1-storage-units';
const troubleLesson = 'tech-plus-1-4-1-troubleshooting-methodology';
const troubleQuiz = 'tech-plus-1-4-1-troubleshooting-methodology';

if (!lessonSlugs.has(storageLesson) || !quizSlugs.has(storageQuiz)) {
  console.error('FAIL: Storage Units lesson or quiz missing!');
  process.exit(1);
}
if (!lessonSlugs.has(troubleLesson) || !quizSlugs.has(troubleQuiz)) {
  console.error('FAIL: Troubleshooting Methodology lesson or quiz missing!');
  process.exit(1);
}
console.log('PASS: "Storage Units" and "Troubleshooting Methodology" both exist in lessons and quizzes.');

// 2. Check built AppShell chunk & TrackModuleSummary
const chunksDir = path.resolve('dist', 'server', 'chunks');
const appShellFile = fs.readdirSync(chunksDir).find(f => f.startsWith('AppShell_') && f.endsWith('.mjs'));
const appShellUrl = pathToFileURL(path.join(chunksDir, appShellFile)).href;
const appShellMod = await import(appShellUrl);
const getTrackDetailData =
  appShellMod.getTrackDetailData ||
  Object.values(appShellMod).find(fn => typeof fn === 'function' && fn.name === 'getTrackDetailData');

const detail = await getTrackDetailData('tech-plus');
if (!detail) {
  console.error('FAIL: Failed to load tech-plus detail');
  process.exit(1);
}

console.log(`\n=== Tech+ Modules & Activities Verification ===`);
console.log(`Modules count: ${detail.modules.length} (expected 6)`);
const totalActs = detail.modules.reduce((sum, m) => sum + m.activities.length, 0);
console.log(`Total activities count: ${totalActs} (expected 116)`);

if (totalActs !== 116) {
  console.error(`FAIL: Total activities count is ${totalActs}, expected 116`);
  process.exit(1);
}

// 3. Check that for every single pair in every module, lesson precedes quiz
for (const mod of detail.modules) {
  console.log(`\nChecking Module: ${mod.slug} (${mod.activities.length} activities)`);
  for (let i = 0; i < mod.activities.length; i += 2) {
    const first = mod.activities[i];
    const second = mod.activities[i + 1];

    if (!first || !second) {
      console.error(`FAIL: Unpaired activity at index ${i} in module ${mod.slug}`);
      process.exit(1);
    }

    if (first.type !== 'lesson') {
      console.error(`FAIL: Expected lesson first, got ${first.type} (${first.slug}) at index ${i}`);
      process.exit(1);
    }
    if (second.type !== 'quiz') {
      console.error(`FAIL: Expected quiz second, got ${second.type} (${second.slug}) at index ${i + 1}`);
      process.exit(1);
    }

    if (first.order !== second.order) {
      console.error(`FAIL: Order mismatch between lesson (${first.order}) and quiz (${second.order}) for ${first.slug}`);
      process.exit(1);
    }

    if (first.slug !== second.slug) {
      console.error(`FAIL: Slug mismatch between lesson (${first.slug}) and quiz (${second.slug})`);
      process.exit(1);
    }
  }
  console.log(`  ✓ All ${mod.activities.length / 2} concepts in ${mod.slug} strictly follow: [Core Lesson] -> [Checkpoint Quiz]`);
}

console.log('\n===============================================================');
console.log('ALL VERIFICATION CHECKS PASSED: 100% SUCCESS');
console.log('===============================================================');
