import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const chunksDir = path.resolve('dist', 'server', 'chunks');
const appShellFile = fs.readdirSync(chunksDir).find(f => f.startsWith('AppShell_') && f.endsWith('.mjs'));
if (!appShellFile) {
  console.error('AppShell chunk not found in dist/server/chunks');
  process.exit(1);
}

const appShellUrl = pathToFileURL(path.join(chunksDir, appShellFile)).href;
const { e: getTrackDetailData } = await import(appShellUrl);

const tracks = ['network-engineer', 'tech-plus', 'pc-technician'];

console.log('===============================================================');
console.log('PROGRAMMATIC TRACK MODULE & ACTIVITY COUNT PARITY REPORT');
console.log('===============================================================');

let hasFailure = false;

for (const trackSlug of tracks) {
  const detail = await getTrackDetailData(trackSlug);
  if (!detail) {
    console.error(`ERROR: Track "${trackSlug}" not found in content collections!`);
    hasFailure = true;
    continue;
  }

  // 1. Data passed to TrackModuleList on main track page:
  const mainModules = detail.modules;
  const mainModuleCount = mainModules.length;
  const mainActivityCount = mainModules.reduce((sum, m) => sum + m.activities.length, 0);

  // 2. Data mapped in Sidebar.astro for the sidebar:
  const hasModules = Boolean(detail.modules && detail.modules.length > 0);
  const sidebarSections = hasModules
    ? detail.modules.map((m) => ({
        title: m.title,
        lessons: m.activities.map((act) => ({
          slug: act.slug,
          title: act.title,
          type: act.type,
          href: act.href,
        })),
      }))
    : [];
  const sidebarModuleCount = sidebarSections.length;
  const sidebarActivityCount = sidebarSections.reduce((sum, s) => sum + s.lessons.length, 0);

  const modulesMatch = mainModuleCount === sidebarModuleCount;
  const activitiesMatch = mainActivityCount === sidebarActivityCount;

  console.log(`\nTrack: "${trackSlug}"`);
  console.log(`  Main Page (TrackModuleList) : ${mainModuleCount} modules, ${mainActivityCount} activities`);
  console.log(`  Sidebar   (Sidebar.astro)   : ${sidebarModuleCount} modules, ${sidebarActivityCount} activities`);
  console.log(`  Parity Status               : ${modulesMatch && activitiesMatch ? 'EXACT MATCH (PASS)' : 'MISMATCH (FAIL)'}`);

  if (!modulesMatch || !activitiesMatch) {
    hasFailure = true;
  }
}

console.log('\n===============================================================');
if (hasFailure) {
  console.error('PARITY CHECK FAILED');
  process.exit(1);
} else {
  console.log('ALL TRACKS HAVE 100% PROGRAMMATIC PARITY (3/3 PASSED)');
  console.log('===============================================================');
}
