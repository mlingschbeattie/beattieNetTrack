const fs = require('fs');
const path = require('path');

const lessonsDir = 'src/content/lessons';
const files = fs.readdirSync(lessonsDir).filter(f => f.endsWith('.mdx'));

const techPlusLessons = [];

files.forEach(f => {
  const content = fs.readFileSync(path.join(lessonsDir, f), 'utf-8');
  const trackMatch = content.match(/track:\s*['"]?([^'\n\r"]+)/);
  const moduleMatch = content.match(/moduleId:\s*['"]?([^'\n\r"]+)/);
  const titleMatch = content.match(/title:\s*['"]?([^'\n\r"]+)/);
  const orderMatch = content.match(/order:\s*(\d+)/);
  
  const track = trackMatch ? trackMatch[1].trim() : '';
  const moduleId = moduleMatch ? moduleMatch[1].trim() : '';
  const title = titleMatch ? titleMatch[1].trim() : '';
  const order = orderMatch ? parseInt(orderMatch[1], 10) : 0;
  
  if (track === 'tech-plus' || moduleId.startsWith('tech-plus.')) {
    const images = [...content.matchAll(/!\[(.*?)\]\((.*?)\)/g)].map(m => m[2]);
    techPlusLessons.push({
      file: f,
      slug: f.replace(/\.mdx$/, ''),
      title,
      moduleId,
      order,
      hasImage: images.length > 0,
      images,
      length: content.length
    });
  }
});

techPlusLessons.sort((a, b) => a.moduleId.localeCompare(b.moduleId) || a.order - b.order);

console.log('Total Tech+ lessons:', techPlusLessons.length);
console.log('With images:', techPlusLessons.filter(l => l.hasImage).length);
console.log('Without images:', techPlusLessons.filter(l => !l.hasImage).length);

const byModule = {};
techPlusLessons.forEach(l => {
  byModule[l.moduleId] = byModule[l.moduleId] || [];
  byModule[l.moduleId].push(l);
});

Object.keys(byModule).forEach(mod => {
  console.log(`\n=== Module: ${mod} (${byModule[mod].length} lessons) ===`);
  byModule[mod].forEach(l => {
    console.log(`  [${l.order}] ${l.slug} ("${l.title}"): ${l.images.length ? l.images.join(', ') : 'NONE'}`);
  });
});
