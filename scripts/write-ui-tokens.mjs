import fs from 'node:fs';

const tokensCss = `/**
 * @beattie/ui Design Tokens
 * Canonical shared design system for Beattie Tech ecosystem applications.
 * Clean, high-density, enterprise dark UI standard with full RTL / Arabic support.
 */

:root {
  /* ==========================================================================
     Surfaces & Neutral Palette (Deep Slate & Obsidian)
     ========================================================================== */
  --beattie-bg: #07090e;
  --beattie-surface: #0e131f;
  --beattie-surface-elevated: #161e2e;
  --beattie-surface-subtle: #1c2638;
  --beattie-surface-glass: rgba(14, 19, 31, 0.85);

  --beattie-border: rgba(255, 255, 255, 0.08);
  --beattie-border-subtle: rgba(255, 255, 255, 0.14);
  --beattie-border-hover: rgba(255, 255, 255, 0.22);
  --beattie-border-active: #3b82f6;

  /* ==========================================================================
     Typography & Font Stacks (Latin + Arabic Fallback)
     ========================================================================== */
  --font-sans: 'Plus Jakarta Sans', 'Inter', 'Noto Sans Arabic', 'Segoe UI Arabic', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  --beattie-text: #f3f4f6;
  --beattie-text-muted: #94a3b8;
  --beattie-text-dim: #64748b;
  --beattie-text-inverse: #07090e;

  /* Typographic Scales */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */

  --leading-tight: 1.2;
  --leading-normal: 1.55;
  --leading-relaxed: 1.7;

  /* ==========================================================================
     Calibrated Semantic Accents (Sophisticated Enterprise - Zero Neon Bleed)
     ========================================================================== */
  /* Primary (Cobalt Blue) */
  --beattie-primary: #3b82f6;
  --beattie-primary-hover: #2563eb;
  --beattie-primary-subtle: rgba(59, 130, 246, 0.12);
  --beattie-primary-border: rgba(59, 130, 246, 0.35);

  /* Success / Mastery (Muted Emerald) */
  --beattie-success: #10b981;
  --beattie-success-hover: #059669;
  --beattie-success-subtle: rgba(16, 185, 129, 0.12);
  --beattie-success-border: rgba(16, 185, 129, 0.35);

  /* Warning / In Progress (Warm Amber) */
  --beattie-warning: #f59e0b;
  --beattie-warning-hover: #d97706;
  --beattie-warning-subtle: rgba(245, 158, 11, 0.12);
  --beattie-warning-border: rgba(245, 158, 11, 0.35);

  /* Danger / Deficit (Rose Red) */
  --beattie-danger: #ef4444;
  --beattie-danger-hover: #dc2626;
  --beattie-danger-subtle: rgba(239, 68, 68, 0.12);
  --beattie-danger-border: rgba(239, 68, 68, 0.35);

  /* AI / Intelligence / Utilities (Purple) */
  --beattie-ai: #8b5cf6;
  --beattie-ai-hover: #7c3aed;
  --beattie-ai-subtle: rgba(139, 92, 246, 0.12);
  --beattie-ai-border: rgba(139, 92, 246, 0.35);

  /* Cyan Accent (Network / Labs) */
  --beattie-cyan: #06b6d4;
  --beattie-cyan-subtle: rgba(6, 182, 212, 0.12);
  --beattie-cyan-border: rgba(6, 182, 212, 0.35);

  /* ==========================================================================
     Radii, Shadows & Elevation
     ========================================================================== */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 20px;
  --radius-pill: 9999px;

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.35);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6), 0 8px 10px -6px rgba(0, 0, 0, 0.5);

  /* ==========================================================================
     Layout & Spacing
     ========================================================================== */
  --header-height: 64px;
  --sidebar-width: 260px;
  --container-max: 1360px;
  --content-reading-max: 76ch;
}

/* ==========================================================================
   RTL Directionality & Bidirectional Utilities
   ========================================================================== */
[dir="rtl"] {
  text-align: right;
}

[dir="rtl"] .icon-directional {
  transform: scaleX(-1);
}

[dir="rtl"] .icon-directional-rotate {
  transform: rotate(180deg);
}
`;

// Write tokens.css
fs.writeFileSync('c:/Users/mlingsch/cluster/packages/ui/src/tokens.css', tokensCss);

// Update package.json
const pkgPath = 'c:/Users/mlingsch/cluster/packages/ui/package.json';
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
pkg.version = '0.2.0';
pkg.exports = {
  ".": "./src/index.ts",
  "./tokens.css": "./src/tokens.css"
};
fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2));

// Update index.ts
const indexTs = `// @beattie/ui - Canonical shared UI design tokens & primitives
export const UiVersion = '0.2.0';
`;
fs.writeFileSync('c:/Users/mlingsch/cluster/packages/ui/src/index.ts', indexTs);

console.log('Successfully wrote tokens.css, bumped @beattie/ui to 0.2.0');
