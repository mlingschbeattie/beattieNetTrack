const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, '..', 'src', 'content', 'lessons');

function convertHrefHrefHtml(content) {
  // Replace href="...something.html[#frag]" where href does NOT start with /lessons/ or http(s): or mailto: or tel: or #
  return content.replace(/href=\"([^\"\n]+?)\.html(#[^\"]*)?\"/g, (m, p1, frag) => {
    if (/^(\/lessons\/|https?:|mailto:|tel:|#)/.test(p1)) return m;
    const base = path.basename(p1);
    const out = `/lessons/${base}${frag || ''}`;
    return `href=\"${out}\"`;
  });
}

function processFile(file) {
  const fp = path.join(dir, file);
  let src = fs.readFileSync(fp, 'utf8');
  const updated = convertHrefHrefHtml(src);
  if (updated !== src) {
    fs.writeFileSync(fp, updated, 'utf8');
    console.log('updated', file);
  }
}

fs.readdirSync(dir).filter(f => f.endsWith('.mdx')).forEach(processFile);

console.log('done');
