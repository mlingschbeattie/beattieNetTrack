---
const username = Astro.request.headers.get('Remote-User');
if (!username) return Astro.redirect('https://auth.beattietech.local');
const remoteUser = username;

const remoteName = Astro.request.headers.get('Remote-Name') ?? username;
const remoteGroups = Astro.request.headers.get('Remote-Groups') ?? '';

// Use internal container URL for SSR fetches to avoid Authelia overwriting Remote-Groups
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
      const res = await fetch(`${apiBase}${path}`, {
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
const role = me?.role ?? (remoteGroups.includes('teachers') || remoteGroups.includes('admin') ? 'instructor' : 'student');
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
  const text = `${app?.title ?? ''} ${app?.description ?? ''} ${app?.url ?? ''}`.toLowerCase();

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
  'curriculum': { label: 'Core Curriculum & Certification', icon: '🎓', color: '#3b82f6' },
  'simulators': { label: 'Interactive Ranges & Simulators', icon: '⚡', color: '#10b981' },
  'ai-tools': { label: 'AI Studio & Technical Utilities', icon: '✨', color: '#8b5cf6' },
  'interactive': { label: 'Games, Quests & Challenges', icon: '🎮', color: '#f59e0b' }
};

const APP_ICONS: Record<string, string> = {
  'lms': '📚',
  'cis': '🏆',
  'chat': '💬',
  'traceback': '🎯',
  'labs': '🔬',
  'quests': '⚡',
  'game': '🕹️',
  'journal': '📓',
  'shop': '🛍️',
  'ai': '✨',
  'pcap-hunt': '🛡️',
  'cipher': '🔒',
  'techsupport': '🎧',
  'cyberlab': '🚨',
  'cyterm': '💻',
  'nexus': '⚙️',
  'rj45-tool': '🔌',
  'lostintime': '⏳'
};
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
        --bg: #06090e;
        --bg-surface: #0c121b;
        --bg-surface-elevated: #131b27;
        --border: rgba(255, 255, 255, 0.08);
        --border-hover: rgba(16, 185, 129, 0.4);
        --text-main: #f3f4f6;
        --text-muted: #9ca3af;
        --text-dim: #6b7280;
        --accent-emerald: #10b981;
        --accent-cyan: #06b6d4;
        --accent-indigo: #6366f1;
        --accent-purple: #8b5cf6;
        --accent-amber: #f59e0b;
      }

      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }

      body {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text-main);
        min-height: 100vh;
        background-image: 
          radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.08) 0px, transparent 50%),
          radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
          radial-gradient(at 50% 100%, rgba(6, 182, 212, 0.05) 0px, transparent 50%);
        background-attachment: fixed;
        display: flex;
        flex-direction: column;
      }

      /* Header */
      .header {
        position: sticky;
        top: 0;
        z-index: 50;
        backdrop-filter: blur(16px);
        background: rgba(6, 9, 14, 0.85);
        border-bottom: 1px solid var(--border);
      }

      .header-inner {
        max-width: 1360px;
        margin: 0 auto;
        padding: 0 24px;
        height: 68px;
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

      .brand-logo {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 0 16px rgba(16, 185, 129, 0.35);
      }

      .brand-text h1 {
        font-size: 16px;
        font-weight: 800;
        letter-spacing: -0.3px;
        color: #ffffff;
      }

      .brand-text span {
        font-size: 11px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent-emerald);
        letter-spacing: 0.5px;
      }

      .user-pill {
        display: flex;
        align-items: center;
        gap: 12px;
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 5px 14px 5px 6px;
      }

      .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #1e293b;
        color: var(--accent-emerald);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        border: 1px solid rgba(16, 185, 129, 0.3);
      }

      .user-info {
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
        color: var(--text-muted);
        text-transform: uppercase;
      }

      /* Main Content */
      .main {
        flex: 1;
        max-width: 1360px;
        margin: 0 auto;
        padding: 36px 24px 64px;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 36px;
      }

      /* Hero Command Center */
      .hero {
        background: linear-gradient(135deg, rgba(12, 18, 27, 0.9), rgba(19, 27, 39, 0.7));
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 28px 32px;
        backdrop-filter: blur(12px);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.5);
      }

      .hero-welcome h2 {
        font-size: 26px;
        font-weight: 800;
        color: #fff;
        letter-spacing: -0.5px;
      }

      .hero-welcome p {
        font-size: 14px;
        color: var(--text-muted);
        margin-top: 4px;
      }

      /* Telemetry KPI Badges */
      .hero-kpis {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
      }

      .kpi-card {
        background: rgba(6, 9, 14, 0.65);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 12px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 130px;
      }

      .kpi-icon {
        font-size: 20px;
      }

      .kpi-label {
        font-size: 11px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-dim);
        text-transform: uppercase;
      }

      .kpi-val {
        font-size: 18px;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: #fff;
      }

      /* Sections & Cards */
      .category-section {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .category-header {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .category-icon {
        font-size: 18px;
      }

      .category-title {
        font-size: 17px;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.2px;
      }

      .category-count {
        font-size: 12px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-dim);
      }

      .app-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
        gap: 18px;
      }

      /* App Card */
      .app-card {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
        text-decoration: none;
        color: inherit;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
      }

      .app-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--card-color, var(--accent-emerald));
        opacity: 0.8;
      }

      .app-card:hover {
        transform: translateY(-4px);
        background: var(--bg-surface-elevated);
        border-color: rgba(255, 255, 255, 0.18);
        box-shadow: 0 14px 28px -6px rgba(0, 0, 0, 0.5), 0 0 16px -2px var(--card-glow, rgba(16, 185, 129, 0.2));
      }

      .app-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 14px;
      }

      .app-icon-wrap {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: var(--card-bg, rgba(16, 185, 129, 0.1));
        border: 1px solid var(--card-border, rgba(16, 185, 129, 0.25));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
      }

      .app-tag {
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-muted);
        border: 1px solid var(--border);
      }

      .app-body h3 {
        font-size: 16px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
        letter-spacing: -0.2px;
      }

      .app-body p {
        font-size: 13px;
        color: var(--text-muted);
        line-height: 1.55;
      }

      .app-footer {
        margin-top: 20px;
        padding-top: 14px;
        border-top: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 12px;
        font-weight: 600;
        color: var(--card-color, var(--accent-emerald));
      }

      .app-arrow {
        transition: transform 0.2s ease;
      }

      .app-card:hover .app-arrow {
        transform: translateX(4px);
      }

      @media (max-width: 768px) {
        .hero {
          padding: 20px;
        }
        .hero-welcome h2 {
          font-size: 22px;
        }
      }
    </style>
  </head>
  <body>
    <!-- Top Navigation -->
    <header class="header">
      <div class="header-inner">
        <a href="/" class="brand">
          <div class="brand-logo">⚡</div>
          <div class="brand-text">
            <h1>BEATTIE TECH</h1>
            <span>ECOSYSTEM HUB</span>
          </div>
        </a>

        <div class="user-pill">
          <div class="user-avatar">{displayName.charAt(0).toUpperCase()}</div>
          <div class="user-info">
            <span class="user-name">{displayName}</span>
            <span class="user-role">{role}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Learning Command Center -->
    <main class="main">
      <!-- Hero Banner & KPIs -->
      <section class="hero">
        <div class="hero-welcome">
          <h2>Welcome back, {displayName}</h2>
          <p>Access your certification training tracks, live cyber ranges, and AI lab assistants.</p>
        </div>

        <div class="hero-kpis">
          <div class="kpi-card">
            <span class="kpi-icon">⚡</span>
            <div>
              <div class="kpi-label">Level</div>
              <div class="kpi-val">{level}</div>
            </div>
          </div>
          <div class="kpi-card">
            <span class="kpi-icon">🌟</span>
            <div>
              <div class="kpi-label">XP</div>
              <div class="kpi-val">{xp}</div>
            </div>
          </div>
          <div class="kpi-card">
            <span class="kpi-icon">💎</span>
            <div>
              <div class="kpi-label">Credits</div>
              <div class="kpi-val">{credits}</div>
            </div>
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
              <span class="category-icon">{catMeta.icon}</span>
              <h2 class="category-title">{catMeta.label}</h2>
              <span class="category-count">({categoryApps.length})</span>
            </div>

            <div class="app-grid">
              {categoryApps.map((app: HubApp) => {
                const icon = APP_ICONS[app.id || ''] || '🚀';
                const cardColor = app.color || catMeta.color;

                return (
                  <a
                    href={app.url}
                    class="app-card"
                    style={{
                      '--card-color': cardColor,
                      '--card-glow': cardColor + '40',
                      '--card-bg': cardColor + '18',
                      '--card-border': cardColor + '40',
                    }}
                  >
                    <div>
                      <div class="app-header">
                        <div class="app-icon-wrap">{icon}</div>
                        <span class="app-tag">{app.id || 'app'}</span>
                      </div>
                      <div class="app-body">
                        <h3>{app.title}</h3>
                        <p>{app.description || 'Launch this learning application in the Beattie Tech ecosystem.'}</p>
                      </div>
                    </div>

                    <div class="app-footer">
                      <span>Launch App</span>
                      <span class="app-arrow">→</span>
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

fs.writeFileSync(hubIndexPath, astroTemplate);
console.log('Successfully wrote restyled index.astro to hub repo');
