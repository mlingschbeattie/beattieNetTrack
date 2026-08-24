import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');

const EXTENSIONS = new Set(['.css', '.astro', '.tsx', '.ts', '.jsx', '.js', '.mjs', '.html', '.mdx']);
const IGNORE_DIRS = new Set(['node_modules', '.git', '.astro', 'dist', '.venv']);

const varReferences = new Map(); // varName -> Array<{ file: string, line: number, text: string, hasFallback: boolean, fallbackText: string }>
const varDeclarations = new Map(); // varName -> Array<{ file: string, line: number, text: string }>

function scanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (!IGNORE_DIRS.has(entry.name)) {
        scanDir(path.join(dir, entry.name));
      }
    } else if (entry.isFile()) {
      const ext = path.extname(entry.name);
      if (EXTENSIONS.has(ext)) {
        scanFile(path.join(dir, entry.name));
      }
    }
  }
}

function scanFile(filePath) {
  const relPath = path.relative(repoRoot, filePath).replace(/\\/g, '/');
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split(/\r?\n/);

  // Search for var(--...) references: var\(\s*(--[a-zA-Z0-9_-]+)(?:\s*,\s*([^)]*))?\)
  // Note: nested var() can happen, so let's parse var\(\s*(--[a-zA-Z0-9_-]+)
  lines.forEach((line, index) => {
    const lineNum = index + 1;

    // Matches var(--foo) or var(--foo, fallback)
    const varRegex = /var\(\s*(--[a-zA-Z0-9_-]+)(?:\s*,\s*([^)]*))?\)/g;
    let match;
    while ((match = varRegex.exec(line)) !== null) {
      const varName = match[1];
      const fallback = match[2]?.trim();
      const hasFallback = !!fallback;

      if (!varReferences.has(varName)) {
        varReferences.set(varName, []);
      }
      varReferences.get(varName).push({
        file: relPath,
        line: lineNum,
        text: line.trim(),
        hasFallback,
        fallbackText: fallback || ''
      });
    }

    // Matches --foo: value (CSS declaration) or '--foo': value / "--foo": value in JS/TS objects
    const declRegex = /(?:^|[^\w-])(--[a-zA-Z0-9_-]+)\s*:/g;
    let declMatch;
    while ((declMatch = declRegex.exec(line)) !== null) {
      const varName = declMatch[1];
      // Exclude if it's inside a var() or something (already handled by regex starting with non-word or start)
      if (!varDeclarations.has(varName)) {
        varDeclarations.set(varName, []);
      }
      varDeclarations.get(varName).push({
        file: relPath,
        line: lineNum,
        text: line.trim()
      });
    }
  });
}

scanDir(path.join(repoRoot, 'src'));
// Also scan any root files if relevant
const rootFiles = ['astro.config.mjs'];
for (const rf of rootFiles) {
  const p = path.join(repoRoot, rf);
  if (fs.existsSync(p)) scanFile(p);
}

console.log(`Total unique var() referenced: ${varReferences.size}`);
console.log(`Total unique --var declared: ${varDeclarations.size}`);

const undefinedVars = [];

for (const [varName, refs] of varReferences.entries()) {
  if (!varDeclarations.has(varName)) {
    undefinedVars.push({ varName, refs });
  }
}

console.log(`\nFound ${undefinedVars.length} undefined CSS custom properties:\n`);
for (const { varName, refs } of undefinedVars) {
  console.log(`=== ${varName} (${refs.length} references) ===`);
  for (const ref of refs) {
    console.log(`  ${ref.file}:${ref.line} (fallback: ${ref.hasFallback ? ref.fallbackText : 'NONE'}) -> ${ref.text}`);
  }
}
