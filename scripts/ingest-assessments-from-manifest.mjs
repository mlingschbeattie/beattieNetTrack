import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const manifestPath = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(projectRoot, 'scripts', 'assessment-manifest.techplus.json');

const outputQuizJsonDir = path.join(projectRoot, 'public', 'quizzes', 'tech-plus');
const outputQuizMdxDir = path.join(projectRoot, 'src', 'content', 'quizzes', 'tech-plus');

const ensureDir = async (dirPath) => {
  await fs.mkdir(dirPath, { recursive: true });
};

const toJsonFileName = (assessmentCode) => `assessment-${assessmentCode}.json`;

const toMdx = (entry, quizJsonPath) => `---\ntitle: ${entry.title}\ndescription: Auto-generated assessment quiz from Tech+ manifest.\nslug: ${entry.slug}\ntype: quiz\ntrack: pc-technician\nmoduleId: ${entry.moduleId}\norder: ${entry.order}\ndifficulty: Beginner\nestMinutes: 10\npassThreshold: 70\nquizJsonPath: ${quizJsonPath}\ntags: [\"tech+\", \"assessment\"]\nhints:\n  - Read each prompt carefully before selecting an answer.\nchecklist:\n  - Completed all questions\n  - Reviewed score and corrections\n---\n\nGenerated from manifest entry ${entry.assessmentCode}.\n`;

const run = async () => {
  const raw = await fs.readFile(manifestPath, 'utf8');
  const manifest = JSON.parse(raw);
  if (!Array.isArray(manifest)) {
    throw new Error('Manifest must be an array.');
  }

  await ensureDir(outputQuizJsonDir);
  await ensureDir(outputQuizMdxDir);

  for (const entry of manifest) {
    const jsonFileName = toJsonFileName(entry.assessmentCode);
    const jsonPublicPath = `/quizzes/tech-plus/${jsonFileName}`;
    const jsonDiskPath = path.join(outputQuizJsonDir, jsonFileName);
    const mdxDiskPath = path.join(outputQuizMdxDir, `${entry.slug}.mdx`);

    const jsonPayload = {
      id: entry.slug,
      title: entry.title,
      assessmentCode: entry.assessmentCode,
      sourceQuestionDocx: entry.sourceQuestionDocx,
      sourceAnswerDocx: entry.sourceAnswerDocx,
      questions: Array.isArray(entry.questions) ? entry.questions : [],
    };

    await fs.writeFile(jsonDiskPath, `${JSON.stringify(jsonPayload, null, 2)}\n`, 'utf8');
    await fs.writeFile(mdxDiskPath, toMdx(entry, jsonPublicPath), 'utf8');
  }

  console.log(`Generated ${manifest.length} assessment quizzes from manifest ${manifestPath}`);
};

run().catch((error) => {
  console.error(error);
  process.exit(1);
});
