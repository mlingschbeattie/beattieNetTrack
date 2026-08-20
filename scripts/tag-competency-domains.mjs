import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');
const contentRoot = path.join(repoRoot, 'src', 'content');

const UNMAPPED_LESSON_FIXES = {
  'binary-exploitation.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.network.defense-basics' },
  'cryptography.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.crypto.basics' },
  'forensics.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.incident.response-basics' },
  'reverse-engineering.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.endpoint.hardening' },
  'web-exploitation.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.network.defense-basics' },
  'sql-injection.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.network.defense-basics' },
  'xss-demo.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.network.defense-basics' },
  'password-hashing.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.crypto.basics' },
  'auth-demo.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.identity.access-management' },
  'https-demo.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.crypto.basics' },
  'exif-simulator.mdx': { track: 'cybersecurity-engineer', moduleId: 'sec.incident.response-basics' },
  'general-skills.mdx': { track: 'cybersecurity-foundations', moduleId: 'cfs.fundamentals.security-concepts' },
  'about-class.mdx': { track: 'cybersecurity-foundations', moduleId: 'cfs.fundamentals.security-concepts' },
  'learning-tracks.mdx': { track: 'cybersecurity-foundations', moduleId: 'cfs.fundamentals.security-concepts' },
  'tour.mdx': { track: 'cybersecurity-foundations', moduleId: 'cfs.fundamentals.security-concepts' },
  'cheat-sheets.mdx': { track: 'network-engineer', moduleId: 'net.fundamentals.models-and-standards' },
  'study-guides.mdx': { track: 'network-engineer', moduleId: 'net.fundamentals.models-and-standards' },
  'resources.mdx': { track: 'network-engineer', moduleId: 'net.fundamentals.models-and-standards' },
  'download.mdx': { track: 'network-engineer', moduleId: 'net.fundamentals.models-and-standards' },
  'review-game.mdx': { track: 'network-engineer', moduleId: 'net.fundamentals.models-and-standards' },
  'progress-demo.mdx': { track: 'web-developer', moduleId: 'web.fundamentals.javascript' },
  'card-beam-animation-readme.mdx': { track: 'web-developer', moduleId: 'web.fundamentals.html-css' },
  'site-readme.mdx': { track: 'web-developer', moduleId: 'web.fundamentals.html-css' },
  'site-playwright_test_readme.mdx': { track: 'web-developer', moduleId: 'web.fundamentals.javascript' },
  'index.mdx': { track: 'cybersecurity-foundations', moduleId: 'cfs.fundamentals.security-concepts' },
};

function getDomainsForModule(moduleId, track) {
  if (!moduleId && !track) return [{ domainId: 'general.it', weight: 1.0 }];

  const mod = moduleId || '';

  // Tech+
  if (mod.startsWith('tech-plus.it-concepts')) return [{ domainId: 'techplus.concepts', weight: 1.0 }];
  if (mod.startsWith('tech-plus.infrastructure')) return [{ domainId: 'techplus.infrastructure', weight: 1.0 }];
  if (mod.startsWith('tech-plus.applications')) return [{ domainId: 'techplus.applications', weight: 1.0 }];
  if (mod.startsWith('tech-plus.software-dev')) return [{ domainId: 'techplus.software', weight: 1.0 }];
  if (mod.startsWith('tech-plus.databases')) return [{ domainId: 'techplus.databases', weight: 1.0 }];
  if (mod.startsWith('tech-plus.security')) return [{ domainId: 'techplus.security', weight: 1.0 }];
  if (track === 'tech-plus') return [{ domainId: 'techplus.concepts', weight: 1.0 }];

  // Network Engineer
  if (mod.startsWith('net.fundamentals')) return [{ domainId: 'netplus.networking_concepts', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }];
  if (mod.startsWith('net.implementation')) return [{ domainId: 'netplus.infrastructure', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }];
  if (mod.startsWith('net.operations')) return [{ domainId: 'netplus.operations', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }];
  if (mod.startsWith('net.security')) return [{ domainId: 'netplus.security', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }];
  if (mod.startsWith('net.troubleshooting')) return [{ domainId: 'netplus.troubleshooting', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }];
  if (mod === 'network-legacy' || track === 'network-engineer') return [{ domainId: 'netplus.networking_concepts', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }];

  // PC Technician / A+
  if (mod.startsWith('pct.hardware') || mod === 'hardware-fundamentals' || mod === 'pc-tech-labs') return [{ domainId: 'aplus1.hardware', weight: 0.8 }, { domainId: 'nocti.hardware', weight: 0.2 }];
  if (mod.startsWith('pct.troubleshooting')) return [{ domainId: 'aplus1.troubleshooting', weight: 0.8 }, { domainId: 'nocti.hardware', weight: 0.2 }];
  if (mod.startsWith('pct.os')) return [{ domainId: 'aplus2.os', weight: 0.8 }, { domainId: 'nocti.os', weight: 0.2 }];
  if (mod.startsWith('pct.fundamentals')) return [{ domainId: 'aplus1.hardware', weight: 0.5 }, { domainId: 'aplus2.os', weight: 0.5 }];
  if (mod.startsWith('pct.customer')) return [{ domainId: 'aplus2.operational_procedures', weight: 1.0 }];
  if (mod === 'pc-tech-legacy' || track === 'pc-technician') return [{ domainId: 'aplus1.hardware', weight: 0.8 }, { domainId: 'nocti.hardware', weight: 0.2 }];

  // Cybersecurity
  if (mod.startsWith('cfs.fundamentals') || track === 'cybersecurity-foundations') return [{ domainId: 'cyber.foundations', weight: 1.0 }];
  if (mod.startsWith('sec.crypto')) return [{ domainId: 'secplus.architecture', weight: 0.8 }, { domainId: 'cyber.foundations', weight: 0.2 }];
  if (mod.startsWith('sec.endpoint')) return [{ domainId: 'secplus.operations', weight: 0.8 }, { domainId: 'nocti.security', weight: 0.2 }];
  if (mod.startsWith('sec.fundamentals')) return [{ domainId: 'cyber.foundations', weight: 0.6 }, { domainId: 'secplus.threats', weight: 0.4 }];
  if (mod.startsWith('sec.identity')) return [{ domainId: 'secplus.architecture', weight: 0.8 }, { domainId: 'cyber.foundations', weight: 0.2 }];
  if (mod.startsWith('sec.incident')) return [{ domainId: 'secplus.operations', weight: 0.8 }, { domainId: 'cyber.foundations', weight: 0.2 }];
  if (mod.startsWith('sec.network')) return [{ domainId: 'secplus.threats', weight: 0.8 }, { domainId: 'nocti.networking', weight: 0.2 }];
  if (mod.startsWith('sec.security-awareness')) return [{ domainId: 'secplus.threats', weight: 0.8 }, { domainId: 'cyber.foundations', weight: 0.2 }];
  if (mod === 'cybersecurity-legacy' || track === 'cybersecurity-engineer') return [{ domainId: 'cyber.foundations', weight: 1.0 }];

  // Web Dev
  if (mod.startsWith('web.fundamentals.javascript')) return [{ domainId: 'aplus2.os', weight: 0.5 }, { domainId: 'web.frontend', weight: 0.5 }];
  if (mod.startsWith('web.fundamentals')) return [{ domainId: 'web.frontend', weight: 1.0 }];
  if (mod.startsWith('web.backend')) return [{ domainId: 'web.backend', weight: 1.0 }];
  if (mod.startsWith('web.security')) return [{ domainId: 'cyber.foundations', weight: 0.5 }, { domainId: 'web.security', weight: 0.5 }];
  if (track === 'web-developer') return [{ domainId: 'web.frontend', weight: 1.0 }];

  // Python
  if (mod.startsWith('py.') || track === 'python-developer') return [{ domainId: 'python.fundamentals', weight: 1.0 }];

  // AI/ML
  if (mod.startsWith('ai.') || track === 'ai-ml') return [{ domainId: 'ai.literacy', weight: 1.0 }];

  return [{ domainId: 'general.it', weight: 1.0 }];
}

function listFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  const results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) results.push(...listFiles(full));
    else if (/\.mdx?$/i.test(entry.name)) results.push(full);
  }
  return results;
}

function processCollection(collectionName, dirPath) {
  const files = listFiles(dirPath);
  let updated = 0;
  let skipped = 0;

  for (const filePath of files) {
    const fileName = path.basename(filePath);
    let content = fs.readFileSync(filePath, 'utf8');

    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!fmMatch) continue;

    const fmRaw = fmMatch[1];
    let trackMatch = fmRaw.match(/^track:\s*['"]?(.*?)['"]?$/m);
    let moduleMatch = fmRaw.match(/^moduleId:\s*['"]?(.*?)['"]?$/m) || fmRaw.match(/^module:\s*['"]?(.*?)['"]?$/m);

    let track = trackMatch ? trackMatch[1].trim() : null;
    let moduleId = moduleMatch ? moduleMatch[1].trim() : null;

    // Apply unmapped lesson fix if applicable
    if (collectionName === 'lessons' && (!track || !moduleId)) {
      if (UNMAPPED_LESSON_FIXES[fileName]) {
        track = UNMAPPED_LESSON_FIXES[fileName].track;
        moduleId = UNMAPPED_LESSON_FIXES[fileName].moduleId;
      }
    }

    const domains = getDomainsForModule(moduleId, track);
    const domainYaml = 'domains:\n' + domains.map((d) => `  - domainId: ${d.domainId}\n    weight: ${d.weight}`).join('\n');

    let newFm = fmRaw;

    // Fix track if missing
    if (track && !trackMatch) {
      newFm += `\ntrack: ${track}`;
    }
    // Fix moduleId if missing
    if (moduleId && !moduleMatch) {
      newFm += `\nmoduleId: ${moduleId}`;
    }

    // Replace or insert domains
    if (newFm.includes('domains:')) {
      // already has domains, check if we should update or keep
      skipped++;
      continue;
    } else {
      newFm += `\n${domainYaml}`;
    }

    const newContent = content.replace(/^---\r?\n[\s\S]*?\r?\n---/, `---\n${newFm}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf8');
    updated++;
  }

  console.log(`[${collectionName}] Processed ${files.length} files: ${updated} updated, ${skipped} already had domains.`);
}

console.log('--- Tagging Competency Domains ---');
processCollection('lessons', path.join(contentRoot, 'lessons'));
processCollection('quizzes', path.join(contentRoot, 'quizzes'));
console.log('--- Tagging Complete ---');
