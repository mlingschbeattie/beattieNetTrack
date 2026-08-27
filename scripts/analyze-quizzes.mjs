import fs from 'fs';
import path from 'path';

const root = process.cwd();
const quizDir = path.join(root, 'src', 'content', 'quizzes');
const trackDir = path.join(root, 'src', 'content', 'tracks');
const moduleDir = path.join(root, 'src', 'content', 'modules');
const lessonDir = path.join(root, 'src', 'content', 'lessons');

function getAllFiles(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  const list = fs.readdirSync(dir);
  list.forEach((file) => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllFiles(filePath));
    } else if (file.endsWith('.mdx') || file.endsWith('.md')) {
      results.push(filePath);
    }
  });
  return results;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return { raw: '', data: {}, questionsCount: 0 };
  const yaml = match[1];
  const lines = yaml.split(/\r?\n/);
  const data = {};
  let inQuestions = false;
  let qCount = 0;
  let currentKey = null;

  for (let line of lines) {
    const trimmed = line.trim();
    if (line.startsWith('questions:')) {
      inQuestions = true;
      continue;
    }
    if (inQuestions) {
      if (/^\s*-\s+id:/.test(line) || /^\s*-\s+prompt:/.test(line) || /^\s*-\s+type:/.test(line)) {
        qCount++;
      }
      if (/^[a-zA-Z0-9_-]+:/.test(line) && !line.startsWith(' ') && !line.startsWith('-')) {
        inQuestions = false;
      }
    }
    const kv = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (kv && !line.startsWith(' ') && !line.startsWith('-')) {
      currentKey = kv[1];
      data[currentKey] = kv[2].replace(/^["']|["']$/g, '');
    }
  }
  return { raw: yaml, data, questionsCount: qCount };
}

const quizFiles = getAllFiles(quizDir);
const quizzes = quizFiles.map((f) => {
  const content = fs.readFileSync(f, 'utf8');
  const fm = parseFrontmatter(content);
  let qCount = fm.questionsCount;
  if (fm.data.quizJsonPath) {
    const jsonPath = path.join(root, 'public', fm.data.quizJsonPath);
    if (fs.existsSync(jsonPath)) {
      try {
        const j = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
        qCount = Array.isArray(j.questions) ? j.questions.length : qCount;
      } catch (e) {}
    }
  }
  const rel = path.relative(quizDir, f).replace(/\\/g, '/');
  return {
    file: rel,
    fullPath: f,
    title: fm.data.title,
    slug: fm.data.slug || rel.replace(/\.mdx?$/, ''),
    track: fm.data.track,
    moduleId: fm.data.moduleId,
    module: fm.data.module,
    tags: fm.data.tags,
    difficulty: fm.data.difficulty,
    estMinutes: fm.data.estMinutes,
    passThreshold: fm.data.passThreshold,
    quizJsonPath: fm.data.quizJsonPath,
    qCount,
    rawYaml: fm.raw,
  };
});

console.log('Total Quizzes:', quizzes.length);

// Analyze track field presence
const missingTrack = quizzes.filter((q) => !q.track);
console.log('Quizzes missing track field:', missingTrack.length);
if (missingTrack.length > 0) {
  console.log('  Missing track files:', missingTrack.map((q) => q.file));
}

// Check tracks in tracks collection
const tracks = getAllFiles(trackDir).map((f) => {
  const content = fs.readFileSync(f, 'utf8');
  const fm = parseFrontmatter(content);
  return { file: path.basename(f), slug: fm.data.slug || path.basename(f, path.extname(f)), title: fm.data.title };
});
console.log('\nTracks in content collection:', tracks.map((t) => t.slug));

// Check modules in modules collection
const modules = getAllFiles(moduleDir).map((f) => {
  const content = fs.readFileSync(f, 'utf8');
  const fm = parseFrontmatter(content);
  return {
    file: path.relative(moduleDir, f).replace(/\\/g, '/'),
    slug: fm.data.slug || path.relative(moduleDir, f).replace(/\\/g, '/').replace(/\.mdx?$/, ''),
    track: fm.data.track,
    moduleId: fm.data.moduleId,
    title: fm.data.title,
  };
});
console.log('Total Modules:', modules.length);

// Check how quizzes map to modules
const mappedToModules = quizzes.filter((q) => {
  const modId = q.moduleId || q.module;
  return modules.some((m) => m.moduleId === modId || m.slug === modId || m.slug.endsWith(modId));
});
console.log('Quizzes matching a module in modules collection:', mappedToModules.length, 'out of', quizzes.length);

// Question count breakdown and categorizations
console.log('\n--- Question Count Histogram ---');
const hist = {};
quizzes.forEach((q) => {
  hist[q.qCount] = (hist[q.qCount] || 0) + 1;
});
console.log(hist);

// Group naming patterns
console.log('\n--- Naming Patterns ---');
const patternGroups = {
  'assessment-1-x-x (Tech+ / PC-Tech docx import)': quizzes.filter((q) => q.file.includes('assessment-1-')),
  'pct-xxx (Comprehensive PC Tech assessments)': quizzes.filter((q) => q.file.startsWith('pc-technician/pct-')),
  'net-x-x-x (Network Engineer unit quizzes)': quizzes.filter((q) => q.file.startsWith('network-engineer/net-')),
  'tech-plus-x-x-x (Tech+ topic quizzes)': quizzes.filter((q) => q.file.startsWith('tech-plus/tech-plus-')),
  'standalone checkpoints (*checkpoint.mdx, *check.mdx)': quizzes.filter((q) => !q.file.includes('/')),
  'cybersecurity-foundations': quizzes.filter((q) => q.file.startsWith('cybersecurity-foundations/')),
};

for (const [name, list] of Object.entries(patternGroups)) {
  console.log(`\nGroup: ${name} (${list.length} quizzes)`);
  const qCounts = list.map((q) => q.qCount);
  console.log(`  Question counts min: ${Math.min(...qCounts)}, max: ${Math.max(...qCounts)}, avg: ${(qCounts.reduce((a, b) => a + b, 0) / qCounts.length).toFixed(1)}`);
  console.log(`  Sample title: ${list[0]?.title}`);
  console.log(`  Sample track: ${list[0]?.track}`);
  console.log(`  Sample moduleId: ${list[0]?.moduleId}`);
  console.log(`  Sample tags: ${list[0]?.tags}`);
  console.log(`  Has quizJsonPath: ${list.filter((q) => q.quizJsonPath).length} / ${list.length}`);
}
