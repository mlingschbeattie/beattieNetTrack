import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');
const contentRoot = path.join(repoRoot, 'src', 'content');

const args = process.argv.slice(2);
const isStrict = args.includes('--strict');
const showDetails = args.includes('--details');
const trackFilter = args.find((a) => a.startsWith('--track='))?.split('=')[1];

function readFrontmatterAndBody(filePath) {
  const raw = fs.readFileSync(filePath, 'utf-8');
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return { frontmatter: {}, body: raw, raw };
  const block = match[1];
  const body = raw.slice(match[0].length);
  const lines = block.split(/\r?\n/);
  const frontmatter = {};
  for (const line of lines) {
    if (!line || /^\s/.test(line)) continue;
    const colon = line.indexOf(':');
    if (colon === -1) continue;
    const k = line.slice(0, colon).trim();
    const v = line.slice(colon + 1).trim();
    frontmatter[k] = v.replace(/^['"]|['"]$/g, '');
  }
  return { frontmatter, body, raw };
}

function scanDir(dir) {
  if (!fs.existsSync(dir)) return [];
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) results.push(...scanDir(p));
    else if (entry.name.endsWith('.md') || entry.name.endsWith('.mdx')) results.push(p);
  }
  return results;
}

// ─── 1. LESSON QUALITY EVALUATOR ─────────────────────────────────────────────
export function evaluateLessonQuality(filePath) {
  const { raw, body } = readFrontmatterAndBody(filePath);
  const rel = path.relative(repoRoot, filePath);
  let score = 0;
  const breakdown = [];
  const flags = [];

  const trackMatch = raw.match(/track:\s*['"]?([^'\n\r"]+)/);
  const track = trackMatch ? trackMatch[1].trim() : '';
  const moduleMatch = raw.match(/moduleId:\s*['"]?([^'\n\r"]+)/);
  const moduleId = moduleMatch ? moduleMatch[1].trim() : '';
  const orderMatch = raw.match(/order:\s*(\d+)/);
  const order = orderMatch ? parseInt(orderMatch[1], 10) : undefined;

  // If missing order, it's a utility or unindexed file
  if (typeof order === 'undefined' && !raw.includes('order:')) {
    return null; // Skip non-lesson utility pages (e.g. download, cheat-sheets)
  }

  // A. Interactive Sections (30 pts)
  const hasSections = /sections:/.test(raw);
  const sectionMatches = [...raw.matchAll(/- id:\s*([^\r\n]+)/g)];
  const hasKeyTerms = /##\s+Key Terms/i.test(body);

  if (hasSections && sectionMatches.length >= 3) {
    score += 15;
    breakdown.push(`✓ Sections (${sectionMatches.length}) [+15]`);
  } else if (hasSections) {
    score += 8;
    breakdown.push(`⚠ Few Sections (${sectionMatches.length}) [+8]`);
    flags.push('Low section count');
  } else {
    breakdown.push(`✗ Missing Sections [0]`);
    flags.push('No sections[]');
  }

  if (hasKeyTerms) {
    score += 15;
    breakdown.push(`✓ Key Terms present [+15]`);
  } else {
    breakdown.push(`✗ Missing Key Terms [0]`);
    flags.push('No ## Key Terms');
  }

  // B. Pedagogical Callouts (20 pts)
  const hasExamCallout = /<Callout[^>]*type=['"]exam['"]/i.test(body);
  const hasWarnCallout = /<Callout[^>]*type=['"]warn['"]/i.test(body);

  if (hasExamCallout) {
    score += 10;
    breakdown.push(`✓ CompTIA Exam Callout [+10]`);
  } else {
    flags.push('Missing <Callout type="exam">');
  }

  if (hasWarnCallout) {
    score += 10;
    breakdown.push(`✓ Misconception Warning Callout [+10]`);
  } else {
    flags.push('Missing <Callout type="warn">');
  }

  // C. Visual / Diagram Asset (20 pts)
  const imageMatches = [
    ...body.matchAll(/!\[(.*?)\]\((.*?)\)/g),
    ...body.matchAll(/<img[^>]+src=["']([^"']+)["'][^>]*>/g),
  ];
  if (imageMatches.length > 0) {
    score += 20;
    breakdown.push(`✓ Technical visual asset (${imageMatches.length}) [+20]`);
    // Verify image path existence
    for (const m of imageMatches) {
      const src = m[2] || m[1];
      const resolved = src.startsWith('/')
        ? path.join(repoRoot, 'public', src.replace(/^\//, ''))
        : path.resolve(path.dirname(filePath), src);
      if (!fs.existsSync(resolved)) {
        flags.push(`Broken image link: ${src}`);
      }
    }
  } else {
    flags.push('No technical diagram or photo');
  }

  // D. Voice & Tone Hygiene (20 pts)
  const patronizingWords = ['simply', 'obviously', 'it is easy to', 'just run', 'just plug', 'just click'];
  const academicFluff = ['in this lesson, we will', 'students will learn', 'it is important to note that'];
  let toneDeductions = 0;

  for (const w of patronizingWords) {
    if (new RegExp('\\b' + w + '\\b', 'i').test(body)) {
      toneDeductions += 4;
      flags.push(`Patronizing word "${w}"`);
    }
  }
  for (const w of academicFluff) {
    if (new RegExp('\\b' + w + '\\b', 'i').test(body)) {
      toneDeductions += 5;
      flags.push(`Academic preamble "${w}"`);
    }
  }
  const toneScore = Math.max(0, 20 - toneDeductions);
  score += toneScore;
  breakdown.push(`Voice hygiene: ${toneScore}/20`);

  // E. Depth & Content Scope (10 pts)
  const words = body.split(/\s+/).length;
  if (words >= 800) {
    score += 10;
    breakdown.push(`✓ Substantial prose depth (${words} words) [+10]`);
  } else if (words >= 400) {
    score += 6;
    flags.push(`Prose brief (${words} words)`);
  } else {
    score += 2;
    flags.push(`Prose thin (${words} words)`);
  }

  return { file: rel, track, moduleId, order, score, flags, breakdown };
}

// ─── 2. LAB QUALITY EVALUATOR ───────────────────────────────────────────────
export function evaluateLabQuality(filePath) {
  const { raw } = readFrontmatterAndBody(filePath);
  const rel = path.relative(repoRoot, filePath);
  let score = 0;
  const breakdown = [];
  const flags = [];

  const trackMatch = raw.match(/track:\s*['"]?([^'\n\r"]+)/);
  const track = trackMatch ? trackMatch[1].trim() : '';
  const moduleMatch = raw.match(/moduleId:\s*['"]?([^'\n\r"]+)/);
  const moduleId = moduleMatch ? moduleMatch[1].trim() : '';
  const orderMatch = raw.match(/order:\s*(\d+)/);
  const order = orderMatch ? parseInt(orderMatch[1], 10) : 0;

  const choiceMatches = [...raw.matchAll(/type:\s*['"]?choice['"]?/g)].length;
  const exactMatches = [...raw.matchAll(/type:\s*['"]?exact['"]?/g)].length;
  const oneOfMatches = [...raw.matchAll(/type:\s*['"]?oneOf['"]?/g)].length;
  const regexMatches = [...raw.matchAll(/type:\s*['"]?regex['"]?/g)].length;
  const totalTyped = exactMatches + oneOfMatches + regexMatches;
  const totalSteps = choiceMatches + totalTyped;

  if (totalSteps === 0) {
    if (/activity:\s*['"]?code['"]?/.test(raw)) {
      const slugMatch = raw.match(/slug:\s*['"]?([^'\n\r"]+)/);
      const slug = slugMatch ? slugMatch[1].trim() : '';
      const codeExPath = path.join(repoRoot, 'src', 'lib', 'codeExercises.ts');
      const codeExContent = fs.existsSync(codeExPath) ? fs.readFileSync(codeExPath, 'utf-8') : '';
      const hasExercise = codeExContent.includes(`'${slug}'`) || codeExContent.includes(`"${slug}"`);
      const hasStarterCode = codeExContent.includes('starterCode:');
      const hasExpectedOutput = codeExContent.includes('expectedOutput:');
      const hasHints = codeExContent.includes('hints:');
      if (hasExercise && hasStarterCode && hasExpectedOutput && hasHints) {
        return {
          file: rel,
          track,
          moduleId,
          order,
          score: 100,
          flags: [],
          breakdown: ['✓ Interactive code laboratory with verified Monaco starter code, assertions, and hints [+100]'],
        };
      }
    }
    // Non-step lab (e.g. pc-assembly or legacy iframe)
    return { file: rel, track, moduleId, order, score: 70, flags: ['Non-step custom activity'], breakdown: ['Legacy or custom simulator'] };
  }

  // A. Step Count & Scope (25 pts) - target 8–12
  if (totalSteps >= 8 && totalSteps <= 14) {
    score += 25;
    breakdown.push(`✓ Optimal step scope (${totalSteps} steps) [+25]`);
  } else if (totalSteps >= 6) {
    score += 18;
    flags.push(`Moderate step count (${totalSteps} steps, target: 8-12)`);
  } else {
    score += 8;
    flags.push(`Short lab (${totalSteps} steps, target: 8-12)`);
  }

  // B. Typed Performance Ratio (35 pts) - hard rule: >= 50% typed
  const typedRatio = totalTyped / totalSteps;
  if (typedRatio >= 0.5) {
    score += 35;
    breakdown.push(`✓ Performance-first: ${Math.round(typedRatio * 100)}% typed (${totalTyped}/${totalSteps}) [+35]`);
  } else {
    const pts = Math.round(typedRatio * 40);
    score += pts;
    flags.push(`Multiple-choice heavy: only ${Math.round(typedRatio * 100)}% typed (${totalTyped}/${totalSteps})`);
  }

  // C. Diagnostic Rationales (15 pts) - 100% of choices must have rationales
  const rationales = [...raw.matchAll(/rationale:/g)].length;
  if (choiceMatches === 0 || rationales >= choiceMatches) {
    score += 15;
    breakdown.push(`✓ 100% choice rationales [+15]`);
  } else {
    const pts = Math.round((rationales / Math.max(1, choiceMatches)) * 15);
    score += pts;
    flags.push(`Missing rationales: ${rationales}/${choiceMatches} choice steps`);
  }

  // D. Progressive Hints & Success Confirmation (15 pts)
  const hints = [...raw.matchAll(/hint:/g)].length;
  const successMsgs = [...raw.matchAll(/successMessage:/g)].length;
  if (hints >= totalSteps && successMsgs >= totalSteps) {
    score += 15;
    breakdown.push(`✓ Hints and success messages complete [+15]`);
  } else {
    const pts = Math.round(((hints + successMsgs) / Math.max(2, totalSteps * 2)) * 15);
    score += pts;
    flags.push(`Missing hints (${hints}/${totalSteps}) or successMsgs (${successMsgs}/${totalSteps})`);
  }

  // E. Production Ending (10 pts)
  const validators = [...raw.matchAll(/type:\s*['"]?([a-zA-Z0-9]+)['"]?/g)].map((m) => m[1]);
  const lastValidator = validators[validators.length - 1];
  if (lastValidator === 'regex' || lastValidator === 'exact' || lastValidator === 'oneOf') {
    score += 10;
    breakdown.push(`✓ Ends with student-produced artifact (${lastValidator}) [+10]`);
  } else {
    flags.push(`Ends with passive selection (${lastValidator})`);
  }

  return { file: rel, track, moduleId, order, score, flags, breakdown };
}

// ─── 3. QUIZ QUALITY EVALUATOR ──────────────────────────────────────────────
export function evaluateQuizQuality(filePath) {
  const { raw } = readFrontmatterAndBody(filePath);
  const rel = path.relative(repoRoot, filePath);
  let score = 0;
  const breakdown = [];
  const flags = [];

  const trackMatch = raw.match(/track:\s*['"]?([^'\n\r"]+)/);
  const track = trackMatch ? trackMatch[1].trim() : '';
  const moduleMatch = raw.match(/moduleId:\s*['"]?([^'\n\r"]+)/);
  const moduleId = moduleMatch ? moduleMatch[1].trim() : '';
  const orderMatch = raw.match(/order:\s*(\d+)/);
  const order = orderMatch ? parseInt(orderMatch[1], 10) : 0;

  const singles = [...raw.matchAll(/type:\s*['"]?single['"]?/g)].length;
  const multis = [...raw.matchAll(/type:\s*['"]?multi['"]?/g)].length;
  const shorts = [...raw.matchAll(/type:\s*['"]?short['"]?/g)].length;
  const totalQuestions = singles + multis + shorts;

  if (totalQuestions === 0) {
    return { file: rel, track, moduleId, order, score: 0, flags: ['Zero inline questions (empty stub)'], breakdown: [] };
  }

  // A. Diagnostic Explanations (40 pts) - 100% must have explanations
  const explanations = [...raw.matchAll(/explanation:/g)].length;
  const explRatio = explanations / totalQuestions;
  if (explRatio >= 0.95) {
    score += 40;
    breakdown.push(`✓ Explanations complete (${explanations}/${totalQuestions}) [+40]`);
  } else {
    const pts = Math.round(explRatio * 40);
    score += pts;
    flags.push(`Missing explanations: ${totalQuestions - explanations} of ${totalQuestions} questions`);
  }

  // B. Question Diversity (30 pts)
  const singleRatio = singles / totalQuestions;
  if (singleRatio <= 0.75 && (multis > 0 || shorts > 0)) {
    score += 30;
    breakdown.push(`✓ Healthy question type mix (single/multi/short) [+30]`);
  } else if (singleRatio < 1.0) {
    score += 20;
    flags.push(`Dominantly single-choice (${singles}/${totalQuestions})`);
  } else {
    score += 10;
    flags.push('100% single-choice questions');
  }

  // C. Question Volume / Breadth (15 pts) - checkpoints 10+, reviews 15+
  if (totalQuestions >= 10) {
    score += 15;
    breakdown.push(`✓ Solid assessment breadth (${totalQuestions} questions) [+15]`);
  } else if (totalQuestions >= 6) {
    score += 10;
    flags.push(`Short quiz (${totalQuestions} questions, target: 10-15)`);
  } else {
    score += 4;
    flags.push(`Very brief assessment (${totalQuestions} questions)`);
  }

  // D. Item Integrity & Distractor Quality (15 pts)
  const hasAllOfTheAbove = /all of the above/i.test(raw);
  const hasNoneOfTheAbove = /none of the above/i.test(raw);
  const hasNegativeStem = /which of the following is not/i.test(raw) || /which is not/i.test(raw);

  let integrityDeductions = 0;
  if (hasAllOfTheAbove) {
    integrityDeductions += 5;
    flags.push('Contains "All of the above"');
  }
  if (hasNoneOfTheAbove) {
    integrityDeductions += 5;
    flags.push('Contains "None of the above"');
  }
  if (hasNegativeStem) {
    integrityDeductions += 5;
    flags.push('Contains negative prompt phrasing ("is NOT")');
  }
  const integrityScore = Math.max(0, 15 - integrityDeductions);
  score += integrityScore;
  breakdown.push(`Item integrity: ${integrityScore}/15`);

  return { file: rel, track, moduleId, order, score, flags, breakdown };
}

// ─── 4. MAIN AUDIT RUNNER ───────────────────────────────────────────────────
export function runQualityAudit() {
  const lessonFiles = scanDir(path.join(contentRoot, 'lessons'));
  const labFiles = scanDir(path.join(contentRoot, 'labs'));
  const quizFiles = scanDir(path.join(contentRoot, 'quizzes'));

  const lessons = lessonFiles.map(evaluateLessonQuality).filter(Boolean);
  const labs = labFiles.map(evaluateLabQuality).filter(Boolean);
  const quizzes = quizFiles.map(evaluateQuizQuality).filter(Boolean);

  const filterByTrack = (items) => (trackFilter ? items.filter((i) => i.track === trackFilter) : items);

  const filteredLessons = filterByTrack(lessons);
  const filteredLabs = filterByTrack(labs);
  const filteredQuizzes = filterByTrack(quizzes);

  const calcAvg = (items) => (items.length ? Math.round(items.reduce((s, i) => s + i.score, 0) / items.length) : 0);

  console.log('\n================================================================');
  console.log('            BEATTIENETTRACK QUALITY SCORECARD REPORT            ');
  console.log('================================================================');

  const summary = [
    {
      Type: 'Lessons',
      Total: filteredLessons.length,
      'Avg Score': `${calcAvg(filteredLessons)} / 100`,
      'Passing (>=80)': filteredLessons.filter((l) => l.score >= 80).length,
      'Failing (<80)': filteredLessons.filter((l) => l.score < 80).length,
    },
    {
      Type: 'Labs',
      Total: filteredLabs.length,
      'Avg Score': `${calcAvg(filteredLabs)} / 100`,
      'Passing (>=80)': filteredLabs.filter((l) => l.score >= 80).length,
      'Failing (<80)': filteredLabs.filter((l) => l.score < 80).length,
    },
    {
      Type: 'Quizzes',
      Total: filteredQuizzes.length,
      'Avg Score': `${calcAvg(filteredQuizzes)} / 100`,
      'Passing (>=80)': filteredQuizzes.filter((q) => q.score >= 80).length,
      'Failing (<80)': filteredQuizzes.filter((q) => q.score < 80).length,
    },
  ];

  console.table(summary);

  // Group by Track
  const byTrack = {};
  for (const item of [...filteredLessons, ...filteredLabs, ...filteredQuizzes]) {
    const t = item.track || 'unassigned';
    byTrack[t] = byTrack[t] || { lessons: [], labs: [], quizzes: [] };
    if (item.file.includes('lessons')) byTrack[t].lessons.push(item);
    else if (item.file.includes('labs')) byTrack[t].labs.push(item);
    else if (item.file.includes('quizzes')) byTrack[t].quizzes.push(item);
  }

  console.log('\n=== QUALITY SCORES BY TRACK ===');
  const trackTable = Object.keys(byTrack).map((t) => ({
    Track: t,
    'Lesson Avg': `${calcAvg(byTrack[t].lessons)} (${byTrack[t].lessons.length})`,
    'Lab Avg': `${calcAvg(byTrack[t].labs)} (${byTrack[t].labs.length})`,
    'Quiz Avg': `${calcAvg(byTrack[t].quizzes)} (${byTrack[t].quizzes.length})`,
  }));
  console.table(trackTable);

  // Priority remediation list: Worst performing labs (<60)
  const lowLabs = filteredLabs.filter((l) => l.score < 60).sort((a, b) => a.score - b.score);
  if (lowLabs.length) {
    console.log('\n=== HIGH PRIORITY LAB REMEDIATIONS (Score < 60) ===');
    lowLabs.forEach((l) => {
      console.log(`❌ [${l.score}/100] ${l.file}`);
      console.log(`   Flags: ${l.flags.join(', ')}`);
    });
  }

  // Priority remediation list: Worst performing lessons (<75)
  const lowLessons = filteredLessons.filter((l) => l.score < 75).sort((a, b) => a.score - b.score);
  if (lowLessons.length) {
    console.log('\n=== HIGH PRIORITY LESSON REMEDIATIONS (Score < 75) ===');
    lowLessons.slice(0, 10).forEach((l) => {
      console.log(`❌ [${l.score}/100] ${l.file}`);
      console.log(`   Flags: ${l.flags.join(', ')}`);
    });
  }

  if (showDetails) {
    console.log('\n=== ALL FLAGGED ITEMS ===');
    [...filteredLessons, ...filteredLabs, ...filteredQuizzes]
      .filter((i) => i.score < 80)
      .forEach((i) => {
        console.log(`[${i.score}/100] ${i.file} -> ${i.flags.join('; ')}`);
      });
  }

  const failingCount =
    filteredLessons.filter((l) => l.score < 80).length +
    filteredLabs.filter((l) => l.score < 80).length +
    filteredQuizzes.filter((q) => q.score < 80).length;

  if (isStrict && failingCount > 0) {
    console.error(`\n❌ Quality Audit Failed: ${failingCount} items scored below the 80/100 threshold.`);
    process.exit(1);
  } else {
    console.log(`\n✓ Quality Audit complete.`);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  runQualityAudit();
}
