import fs from 'node:fs';

const hubTemplate = `---
const username = Astro.request.headers.get('Remote-User');
if (!username) return Astro.redirect('https://auth.beattietech.local');
const remoteUser = username;

const remoteName = Astro.request.headers.get('Remote-Name') ?? username;
const remoteGroups = Astro.request.headers.get('Remote-Groups') ?? '';

const preferredApiBase =
  (typeof process !== 'undefined' ? process.env.SERVER_API_URL : undefined) ??
  import.meta.env.SERVER_API_URL ??
  'http://beattie-api:3000';
const fallbackApiBase =
  (typeof process !== 'undefined' ? process.env.PUBLIC_API_URL : undefined) ??
  import.meta.env.PUBLIC_API_URL ??
  'https://api.beattietech.local';
const apiBases = [
  ...new Set([
    preferredApiBase,
    'http://beattie-api:3000',
    fallbackApiBase,
    'https://api.beattietech.local',
  ]),
];

async function apiJson(path: string) {
  for (const apiBase of apiBases) {
    try {
      const res = await fetch(\`\${apiBase}\${path}\`, {
        headers: {
          'Remote-User': remoteUser,
          'Remote-Name': remoteName,
          'Remote-Groups': remoteGroups,
        },
      });

      if (!res.ok) continue;
      const type = res.headers.get('content-type') ?? '';
      if (!type.includes('application/json')) continue;
      return res.json();
    } catch {
      // Continue to next configured API base if this one is unreachable.
    }
  }

  return null;
}

const [me, apps] = await Promise.all([
  apiJson('/api/me'),
  apiJson('/api/apps'),
]);

const safeApps = Array.isArray(apps) ? apps : [];
const displayName = me?.display_name ?? me?.displayName ?? remoteName;
const role = me?.role ?? (remoteGroups.includes('teachers') || remoteGroups.includes('admin') ? 'Instructor' : 'Student');
const level = Number(me?.level ?? 1);
const xp = Number(me?.xp ?? 0);
const credits = Number(me?.credits ?? 0);

type HubApp = {
  id?: string;
  title?: string;
  description?: string;
  url?: string;
  icon?: string;
  color?: string;
  navPosition?: number;
};

// Categorization Engine
function getAppCategory(app: HubApp) {
  const id = String(app?.id ?? '').toLowerCase();
  const text = \`\${app?.title ?? ''} \${app?.description ?? ''} \${app?.url ?? ''}\`.toLowerCase();

  if (['lms', 'cis', 'journal'].includes(id) || /curriculum|certification|comptia|nocti|tracking/.test(text)) {
    return 'curriculum';
  }
  if (['cyberlab', 'cyterm', 'techsupport', 'nexus', 'traceback', 'pcap-hunt', 'labs', 'lostintime'].includes(id) || /simulator|terminal|sandbox|threat|defense|hunting|workbench/.test(text)) {
    return 'simulators';
  }
  if (['chat', 'ai', 'rj45-tool', 'tools'].includes(id) || /ai|chat|model|assistant|pinout|reference/.test(text)) {
    return 'ai-tools';
  }
  return 'interactive';
}

const CATEGORY_META = {
  'curriculum': { label: 'Core Curriculum & Certification', color: '#3b82f6' },
  'simulators': { label: 'Interactive Ranges & Simulators', color: '#10b981' },
  'ai-tools': { label: 'AI Studio & Technical Utilities', color: '#8b5cf6' },
  'interactive': { label: 'Games, Quests & Challenges', color: '#f59e0b' }
};

// Clean Monochrome / Duotone SVG Icons
const SVG_ICONS: Record<string, string> = {
  'lms': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>',
  'cis': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>',
  'chat': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
  'traceback': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>',
  'labs': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4.5 16.5 6-6V3h3v7.5l6 6a3 3 0 0 1-2.25 5.25H6.75A3 3 0 0 1 4.5 16.5z"/></svg>',
  'quests': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
  'game': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="12" x2="10" y2="12"/><line x1="8" y1="10" x2="8" y2="14"/><line x1="15" y1="13" x2="15.01" y2="13"/><line x1="18" y1="11" x2="18.01" y2="11"/><rect x="2" y="6" width="20" height="12" rx="2"/></svg>',
  'journal': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
  'shop': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
  'ai': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>',
  'pcap-hunt': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
  'cipher': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
  'techsupport': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/></svg>',
  'cyberlab': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
  'cyterm': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>',
  'nexus': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>',
  'rj45-tool': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v6"/><path d="m19 13-7 7-7-7"/><path d="M12 17V3"/></svg>',
  'lostintime': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>'
};

const DEFAULT_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>';
---
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Beattie Hub — Ecosystem Command Center</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <style>
      :root {
        --beattie-bg: #07090e;
        --beattie-surface: #0e131f;
        --beattie-surface-elevated: #161e2e;
        --beattie-surface-subtle: #1c2638;
        --beattie-border: rgba(255, 255, 255, 0.08);
        --beattie-border-hover: rgba(255, 255, 255, 0.2);
        --beattie-text: #f3f4f6;
        --beattie-text-muted: #94a3b8;
        --beattie-text-dim: #64748b;
        --beattie-primary: #3b82f6;
        --beattie-success: #10b981;
      }

      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }

      body {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: var(--beattie-bg);
        color: var(--beattie-text);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
      }

      /* RTL Support */
      [dir="rtl"] {
        text-align: right;
      }

      [dir="rtl"] .icon-directional {
        transform: scaleX(-1);
      }

      /* Header */
      .header {
        position: sticky;
        top: 0;
        z-index: 50;
        background: #07090e;
        border-bottom: 1px solid var(--beattie-border);
      }

      .header-inner {
        max-width: 1360px;
        margin-inline: auto;
        padding-inline: 24px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
        color: inherit;
      }

      .brand-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 13px;
        background: #161e2e;
        border: 1px solid var(--beattie-border);
        color: var(--beattie-primary);
        padding: 4px 8px;
        border-radius: 6px;
      }

      .brand-title {
        font-size: 15px;
        font-weight: 700;
        letter-spacing: -0.2px;
        color: #ffffff;
      }

      .user-pill {
        display: flex;
        align-items: center;
        gap: 10px;
        background: var(--beattie-surface);
        border: 1px solid var(--beattie-border);
        border-radius: 999px;
        padding-inline: 12px 6px;
        padding-block: 4px;
      }

      .user-meta {
        display: flex;
        flex-direction: column;
      }

      .user-name {
        font-size: 13px;
        font-weight: 600;
        color: #fff;
        line-height: 1.2;
      }

      .user-role {
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--beattie-text-muted);
        text-transform: uppercase;
      }

      .user-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #1e293b;
        color: var(--beattie-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid var(--beattie-border);
      }

      /* Main Content */
      .main {
        flex: 1;
        max-width: 1360px;
        margin-inline: auto;
        padding: 32px 24px 64px;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 36px;
      }

      /* Hero Command Center */
      .hero {
        background: var(--beattie-surface);
        border: 1px solid var(--beattie-border);
        border-radius: 14px;
        padding: 24px 28px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
      }

      .hero-welcome h2 {
        font-size: 22px;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.4px;
      }

      .hero-welcome p {
        font-size: 14px;
        color: var(--beattie-text-muted);
        margin-top: 4px;
      }

      /* Telemetry KPI Badges */
      .hero-kpis {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
      }

      .kpi-card {
        background: var(--beattie-surface-elevated);
        border: 1px solid var(--beattie-border);
        border-radius: 8px;
        padding: 8px 16px;
        display: flex;
        flex-direction: column;
        min-width: 100px;
      }

      .kpi-label {
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--beattie-text-dim);
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .kpi-val {
        font-size: 18px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #fff;
      }

      /* Sections & Cards */
      .category-section {
        display: flex;
        flex-direction: column;
        gap: 14px;
      }

      .category-header {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .category-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--dot-color, var(--beattie-primary));
      }

      .category-title {
        font-size: 15px;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.2px;
      }

      .category-count {
        font-size: 12px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--beattie-text-dim);
      }

      .app-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
        gap: 16px;
      }

      /* App Card */
      .app-card {
        background: var(--beattie-surface);
        border: 1px solid var(--beattie-border);
        border-radius: 12px;
        padding: 20px;
        text-decoration: none;
        color: inherit;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.2s ease;
      }

      .app-card:hover {
        transform: translateY(-2px);
        background: var(--beattie-surface-elevated);
        border-color: var(--beattie-border-hover);
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
      }

      .app-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 12px;
      }

      .app-icon-wrap {
        width: 38px;
        height: 38px;
        border-radius: 8px;
        background: #161e2e;
        border: 1px solid var(--beattie-border);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--card-color, var(--beattie-primary));
      }

      .app-tag {
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 2px 7px;
        border-radius: 4px;
        background: #161e2e;
        color: var(--beattie-text-muted);
        border: 1px solid var(--beattie-border);
      }

      .app-body h3 {
        font-size: 15px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
        letter-spacing: -0.2px;
      }

      .app-body p {
        font-size: 13px;
        color: var(--beattie-text-muted);
        line-height: 1.5;
      }

      .app-footer {
        margin-top: 18px;
        padding-top: 12px;
        border-top: 1px solid var(--beattie-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 12px;
        font-weight: 600;
        color: var(--card-color, var(--beattie-primary));
      }

      .app-arrow {
        transition: transform 0.2s ease;
      }

      .app-card:hover .app-arrow {
        transform: translateX(4px);
      }

      [dir="rtl"] .app-card:hover .app-arrow {
        transform: translateX(-4px);
      }

      @media (max-width: 768px) {
        .hero {
          padding: 18px;
        }
        .hero-welcome h2 {
          font-size: 20px;
        }
      }
    </style>
  </head>
  <body>
    <!-- Top Navigation -->
    <header class="header">
      <div class="header-inner">
        <a href="/" class="brand">
          <span class="brand-badge">BN</span>
          <span class="brand-title">Beattie Tech Hub</span>
        </a>

        <div class="user-pill">
          <div class="user-meta">
            <span class="user-name">{displayName}</span>
            <span class="user-role">{role}</span>
          </div>
          <div class="user-avatar">{displayName.charAt(0).toUpperCase()}</div>
        </div>
      </div>
    </header>

    <!-- Main Learning Command Center -->
    <main class="main">
      <!-- Hero Banner & KPIs -->
      <section class="hero">
        <div class="hero-welcome">
          <h2>Learning Ecosystem</h2>
          <p>Access your core certification curricula, interactive cyber ranges, and AI lab assistants.</p>
        </div>

        <div class="hero-kpis">
          <div class="kpi-card">
            <div class="kpi-label">Level</div>
            <div class="kpi-val">{level}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">XP</div>
            <div class="kpi-val">{xp}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Credits</div>
            <div class="kpi-val">{credits}</div>
          </div>
        </div>
      </section>

      <!-- Apps by Category -->
      {['curriculum', 'simulators', 'ai-tools', 'interactive'].map((catKey) => {
        const catMeta = CATEGORY_META[catKey as keyof typeof CATEGORY_META];
        const categoryApps = safeApps.filter((app: HubApp) => getAppCategory(app) === catKey);

        if (categoryApps.length === 0) return null;

        return (
          <section class="category-section">
            <div class="category-header">
              <span class="category-dot" style={{ '--dot-color': catMeta.color }}></span>
              <h2 class="category-title">{catMeta.label}</h2>
              <span class="category-count">({categoryApps.length})</span>
            </div>

            <div class="app-grid">
              {categoryApps.map((app: HubApp) => {
                const iconSvg = SVG_ICONS[app.id || ''] || DEFAULT_SVG;
                const cardColor = app.color || catMeta.color;

                return (
                  <a
                    href={app.url}
                    class="app-card"
                    style={{
                      '--card-color': cardColor,
                    }}
                  >
                    <div>
                      <div class="app-header">
                        <div class="app-icon-wrap" set:html={iconSvg}></div>
                        <span class="app-tag">{app.id || 'app'}</span>
                      </div>
                      <div class="app-body">
                        <h3>{app.title}</h3>
                        <p>{app.description || 'Launch application.'}</p>
                      </div>
                    </div>

                    <div class="app-footer">
                      <span>Launch</span>
                      <span class="app-arrow icon-directional">→</span>
                    </div>
                  </a>
                );
              })}
            </div>
          </section>
        );
      })}
    </main>
  </body>
</html>
`;

fs.writeFileSync('c:/Users/mlingsch/cluster/hub/src/pages/index.astro', hubTemplate);
console.log('Successfully written clean SVG hub index.astro');
