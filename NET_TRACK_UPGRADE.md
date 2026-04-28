# BeattieNetTrack — UI Design Upgrade Spec
# Design Language: RoadShow → LMS

**Status:** Ready to implement  
**Source of truth:** RoadShowV1 codebase (examined 2024)  
**Applies to:** All Astro pages, React islands, global CSS tokens  
**Priority order:** Tokens → Global shell → Nav → Cards → Labs → Quiz → Progress

---

## The North Star

The RoadShow site has something BeattieNetTrack currently lacks: **personality**.
It's a dark, neon-accented, gamified environment that feels like a place where
real learning happens — not a document viewer with a sidebar.

The goal is to bring that energy into the LMS without sacrificing the structural
rigor already in place. The CONSTITUTION doesn't care what color the buttons are.

---

## 1. Design Token Overhaul

**File:** `src/styles/tokens.css`

Replace the current token set wholesale. These values are extracted directly
from the RoadShow design system:

```css
:root {
  /* ── Backgrounds ── */
  --bg-main:              #020510;
  --bg-elevated:          #0a0f22;
  --bg-elevated-soft:     #0e1428;
  --bg-surface:           rgba(2, 5, 16, 0.92);
  --bg-card:              rgba(10, 15, 34, 0.90);

  /* ── Accent palette ── */
  --accent-green:         #00ffb3;
  --accent-blue:          #38d9ff;
  --accent-purple:        #c084fc;
  --accent-yellow:        #fde047;
  --danger:               #ff4b81;

  /* ── Text ── */
  --text-main:            #f1f5f9;
  --text-muted:           #94a3b8;
  --text-accent:          #38d9ff;

  /* ── Borders ── */
  --border-subtle:        rgba(255, 255, 255, 0.10);
  --border-neon:          rgba(0, 255, 179, 0.35);
  --border-blue:          rgba(56, 217, 255, 0.28);

  /* ── Radius ── */
  --radius-lg:            18px;
  --radius-md:            12px;
  --radius-pill:          999px;

  /* ── Shadows / Glows ── */
  --shadow-soft:          0 18px 45px rgba(0, 0, 0, 0.75);
  --shadow-neon-green:    0 0 24px rgba(0, 255, 179, 0.25);
  --shadow-neon-blue:     0 0 20px rgba(56, 217, 255, 0.20);

  /* ── Transitions ── */
  --transition-fast:      0.25s ease-out;
  --transition-med:       0.35s ease-out;

  /* ── Fonts (keep existing imports, just reference here) ── */
  --font-mono:            'JetBrains Mono', ui-monospace, 'Courier New', monospace;
}
```

### Light Mode (keep as opt-in toggle)
```css
html.light-mode {
  --accent-green:   #00875a;
  --accent-blue:    #0369a1;
  --accent-purple:  #7c3aed;
  --text-main:      #0f172a;
  --text-muted:     #475569;
  --bg-main:        #f0f6ff;
  --bg-elevated:    #ffffff;
  --bg-card:        rgba(255, 255, 255, 0.95);
  --border-subtle:  rgba(0, 0, 0, 0.10);
  --shadow-soft:    0 18px 45px rgba(0, 0, 0, 0.10);
}
```

---

## 2. Global Body & Background

**File:** `src/layouts/AppShell.astro` (body/html level)

### Animated binary rain background
The RoadShow's signature atmospheric element. Pure CSS animation, zero performance cost, runs in a fixed `div` behind everything.

```html
<!-- Add immediately after <body> -->
<div class="binary-bg" aria-hidden="true"></div>
```

```css
body {
  background:
    radial-gradient(ellipse at top left,  rgba(0, 255, 179, 0.18), transparent 50%),
    radial-gradient(ellipse at top right, rgba(56, 217, 255, 0.18), transparent 50%),
    radial-gradient(ellipse at bottom center, rgba(192, 132, 252, 0.22), transparent 55%),
    var(--bg-main);
  color: var(--text-main);
  overflow-x: hidden;
}

.binary-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
  opacity: 0.35;
  mix-blend-mode: screen;
}

.binary-column {
  position: absolute;
  top: -120vh;
  width: 40px;
  color: rgba(0, 255, 179, 0.55);
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.2;
  white-space: pre;
  text-shadow: 0 0 8px rgba(0, 255, 179, 0.7);
  animation: binary-fall linear infinite;
}

@keyframes binary-fall { to { transform: translateY(220vh); } }
```

**JS to add to AppShell (client-side island or inline script):**
```js
// Binary rain generator (add to client-side script)
const bg = document.querySelector('.binary-bg');
if (bg) {
  for (let i = 0; i < 32; i++) {
    const col = document.createElement('div');
    col.className = 'binary-column';
    col.style.left = `${(i / 32) * 100}%`;
    const dur = 10 + Math.random() * 10;
    col.style.animationDuration = `${dur}s`;
    col.style.animationDelay = `${-Math.random() * dur}s`;
    col.textContent = Array.from({length: 26}, () => Math.random() > 0.5 ? '1' : '0').join('\n');
    bg.appendChild(col);
  }
}
```

### Page shell (content wrapper)
```css
.page-shell {
  position: relative;
  z-index: 1;
  background: rgba(2, 5, 16, 0.91);
  border: 1px solid rgba(56, 217, 255, 0.12);
  border-radius: 16px;
  box-shadow: 0 0 60px rgba(0, 255, 179, 0.06), 0 32px 80px rgba(0, 0, 0, 0.8);
}
```

---

## 3. Top Navigation

**Current:** Static sidebar-based nav  
**Target:** Sticky top bar matching RoadShow's glassmorphism nav

```css
.top-nav {
  position: sticky;
  top: 0;
  z-index: 40;
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
  background: linear-gradient(
    to bottom,
    rgba(2, 5, 16, 0.98),
    rgba(2, 5, 16, 0.88),
    transparent
  );
  border-bottom: 1px solid rgba(56, 217, 255, 0.12);
}
```

### Brand mark
```html
<div class="brand">
  <div class="brand-icon">BN</div>    <!-- glowing gradient square -->
  <div class="brand-text">
    <span class="brand-title">BeattieNetTrack</span>
    <span class="brand-subtitle">Build Real Skills. Earn Real Certs.</span>
  </div>
</div>
```

```css
.brand-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: radial-gradient(circle at 30% 30%, var(--accent-green), var(--accent-blue));
  box-shadow: 0 0 18px rgba(0, 255, 157, 0.55), 0 0 40px rgba(49, 195, 255, 0.4);
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 14px; letter-spacing: 0.1em;
  color: #020617;
}

.brand-title {
  font-weight: 800; font-size: 13px;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--accent-green);
  text-shadow: 0 0 10px rgba(0, 255, 179, 0.6);
}
```

### Nav links (animated underline on hover)
```css
.nav-link {
  position: relative;
  font-size: 12px; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--text-muted);
  padding-bottom: 4px;
  transition: color var(--transition-fast);
}

.nav-link::after {
  content: "";
  position: absolute; left: 0; bottom: 0;
  width: 0; height: 2px;
  border-radius: var(--radius-pill);
  background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
  transition: width var(--transition-fast);
}

.nav-link:hover { color: var(--accent-green); }
.nav-link:hover::after, .nav-link.active::after { width: 100%; }
.nav-link.active { color: var(--accent-green); font-weight: 700; }
```

### Live session indicator (right side of nav)
```html
<div class="nav-cta">
  <span class="nav-cta-dot"></span>
  Live Session
</div>
```

```css
.nav-cta {
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  border: 1px solid rgba(0, 255, 157, 0.4);
  background: radial-gradient(circle at 0 0, rgba(0, 255, 157, 0.2), transparent 55%);
  color: var(--accent-green);
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 600;
  display: inline-flex; align-items: center; gap: 6px;
}

.nav-cta-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--accent-green);
  box-shadow: 0 0 8px rgba(0, 255, 157, 0.9);
  animation: pulse 1.3s infinite alternate;
}

@keyframes pulse {
  from { transform: scale(0.9); opacity: 0.7; }
  to   { transform: scale(1.15); opacity: 1; }
}
```

---

## 4. Cards (Module / Lesson / Lab / Quiz)

Replace the current flat cards throughout the system.

```css
.card {
  background: linear-gradient(145deg, rgba(56, 217, 255, 0.05) 0%, rgba(2, 5, 16, 0.5) 60%);
  border-radius: var(--radius-lg);
  padding: 20px;
  border: 1px solid var(--border-blue);
  border-top: 3px solid var(--accent-blue);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast), border-color var(--transition-fast);
  display: flex; flex-direction: column; gap: 12px;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 255, 179, 0.15);
  border-top-color: var(--accent-green);
  border-color: rgba(0, 255, 179, 0.3);
}
```

### Card variants by content type

| Type | Border-top color | Hover glow color |
|---|---|---|
| Lesson (reading) | `--accent-blue` | blue |
| Lab (hands-on) | `--accent-green` | green |
| Quiz | `--accent-purple` | purple |
| Track overview | gradient green→blue | green |

### Status badges on cards
```css
.card-status {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: var(--text-muted);
  margin-bottom: 4px;
}

.card-status.done {
  color: var(--accent-green);
  text-shadow: 0 0 6px rgba(0, 255, 179, 0.4);
}
```

---

## 5. Progress System (XP, Streaks, Track Progress)

**Component:** `src/components/islands/TrackProgressSummary.tsx`

### Progress header (sits above activity grids)
```css
.progress-header {
  background: rgba(2, 5, 16, 0.9);
  border: 1px solid rgba(0, 255, 179, 0.2);
  border-left: 4px solid var(--accent-green);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  margin-bottom: 28px;
  display: flex; flex-wrap: wrap; align-items: center; gap: 20px;
  box-shadow: 0 0 20px rgba(0, 255, 179, 0.06);
}
```

### Progress bar
```css
.progress-bar-track {
  height: 10px; border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.08); overflow: hidden;
}

.progress-bar-fill {
  height: 100%; border-radius: var(--radius-pill);
  background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
  transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 0 12px rgba(0, 255, 179, 0.5);
}
```

### XP display (star tally)
```html
<div class="xp-display">
  <span class="xp-icon">⚡</span>
  <span class="xp-value" id="xp-count">0</span>
  <span class="xp-label">XP</span>
</div>
```

```css
.xp-display {
  display: flex; align-items: center; gap: 6px;
  font-size: 22px; font-weight: 700;
  color: var(--accent-yellow);
  text-shadow: 0 0 10px rgba(253, 224, 71, 0.5);
}
```

### Gamification copy (motivational subtitles)
When rendering progress subtitle, use this message ladder:

```ts
const PROGRESS_MESSAGES = [
  "Just getting started — your journey begins here.",
  "First checkpoint! Keep that momentum.",
  "Two down. You're building something real.",
  "Halfway through — nobody quits at the halfway point.",
  "More than half! The cert is within reach.",
  "Almost there — don't stop now.",
  "One more and you're a certified badass.",
  "🎉 Track complete! You earned this.",
];
```

---

## 6. Lab Runner (`QuizRunner.tsx` / LabRunner)

This is the highest-impact area. Labs need to feel like missions, not forms.

### Terminal simulator styling
```css
.terminal {
  background: #0a0a0a;
  border: 1px solid rgba(0, 255, 179, 0.25);
  border-radius: var(--radius-md);
  font-family: var(--font-mono);
  font-size: 14px;
  padding: 12px;
  min-height: 220px;
  display: flex; flex-direction: column;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(0, 255, 179, 0.03);
  position: relative;
  overflow: hidden;
}

/* CRT scanline effect (subtle, optional) */
.terminal::before {
  content: "";
  position: absolute; inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.03) 2px,
    rgba(0, 0, 0, 0.03) 4px
  );
  pointer-events: none; z-index: 1;
}

.terminal-output {
  flex-grow: 1; white-space: pre-wrap; word-break: break-all;
  color: rgba(0, 255, 179, 0.9);
  line-height: 1.5;
}

.terminal-input {
  background: transparent; border: none;
  color: rgba(0, 255, 179, 0.9);
  font-family: var(--font-mono); font-size: 14px;
  flex-grow: 1; outline: none; caret-color: var(--accent-green);
}

.prompt { color: var(--accent-green); }
```

### Lab step tracker (sidebar within a lab)
```css
.lab-steps {
  display: flex; flex-direction: column; gap: 4px;
  padding: 16px; 
  background: rgba(2, 5, 16, 0.8);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.lab-step {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px; color: var(--text-muted);
  transition: all var(--transition-fast);
}

.lab-step.active {
  background: rgba(0, 255, 179, 0.08);
  border: 1px solid rgba(0, 255, 179, 0.2);
  color: var(--accent-green);
}

.lab-step.complete {
  color: var(--accent-green);
  opacity: 0.7;
}

.lab-step-num {
  width: 22px; height: 22px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700;
  background: rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

.lab-step.active .lab-step-num {
  background: var(--accent-green);
  color: #020510;
}

.lab-step.complete .lab-step-num::after {
  content: "✓";
}
```

### Lab success flash
When a step is completed, flash a celebratory overlay:

```css
@keyframes successPop {
  0%   { opacity: 0; transform: scale(0.8); }
  50%  { opacity: 1; transform: scale(1.05); }
  100% { opacity: 0; transform: scale(1); }
}

.step-success-toast {
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
  background: rgba(0, 255, 179, 0.15);
  border: 2px solid var(--accent-green);
  border-radius: var(--radius-lg);
  padding: 20px 32px;
  font-size: 18px; font-weight: 700; color: var(--accent-green);
  text-shadow: 0 0 20px rgba(0, 255, 179, 0.8);
  animation: successPop 1.2s ease forwards;
  z-index: 1000; pointer-events: none;
  box-shadow: 0 0 60px rgba(0, 255, 179, 0.3);
}
```

---

## 7. Quiz Runner

### Question area
```css
.quiz-question-card {
  background: rgba(10, 15, 34, 0.9);
  border: 1px solid var(--border-blue);
  border-top: 3px solid var(--accent-purple);
  border-radius: var(--radius-lg);
  padding: 28px;
}

.quiz-question-text {
  font-size: 18px;
  line-height: 1.6;
  color: var(--text-main);
  margin-bottom: 20px;
}
```

### Answer options (radio replacement)
```css
.quiz-option {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 14px 18px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: 8px;
  background: rgba(2, 5, 16, 0.5);
}

.quiz-option:hover {
  border-color: var(--accent-blue);
  background: rgba(56, 217, 255, 0.05);
}

.quiz-option.selected {
  border-color: var(--accent-purple);
  background: rgba(192, 132, 252, 0.08);
}

.quiz-option.correct {
  border-color: var(--accent-green);
  background: rgba(0, 255, 179, 0.08);
}

.quiz-option.incorrect {
  border-color: var(--danger);
  background: rgba(255, 75, 129, 0.08);
}
```

### ELI5 explanation (already exists — style upgrade only)
```css
.quiz-feedback__eli5 {
  margin-top: 16px;
  border-radius: var(--radius-md);
  background: rgba(0, 255, 179, 0.04);
  border: 1px solid rgba(0, 255, 179, 0.22);
  overflow: hidden;
}

.quiz-feedback__eli5-toggle {
  width: 100%; background: none; border: none;
  padding: 12px 16px;
  display: flex; align-items: center; gap: 8px;
  cursor: pointer; color: var(--accent-green);
  font-size: 12px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; text-align: left;
  text-shadow: 0 0 8px rgba(0, 255, 179, 0.35);
  transition: background var(--transition-fast);
}

.quiz-feedback__eli5-toggle:hover {
  background: rgba(0, 255, 157, 0.08);
}

.quiz-feedback__eli5-body {
  padding: 0 16px 14px;
  font-size: 15px; color: var(--text-muted); line-height: 1.75;
}

.quiz-feedback__eli5-body strong { color: var(--accent-green); }
.quiz-feedback__eli5-body code {
  background: rgba(56, 217, 255, 0.1);
  border: 1px solid rgba(56, 217, 255, 0.2);
  border-radius: 4px; padding: 1px 5px;
  font-family: var(--font-mono); font-size: 12px; color: var(--accent-blue);
}
```

---

## 8. Buttons

### Primary (CTA)
```css
.btn-primary {
  padding: 12px 24px; border-radius: var(--radius-pill); border: none;
  font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em;
  cursor: pointer;
  background: linear-gradient(135deg, var(--accent-green), var(--accent-blue));
  color: #020617;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 40px rgba(0, 0, 0, 0.75);
}
```

### Ghost / secondary
```css
.btn-ghost {
  padding: 12px 24px; border-radius: var(--radius-pill);
  border: 2px solid var(--accent-blue);
  background: rgba(7, 10, 30, 0.75);
  color: var(--accent-blue);
  font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.14em;
  cursor: pointer;
  transition: background var(--transition-fast), transform var(--transition-fast);
}

.btn-ghost:hover { background: rgba(56, 217, 255, 0.1); transform: translateY(-1px); }
```

---

## 9. J. Code Mascot (LMS Version)

J. Code is the RoadShow mascot. For BeattieNetTrack, adapt the concept:
- Same bubble UI pattern
- LMS-appropriate tips (cert facts, study tips, encouraging messages, "RAID is not a backup" reminders)
- Appears on lesson, lab, and quiz pages
- Dismissible; remembers dismissed state per session

### Implementation
Add `data-jcode="..."` attribute to the `<body>` of each page template.
The JS in `common.js` (or Astro equivalent) injects the bubble automatically.

```css
.jcode-bubble {
  position: fixed; bottom: 80px; right: 20px;
  background: rgba(2, 5, 16, 0.96);
  border: 2px solid var(--accent-green);
  border-radius: 16px 16px 4px 16px;
  padding: 14px 16px 12px;
  max-width: 280px;
  box-shadow: 0 0 24px rgba(0, 255, 179, 0.25), 0 8px 30px rgba(0, 0, 0, 0.8);
  animation: jcodeSlideUp 0.45s ease 0.5s both;
  z-index: 200;
}

@keyframes jcodeSlideUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### LMS tip bank (add to page frontmatter or template data)
```yaml
# Lesson pages
jcode: "📡 Fun fact: The OSI model was standardized in 1984 — the same year the Macintosh launched. Network+ loves asking about all 7 layers!"

# Lab pages  
jcode: "🖥️ Pro move: try the command, read the output, then try again. Real sysadmins iterate constantly. You're training the right habit."

# Quiz pages
jcode: "🧠 Test tip: eliminate wrong answers first. On CompTIA exams, two options are usually obviously wrong — find those first, then decide between the two that remain."

# RAID content (always)
jcode: "⚠️ Remember: RAID is NOT a backup. RAID protects against drive failure. Ransomware, accidental deletion, and fire affect every drive in the array equally."
```

---

## 10. Section / Page Eyebrows and Headers

Adapt the RoadShow section header pattern for LMS content pages.

```html
<!-- Lesson page header example -->
<div class="section-eyebrow">Unit 1.1 · Network+ N10-009</div>
<h1 class="section-title">The OSI Model</h1>
<p class="section-subtitle">Seven layers. One framework. The foundation every network conversation builds on.</p>
```

```css
.section-eyebrow {
  font-size: 11px; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--accent-green);
  margin-bottom: 8px; font-weight: 600;
}

.section-title {
  font-size: clamp(22px, 3.5vw, 32px);
  font-weight: 700; line-height: 1.15;
  color: var(--text-main);
}

.section-title span {
  background: linear-gradient(120deg, var(--accent-green), var(--accent-blue), var(--accent-purple));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}

.section-subtitle {
  font-size: 16px; color: var(--text-muted);
  max-width: 560px; line-height: 1.7; margin-top: 8px;
}
```

---

## 11. Code Blocks (in Lesson Body)

```css
.code-block {
  background: rgba(0, 0, 0, 0.55);
  border: 1px solid rgba(56, 217, 255, 0.2);
  border-left: 3px solid var(--accent-blue);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: 12px 16px;
  font-family: var(--font-mono);
  font-size: 13px; color: var(--accent-green);
  line-height: 1.7; overflow-x: auto; white-space: pre;
}

.code-block .comment { color: var(--text-muted); font-style: italic; }
.code-block .keyword { color: var(--accent-purple); }
.code-block .string  { color: var(--accent-green); }
```

---

## 12. Theme Toggle

Add the light/dark toggle to nav, identical to RoadShow:

```css
.theme-toggle-btn {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.20);
  border-radius: var(--radius-pill);
  color: var(--text-muted);
  font-size: 13px; font-weight: 600;
  padding: 6px 14px; cursor: pointer;
  display: inline-flex; align-items: center; gap: 8px;
  min-width: 130px;
  transition: background var(--transition-fast);
}
```

---

## 13. Callouts / Info Boxes

```css
.callout {
  border-radius: 8px; padding: 14px 18px; margin: 16px 0;
  display: flex; gap: 12px; align-items: flex-start;
  font-size: 15px;
}

.callout.info    { background: rgba(56, 217, 255, 0.07); border: 1px solid rgba(56, 217, 255, 0.2); }
.callout.success { background: rgba(0, 255, 179, 0.07); border: 1px solid rgba(0, 255, 179, 0.2); }
.callout.warning { background: rgba(249, 115, 22, 0.08); border: 1px solid rgba(249, 115, 22, 0.2); }
.callout.danger  { background: rgba(255, 75, 129, 0.08); border: 1px solid rgba(255, 75, 129, 0.2); }

.callout p { margin: 0; color: var(--text-muted); }
.callout strong { color: var(--text-main); }
```

---

## Implementation Sequence

Work this in order. Each step is independently shippable and improves the site on its own.

| Step | What | Est. effort | Impact |
|---|---|---|---|
| 1 | Replace tokens.css | 30 min | 🔥🔥🔥 |
| 2 | Add binary rain background to AppShell | 45 min | 🔥🔥🔥 |
| 3 | Restyle top nav | 1 hour | 🔥🔥🔥 |
| 4 | Restyle cards globally | 1.5 hours | 🔥🔥 |
| 5 | Progress bar / XP system styling | 1 hour | 🔥🔥 |
| 6 | Quiz option styling | 1 hour | 🔥🔥 |
| 7 | Terminal / lab styling | 1 hour | 🔥🔥 |
| 8 | ELI5 accordion styling | 30 min | 🔥 |
| 9 | J. Code mascot integration | 1.5 hours | 🔥🔥 |
| 10 | Buttons, callouts, code blocks | 1 hour | 🔥 |

---

## Key Decisions

- **Keep the sidebar nav** — the RoadShow uses a top-only nav because it's a single-purpose roadshow. BeattieNetTrack's sidebar is genuinely useful for course navigation at scale. Style the sidebar to match the dark aesthetic rather than replacing it.
- **Don't remove the Fraunces/Space Grotesk fonts** — they're already distinctive and complement the dark aesthetic.
- **Binary rain opacity at 0.35, not 0.55** — the LMS has more reading content than the roadshow; keep the effect atmospheric, not distracting.
- **Labs get the terminal styling** — even if the lab backend changes (Phase 4 live containers), the front-end terminal chrome doesn't need to change.
- **J. Code is optional per-page** — not every page needs the mascot. Add it to activity pages, not to admin/settings pages.