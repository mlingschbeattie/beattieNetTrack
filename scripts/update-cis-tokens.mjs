import fs from 'node:fs';

const cisGlobalCssPath = 'c:/Users/mlingsch/cis-portal/src/styles/global.css';
let css = fs.readFileSync(cisGlobalCssPath, 'utf8');

const updatedTokens = `:root {
  /* ── Calibrated Bucket / Tier colours ─────────────── */
  --bucket-strong:     #10b981;
  --bucket-developing: #3b82f6;
  --bucket-needs-work: #f59e0b;
  --bucket-critical:   #ef4444;

  /* ── Deep Slate Enterprise Backgrounds ────────────── */
  --bg:        #07090e;
  --surface:   #0e131f;
  --surface-2: #161e2e;

  /* ── Text Hierarchy ───────────────────────────────── */
  --text:        #f3f4f6;
  --text-muted:  #94a3b8;
  --text-subtle: #64748b;

  /* ── Crisp Subtle Borders ─────────────────────────── */
  --border:        rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);

  /* ── Typography & Radius ──────────────────────────── */
  --font-sans: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  --radius:    10px;
  --radius-sm: 6px;
  --shadow:    0 1px 3px rgba(0, 0, 0, 0.4);
}`;

css = css.replace(/:root\s*\{[\s\S]*?--shadow:\s*0 1px 3px rgba\(0, 0, 0, 0\.5\);\s*\}/, updatedTokens);

css = css.replace(
  "body {\n  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;",
  "body {\n  font-family: var(--font-sans);"
);

css = css.replace(
  "code {\n  font-family: 'Menlo', 'Consolas', monospace;",
  "code {\n  font-family: var(--font-mono);"
);

css = css.replace(
  "font-family: 'Menlo', 'Consolas', monospace;",
  "font-family: var(--font-mono);"
);

fs.writeFileSync(cisGlobalCssPath, css);
console.log('Updated cis-portal global.css with enterprise design tokens');
