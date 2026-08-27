import os

TARGET_DIR = r"c:\CustomApps\26_27_ LessonsAndAgendas"
os.makedirs(TARGET_DIR, exist_ok=True)

print("Starting generation of fully translated CompTIA 6-Step Lesson & Activity Suite (EN, AR, UK)...")

# ==============================================================================
# 1. GENERATE PRESENTATION.HTML WITH FULL DYNAMIC MULTILINGUAL ENGINE
# ==============================================================================
presentation_html_path = os.path.join(TARGET_DIR, "presentation.html")

presentation_py = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Divide &amp; Conquer // CompTIA 6-Step Troubleshooting Mastery</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg: #040608;
      --panel: #090e13;
      --panel-elevated: #101720;
      --line: #1b272c;
      --line-bright: #2d424b;
      --green: #39ff9e;
      --green-glow: rgba(57, 255, 158, 0.35);
      --green-dim: #134e35;
      --cyan: #38bdf8;
      --cyan-glow: rgba(56, 189, 248, 0.35);
      --amber: #ffb454;
      --red: #ff5c72;
      --purple: #a855f7;
      --text: #e2f4ea;
      --text-muted: #829a90;
      --text-dim: #4d665c;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'JetBrains Mono', monospace;
      min-height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
      position: relative;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(57, 255, 158, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(57, 255, 158, 0.04) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 1;
    }

    body::after {
      content: "";
      position: fixed;
      inset: 0;
      background: 
        repeating-linear-gradient(to bottom, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 2px, rgba(0,0,0,0.18) 3px, rgba(0,0,0,0) 4px),
        radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.7) 100%);
      pointer-events: none;
      mix-blend-mode: multiply;
      z-index: 2;
    }

    :root:lang(ar) {
      font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif;
    }

    [dir="rtl"] {
      text-align: start;
    }

    [dir="rtl"] code,
    [dir="rtl"] pre,
    [dir="rtl"] .font-mono,
    [dir="rtl"] .cli-box {
      direction: ltr !important;
      unicode-bidi: isolate;
      text-align: left;
    }

    .topbar {
      position: relative;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 2rem;
      border-bottom: 1px solid var(--line);
      background: rgba(9, 14, 19, 0.85);
      backdrop-filter: blur(8px);
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: #fff;
    }
    .brand-dot { color: var(--green); animation: pulse 2s infinite; }

    .nav-controls {
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }

    .btn-ctrl {
      background: var(--panel-elevated);
      border: 1px solid var(--line-bright);
      color: var(--text);
      padding: 0.35rem 0.8rem;
      border-radius: 4px;
      font-family: inherit;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.15s ease;
      text-decoration: none;
    }
    .btn-ctrl:hover {
      border-color: var(--green);
      color: var(--green);
      box-shadow: 0 0 10px var(--green-glow);
    }
    .btn-ctrl.active {
      background: var(--green-dim);
      border-color: var(--green);
      color: var(--green);
    }

    .slide-counter {
      font-weight: 800;
      color: var(--green);
      font-size: 0.85rem;
      letter-spacing: 0.05em;
      padding: 0 0.5rem;
    }

    .stage {
      position: relative;
      z-index: 5;
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem 3rem;
      overflow: hidden;
    }

    .slide {
      position: absolute;
      width: 100%;
      max-width: 1350px;
      height: 82vh;
      max-height: 850px;
      background: var(--panel);
      border: 1px solid var(--line-bright);
      border-radius: 12px;
      padding: 2.2rem 3rem;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(57, 255, 158, 0.03);
      opacity: 0;
      transform: translateX(60px) scale(0.97);
      pointer-events: none;
      transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1), transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
    }

    .slide.active {
      opacity: 1;
      transform: translateX(0) scale(1);
      pointer-events: auto;
    }

    .slide.prev {
      opacity: 0;
      transform: translateX(-60px) scale(0.97);
    }

    .slide-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--green);
      background: rgba(57, 255, 158, 0.08);
      border: 1px solid var(--green-dim);
      padding: 0.3rem 0.8rem;
      border-radius: 4px;
      width: fit-content;
      margin-bottom: 0.8rem;
    }

    .slide-badge.cyan { color: var(--cyan); background: rgba(56, 189, 248, 0.08); border-color: rgba(56, 189, 248, 0.3); }
    .slide-badge.amber { color: var(--amber); background: rgba(255, 180, 84, 0.08); border-color: rgba(255, 180, 84, 0.3); }
    .slide-badge.purple { color: var(--purple); background: rgba(168, 85, 247, 0.08); border-color: rgba(168, 85, 247, 0.3); }
    .slide-badge.red { color: var(--red); background: rgba(255, 92, 114, 0.08); border-color: rgba(255, 92, 114, 0.3); }

    .slide-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: clamp(1.8rem, 3vw, 2.6rem);
      font-weight: 700;
      color: #fff;
      line-height: 1.15;
      margin-bottom: 0.4rem;
      letter-spacing: -0.02em;
    }

    .slide-subtitle {
      font-size: 1rem;
      color: var(--text-muted);
      margin-bottom: 1.8rem;
      line-height: 1.5;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.6rem;
      flex: 1;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 1.4rem;
      flex: 1;
    }

    .grid-6 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 1.2rem;
      flex: 1;
    }

    .card {
      background: var(--panel-elevated);
      border: 1px solid var(--line-bright);
      border-radius: 8px;
      padding: 1.3rem 1.5rem;
      position: relative;
      display: flex;
      flex-direction: column;
      transition: all 0.2s ease;
    }
    .card:hover {
      border-color: var(--green);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    .card-num {
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--green);
      margin-bottom: 0.4rem;
      font-family: 'Space Grotesk', sans-serif;
    }
    .card-num.cyan { color: var(--cyan); }
    .card-num.amber { color: var(--amber); }
    .card-num.red { color: var(--red); }
    .card-num.purple { color: var(--purple); }

    .card-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 0.5rem;
      font-family: 'Space Grotesk', sans-serif;
    }

    .card-desc {
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.6;
    }

    .card-desc strong { color: #fff; }

    .card-tag {
      margin-top: auto;
      padding-top: 0.8rem;
      font-size: 0.72rem;
      color: var(--green);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-weight: 700;
    }

    .cli-box {
      background: #020305;
      border: 1px solid var(--line);
      border-left: 3px solid var(--green);
      padding: 0.8rem 1.1rem;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: var(--green);
      margin: 0.7rem 0;
      white-space: pre-wrap;
    }

    .cli-box.amber { border-left-color: var(--amber); color: var(--amber); }
    .cli-box.cyan { border-left-color: var(--cyan); color: var(--cyan); }
    .cli-box.red { border-left-color: var(--red); color: var(--red); }

    .sim-container {
      background: #020305;
      border: 1px solid var(--line-bright);
      border-radius: 8px;
      padding: 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .osi-ladder {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .osi-step {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.65rem 1.1rem;
      background: var(--panel-elevated);
      border: 1px solid var(--line);
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .osi-step:hover {
      border-color: var(--cyan);
      background: #141e2b;
    }
    .osi-step.selected {
      border-color: var(--green);
      background: rgba(57, 255, 158, 0.1);
      box-shadow: 0 0 15px rgba(57, 255, 158, 0.2);
    }
    .osi-step.failed {
      border-color: var(--red);
      background: rgba(255, 92, 114, 0.1);
    }

    .osi-step-left {
      display: flex;
      align-items: center;
      gap: 0.9rem;
    }
    .osi-num {
      font-weight: 800;
      color: var(--cyan);
      font-size: 0.85rem;
      width: 2rem;
    }
    .osi-name {
      font-weight: 700;
      color: #fff;
      font-size: 0.9rem;
    }
    .osi-cmd {
      font-size: 0.75rem;
      color: var(--amber);
    }

    .osi-status {
      font-weight: 800;
      font-size: 0.72rem;
      padding: 0.2rem 0.55rem;
      border-radius: 3px;
      text-transform: uppercase;
    }
    .osi-status.pass { background: rgba(57, 255, 158, 0.2); color: var(--green); }
    .osi-status.fail { background: rgba(255, 92, 114, 0.2); color: var(--red); }
    .osi-status.untested { background: rgba(255, 255, 255, 0.05); color: var(--text-muted); }

    .bottombar {
      position: relative;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.8rem 2rem;
      border-top: 1px solid var(--line);
      background: rgba(9, 14, 19, 0.95);
      backdrop-filter: blur(8px);
    }

    .progress-track {
      flex: 1;
      height: 4px;
      background: var(--line);
      margin: 0 2rem;
      border-radius: 2px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--cyan), var(--green));
      width: 6.66%;
      transition: width 0.3s ease;
      box-shadow: 0 0 8px var(--green-glow);
    }

    .key-hints {
      font-size: 0.75rem;
      color: var(--text-dim);
      display: flex;
      gap: 1rem;
    }
    .key-hints span kbd {
      background: var(--panel-elevated);
      border: 1px solid var(--line-bright);
      padding: 0.15rem 0.4rem;
      border-radius: 3px;
      color: var(--text-muted);
      font-weight: 700;
    }

    .presenter-drawer {
      position: fixed;
      bottom: 60px;
      left: 2rem;
      right: 2rem;
      max-height: 220px;
      background: #020305;
      border: 1px solid var(--amber);
      border-radius: 8px;
      padding: 1.2rem 1.6rem;
      z-index: 100;
      box-shadow: 0 10px 40px rgba(0,0,0,0.9);
      display: none;
      overflow-y: auto;
    }
    .presenter-drawer.open { display: block; }
    .presenter-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.6rem;
      color: var(--amber);
      font-weight: 800;
      font-size: 0.8rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }
    .presenter-text {
      font-size: 0.9rem;
      line-height: 1.6;
      color: #fed7aa;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }
  </style>
</head>
<body>

  <header class="topbar">
    <div class="brand">
      <span class="brand-dot">●</span>
      <span id="brand-text">BEATTIE-NET // CYBER &amp; NET ENGINEERING</span>
      <span style="color: var(--text-dim);">|</span>
      <span id="brand-sub" style="color: var(--cyan); font-weight: 600;">COMPTIA 6-STEP TROUBLESHOOTING</span>
    </div>

    <div class="nav-controls">
      <div style="display:flex; background:var(--panel-elevated); border:1px solid var(--line-bright); border-radius:4px; padding:2px; font-size:0.75rem;">
        <button id="lang-en" class="btn-ctrl active" onclick="setLanguage('en')" style="border:none; padding:0.2rem 0.6rem;">EN</button>
        <button id="lang-ar" class="btn-ctrl" onclick="setLanguage('ar')" style="border:none; padding:0.2rem 0.6rem;">عربي</button>
        <button id="lang-uk" class="btn-ctrl" onclick="setLanguage('uk')" style="border:none; padding:0.2rem 0.6rem;">УКР</button>
      </div>

      <button id="btn-notes" class="btn-ctrl" onclick="toggleNotes()" title="Toggle Instructor Teaching Notes (Press 'N')">
        📝 <span id="txt-notes">Notes [N]</span>
      </button>
      
      <button id="btn-fs" class="btn-ctrl" onclick="toggleFullScreen()" title="Fullscreen Mode (Press 'F')">
        ⛶ <span id="txt-fs">Fullscreen [F]</span>
      </button>

      <a href="activity.html" class="btn-ctrl" style="border-color:var(--green); color:var(--green);">
        ⚡ <span id="txt-act">Launch Lab Activity →</span>
      </a>
    </div>
  </header>

  <main class="stage" id="stage">
    <!-- Slide container dynamically populated by renderSlide() -->
  </main>

  <aside id="presenter-drawer" class="presenter-drawer">
    <div class="presenter-header">
      <span id="txt-notes-header">TEACHER PRESENTER NOTES // MR. L'S GUIDE</span>
      <button onclick="toggleNotes()" style="background:none; border:none; color:var(--amber); cursor:pointer; font-weight:bold;">[X]</button>
    </div>
    <div id="presenter-content" class="presenter-text"></div>
  </aside>

  <footer class="bottombar">
    <div class="key-hints">
      <span id="hint-prev"><kbd>&larr;</kbd> Previous</span>
      <span id="hint-next"><kbd>&rarr;</kbd> Next</span>
      <span id="hint-adv"><kbd>Space</kbd> Advance</span>
      <span id="hint-notes"><kbd>N</kbd> Notes</span>
      <span id="hint-fs"><kbd>F</kbd> Fullscreen</span>
    </div>

    <div class="progress-track">
      <div id="progress-fill" class="progress-fill"></div>
    </div>

    <div style="display:flex; align-items:center; gap:0.6rem;">
      <button class="btn-ctrl" onclick="prevSlide()" id="btn-prev">&larr; PREV</button>
      <span id="slide-counter" class="slide-counter">01 / 15</span>
      <button class="btn-ctrl" onclick="nextSlide()" id="btn-next">NEXT &rarr;</button>
    </div>
  </footer>

  <script>
    // FULL MULTILINGUAL SLIDE DATABASE (EN, AR, UK)
    const SLIDES_DB = {
      en: {
        brand: "BEATTIE-NET // CYBER & NET ENGINEERING",
        sub: "COMPTIA 6-STEP TROUBLESHOOTING",
        notes: "Notes [N]",
        fs: "Fullscreen [F]",
        act: "Launch Lab Activity →",
        prev: "← PREV",
        next: "NEXT →",
        notesHeader: "TEACHER PRESENTER NOTES // MR. L'S GUIDE",
        hints: { prev: "Previous", next: "Next", adv: "Advance", notes: "Notes", fs: "Fullscreen" },
        slides: [
          {
            badge: "LESSON // COMPTIA CORE METHODOLOGY",
            title: "Divide & Conquer: The 6-Step Model",
            subtitle: "Systematic Fault Isolation, Binary Search Troubleshooting, & Enterprise Triage",
            layout: "grid-2",
            cards: [
              { num: "01", col: "green", title: "Stop Guessing. Start Isolating.", desc: "Amateur technicians guess and swap random cables. Enterprise network engineers and ethical hackers use <strong>formal deductive models</strong>. Today, you master the exact 6-step framework codified by <strong>CompTIA A+, Network+, and Security+</strong>.", cli: "root@beattie-net:~# ./isolate_fault.sh --target=\"enterprise-network\"\n[+] Establishing baseline telemetry...\n[+] Initializing 6-step diagnostic protocol...", tag: "CompTIA A+ (220-1101/1102) · Network+ (N10-008/009)" },
              { num: "02", col: "cyan", title: "The Binary Search Algorithm", desc: "Linear troubleshooting takes O(N) time. By applying <strong>Divide & Conquer at the OSI midpoint</strong> (Layer 3/4), you eliminate 50% of the entire problem space in a single CLI command (`ping 127.0.0.1` → `ping gateway` → `ping 8.8.8.8` → `nslookup`).", cli: "Algorithm Efficiency:\n7 Linear Tests -> 100% Time\nDivide & Conquer (3 Tests) -> 57% Faster Mean Time to Resolution (MTTR)", tag: "Mean Time to Resolution (MTTR) Optimization" }
            ],
            notes: "SLIDE 1: Hook the class immediately. Ask students: 'When your Wi-Fi drops at home, what is the first thing you do?' Point out that pulling random plugs without knowing what layer failed is amateur. Introduce the 6 steps as the universal CompTIA standard."
          },
          {
            badge: "INDUSTRY REALITY CHECK",
            badgeClass: "amber",
            title: "The High Cost of Random Guessing",
            subtitle: "Why systematic diagnosis is mandatory in corporate and cybersecurity environments",
            layout: "grid-3",
            cards: [
              { num: "01", col: "red", title: "Wasted Downtime ($$$)", desc: "In enterprise datacenters, network downtime averages <strong>$5,600 per minute</strong>. Swapping parts randomly without a verified hypothesis creates multi-hour outages that cost companies millions.", tag: "Financial & Operational Risk" },
              { num: "02", col: "amber", title: "Collateral Damage", desc: "Modifying settings, rebooting production routers, or updating drivers without an action plan often breaks <strong>unrelated dependent services</strong>, multiplying one ticket into fifty.", tag: "Configuration Drift & Chaos" },
              { num: "03", col: "green", title: "Un-reproducible Fixes", desc: "If you tweak six settings simultaneously and the network starts working, <strong>which one fixed it?</strong> You don't know, and when it breaks next week, you will start from square one.", tag: "Scientific Methodology" }
            ],
            notes: "SLIDE 2: Business context. Emphasize downtime cost. In modern hospitals, data centers, and trading firms, network downtime is an existential crisis. Ask students what happens if you reboot a core switch during school testing."
          },
          {
            badge: "THE COMPTIA 6-STEP STANDARD",
            badgeClass: "cyan",
            title: "The Complete Troubleshooting Lifecycle",
            subtitle: "The industry-standard sequential methodology required for CompTIA Certification",
            layout: "grid-6",
            cards: [
              { num: "1", col: "green", title: "Identify the Problem", desc: "Question the user, identify changes, review system logs, duplicate the symptom." },
              { num: "2", col: "cyan", title: "Establish a Theory", desc: "Question the obvious. Consider Top-to-Bottom, Bottom-to-Top, or Divide & Conquer." },
              { num: "3", col: "amber", title: "Test the Theory", desc: "Confirm root cause. If disproven, form a new theory or escalate immediately." },
              { num: "4", col: "purple", title: "Plan & Implement", desc: "Establish action plan, identify potential side effects, and safely execute solution." },
              { num: "5", col: "green", title: "Verify & Prevent", desc: "Verify full functionality with user; implement proactive preventive measures." },
              { num: "6", col: "cyan", title: "Document Everything", desc: "Record findings, actions, and outcomes in enterprise ticketing & knowledge base." }
            ],
            notes: "SLIDE 3: The Complete Lifecycle. Have the class repeat the 6 steps aloud: Identify, Theorize, Test, Plan/Implement, Verify/Prevent, Document. Highlight that Step 5 (preventative) and Step 6 (documentation) are where good techs become senior engineers."
          },
          {
            badge: "STEP 1 IN-DEPTH",
            title: "Step 1: Identify the Problem",
            subtitle: "Gathering raw telemetry before touching a single configuration file",
            layout: "grid-2",
            cards: [
              { num: "01", col: "green", title: "Interrogation & Change Tracking", desc: "Users rarely report the technical root cause; they report symptoms (e.g. <em>'The server is dead'</em>). Your job:<br><br>• <strong>User Questioning:</strong> When did it start? What exactly were you doing?<br>• <strong>Environmental Changes:</strong> Was new software installed? Was an OS update pushed overnight?<br>• <strong>Duplication:</strong> Can you replicate the exact failure on command?<br>• <strong>Scope Determination:</strong> Is this 1 workstation, 1 VLAN, or the entire building?" },
              { num: "02", col: "cyan", title: "Telemetry & Log Extraction", desc: "Always inspect authoritative system telemetry before theorizing:", cli: "# Windows PowerShell Diagnostic Commands:\nGet-EventLog -LogName System -Newest 10 -EntryType Error\nipconfig /all\nTest-NetConnection -ComputerName 10.0.0.1 -Port 443\n\n# Linux Forensic Inspection:\njournalctl -xe -u networking.service\ndmesg | grep -E \"eth|wlan|link\"" }
            ],
            notes: "SLIDE 4: Step 1 (Identify). Teach students how to ask open-ended vs closed-ended questions. Ask: 'What is the danger of trusting the user when they say the server is down?' Check logs and verify scope first."
          },
          {
            badge: "STEPS 2 & 3 IN-DEPTH",
            badgeClass: "cyan",
            title: "Step 2 & 3: Theorize & Falsify",
            subtitle: "Hypothesis generation and rapid scientific testing",
            layout: "grid-2",
            cards: [
              { num: "02", col: "cyan", title: "Establish Theory of Probable Cause", desc: "<strong>Question the Obvious:</strong> Is the patch cable disconnected? Is caps lock on? Did the DHCP lease expire?<br><br>Rank your theories by likelihood. Always test the least invasive, highest-probability hypothesis first.", cli: "Theory A (Highest Prob): Local DNS resolver timeout\nTheory B (Medium Prob): Default gateway dropped ARP\nTheory C (Low Prob): ISP fiber cut across town" },
              { num: "03", col: "amber", title: "Test the Theory (Falsification)", desc: "Execute targeted, isolated tests. A good test produces a clean binary outcome: <strong>CONFIRMED</strong> or <strong>DISPROVEN</strong>.<br><br><strong>Critical Rule:</strong> If your test disproves the theory, do not fix anything! Form a new theory or escalate.", cli: "C:\\> ping 8.8.8.8  -> Reply from 8.8.8.8 (PASS!)\nC:\\> nslookup google.com -> DNS request timed out (FAIL!)\n[+] THEORY CONFIRMED: IP routing works; DNS resolution failed." }
            ],
            notes: "SLIDE 5: Steps 2 & 3. Falsification! Explain that a failed test is great news because it permanently eliminates a wrong direction. Emphasize: DO NOT fix anything in Step 3; Step 3 is only for testing!"
          },
          {
            badge: "STEP 4 IN-DEPTH",
            badgeClass: "purple",
            title: "Step 4: Plan of Action & Implementation",
            subtitle: "Safe execution with change management, risk mitigation, & rollback plans",
            layout: "grid-2",
            cards: [
              { num: "01", col: "purple", title: "Constructing the Action Plan", desc: "Never deploy a fix blind. A professional action plan consists of three core pillars:<br><br>• <strong>Step-by-Step Remediation:</strong> Exact commands, config syntax, and files to modify.<br>• <strong>Potential Side Effects:</strong> Will bouncing this switch interface drop active VoIP phone calls in room 204?<br>• <strong>Rollback Protocol:</strong> If the update corrupts the database, how do you restore the exact previous snapshot in under 5 minutes?" },
              { num: "02", col: "cyan", title: "Change Windows & Authorization", desc: "Always obtain appropriate authorization (Change Advisory Board / Lead Systems Admin) before modifying enterprise infrastructure.", cli: "ENTERPRISE CHANGE TICKET #8849\nScope: Core Switch VLAN 20 IP Helper Update\nOutage Window: 05:00 - 05:15 EST (Low impact)\nImpact Analysis: 45 Workstations will renew DHCP leases\nRollback Plan: Restore running-config from TFTP /backup/sw01_prev.cfg" }
            ],
            notes: "SLIDE 6: Step 4 (Plan & Implement). Talk about Change Management in real enterprises. Mention outage windows and rollback procedures (e.g. taking a VM snapshot before installing an update)."
          },
          {
            badge: "STEPS 5 & 6 IN-DEPTH",
            title: "Step 5 & 6: Verification & Documentation",
            subtitle: "Closing the loop, preventative hardening, and building organizational memory",
            layout: "grid-2",
            cards: [
              { num: "05", col: "green", title: "Verify & Prevent", desc: "<strong>1. Full System Verification:</strong> Do not just check your command line; have the end user perform their real daily workflow in front of you.<br><br><strong>2. Preventative Hardening:</strong> Why did it fail? If a cable failed from being stepped on, install floor raceways. If an IP address conflicted, configure DHCP reservation and Dynamic ARP Inspection (DAI)." },
              { num: "06", col: "cyan", title: "Document Findings, Actions & Outcomes", desc: "If you don't document it, the problem was never solved. Standard ticketing format:", cli: "TICKET RESOLUTION REPORT\nSymptom: Lab Workstation 12 showing 169.254.x.x (APIPA)\nRoot Cause: DHCP Scope 192.168.10.0/24 100% exhausted\nRemediation: Expanded subnet to /23, reduced lease time to 4h\nVerification: Workstation acquired 192.168.10.142; pinged Gateway\nPreventative Action: Configured 80% capacity alert on DHCP server" }
            ],
            notes: "SLIDE 7: Steps 5 & 6. Verification must involve the user. Then explain preventative maintenance: why did it happen? If a cable failed, replace it with molded boot Cat6. Show ticket documentation format."
          },
          {
            badge: "CORE STRATEGY",
            badgeClass: "cyan",
            title: "The 'Divide & Conquer' Binary Search",
            subtitle: "Slashing diagnosis time by testing the midpoint of the OSI 7-Layer Stack",
            layout: "grid-2",
            cards: [
              { num: "01", col: "red", title: "The Slow Way: Linear OSI Walk (7 Steps)", desc: "Testing Layer 1 (Cable) → Layer 2 (Switch MAC) → Layer 3 (IP Gateway) → Layer 4 (TCP Port) → Layer 5 (Session) → Layer 6 (SSL) → Layer 7 (App).", cli: "Total Sequential Tests: 7\nTime Required: 100%\nFrustration Factor: HIGH" },
              { num: "02", col: "green", title: "The Pro Way: Midpoint Binary Search (3 Steps)", desc: "Test directly at <strong>Layer 3 (Network Layer)</strong>.<br><br>• <strong>If Layer 3 PASSES:</strong> Layers 1, 2, and 3 are 100% confirmed healthy! Never touch a patch cable or switch port. Zoom straight to Layer 4-7.<br><br>• <strong>If Layer 3 FAILS:</strong> The issue is definitely in Layer 1-3. Never waste time checking browser settings, firewalls, or TLS certs." }
            ],
            notes: "SLIDE 8: Divide and Conquer Core Concept. Draw the binary search tree on the board. 7 linear tests take too long. By testing Layer 3, we cut the problem domain in half immediately."
          },
          {
            badge: "THE 5-STEP MIDPOINT LADDER",
            badgeClass: "amber",
            title: "The Golden Diagnostic Sequence",
            subtitle: "Memorize these 5 sequential CLI commands for enterprise network troubleshooting",
            layout: "ladder",
            steps: [
              { num: "1", cmd: "ping 127.0.0.1", title: "Test Local TCP/IP Stack", desc: "Verifies local NIC driver and OS protocol stack" },
              { num: "2", cmd: "ping 192.168.1.1", title: "Test Local Gateway (LAN Exit)", desc: "Verifies Patch Cable, Wall Jack, Switch, & Router Interface (L1-L3)" },
              { num: "3", cmd: "ping 8.8.8.8", title: "Test External Public IP (WAN)", desc: "Verifies ISP modem, NAT, Default Route, & WAN Internet Routing" },
              { num: "4", cmd: "nslookup google.com", title: "Test DNS Name Resolution", desc: "Verifies Port 53 DNS resolver, root hints, & caching server" },
              { num: "5", cmd: "Test-NetConnection -Port 443", title: "Test Application Port & Service", desc: "Verifies Web Daemon, TLS Handshake, & State Inspection Firewall" }
            ],
            notes: "SLIDE 9: The 5-Step Midpoint Ladder. This is the Holy Grail! 1. 127.0.0.1 (NIC). 2. Gateway (LAN). 3. 8.8.8.8 (WAN). 4. google.com (DNS). 5. Port 443 (App). Have students copy this into their notebooks."
          },
          {
            badge: "INTERACTIVE LAB DEMO",
            badgeClass: "cyan",
            title: "Live Midpoint Diagnostic Sandbox",
            subtitle: "Click each diagnostic test to see how the problem space splits in real-time",
            layout: "sim",
            notes: "SLIDE 10: Interactive Sandbox. Walk through the clicks live on the projector. Show what happens when Gateway passes vs fails."
          },
          {
            badge: "CASE STUDY 1 // TIER 1 TRIAGE",
            badgeClass: "amber",
            title: "The 169.254.x.x (APIPA) Outage",
            subtitle: "Symptom: 8 lab workstations suddenly display 'No Internet Access'",
            layout: "grid-2",
            cards: [
              { num: "01", col: "amber", title: "The Incident Scenario", desc: "Students boot up lab computers in Room 104. Link lights on NICs are solid green. However, running <code>ipconfig</code> reveals:", cli: "IPv4 Address. . . . . . . . . . . : 169.254.144.82\nSubnet Mask . . . . . . . . . . . : 255.255.0.0\nDefault Gateway . . . . . . . . . : [BLANK]", tag: "Automatic Private IP Addressing (APIPA / RFC 3927)" },
              { num: "02", col: "green", title: "Divide & Conquer Action Flow", desc: "• <strong>Step 1:</strong> Link lights on → Physical Layer 1 & 2 link are UP.<br>• <strong>Step 2:</strong> Theory → DHCP Server service crashed or scope exhausted.<br>• <strong>Step 3:</strong> Test → Check DHCP server daemon status.<br>• <strong>Step 4:</strong> Fix → Restart DHCP daemon & expand scope.<br>• <strong>Step 5:</strong> Verify → Run <code>ipconfig /renew</code> on client; verify address <code>192.168.10.45</code> received.<br>• <strong>Step 6:</strong> Document → Log DHCP lease pool expansion." }
            ],
            notes: "SLIDE 11: Case Study 1 (APIPA). Teach students why 169.254.0.0/16 happens. Link lights are green because physical Layer 1/2 is UP, but DHCP failed at Layer 3/7. Have them practice `ipconfig /renew`."
          },
          {
            badge: "CASE STUDY 2 // CYBERSECURITY TIER 2",
            badgeClass: "red",
            title: "Suspicious Outbound Port 22 Exfiltration",
            subtitle: "Symptom: Intrusion Detection System (IDS) alerts on high-bandwidth outbound SSH traffic",
            layout: "grid-2",
            cards: [
              { num: "01", col: "red", title: "The Security Incident", desc: "Snort/Suricata IDS triggers high-severity alert: <strong>Workstation-04 (192.168.10.84)</strong> is sending 2.4 GB of encrypted traffic to a known malicious Russian VPS on Port 22 (SSH).", cli: "ALERT: [1:2010935:2] ET EXPLOIT Outbound SSH Connection to Threat Intel C2 IP 185.220.101.5\nSrc: 192.168.10.84:54210 -> Dst: 185.220.101.5:22", tag: "Immediate Security Action: Quarantine Host" },
              { num: "02", col: "amber", title: "Incident Response 6-Step Triage", desc: "• <strong>Step 1:</strong> Identify host & quarantine endpoint (disable switch port).<br>• <strong>Step 2:</strong> Theorize unauthorized persistence / reverse shell.<br>• <strong>Step 3:</strong> Inspect processes with <code>netstat -ano | findstr :22</code>.<br>• <strong>Step 4:</strong> Terminate rogue PID, revoke credentials, block C2 IP.<br>• <strong>Step 5:</strong> Full forensic antivirus scan & re-image.<br>• <strong>Step 6:</strong> File Incident Response report & update firewall rules." }
            ],
            notes: "SLIDE 12: Case Study 2 (Cybersecurity Incident). Transition into Ethical Hacking. Explain Port 22 SSH exfiltration. Immediate action: isolate endpoint from switch port before attacker can move laterally."
          },
          {
            badge: "CASE STUDY 3 // LAYER 2 CYBER ATTACK",
            badgeClass: "purple",
            title: "The ARP Spoofing Doppelgänger",
            subtitle: "Symptom: Multiple lab users report browser SSL/TLS certificate warnings & slow speeds",
            layout: "grid-2",
            cards: [
              { num: "01", col: "purple", title: "Inspecting the ARP Table", desc: "You run <code>arp -a</code> on a victim workstation and make an alarming discovery:", cli: "Interface: 192.168.1.105 --- 0x3\n  Internet Address      Physical Address      Type\n  192.168.1.1           b8-27-eb-93-11-aa     dynamic  <-- Default Gateway\n  192.168.1.55          b8-27-eb-93-11-aa     dynamic  <-- Student Laptop!", tag: "Diagnosis: Man-in-the-Middle (MitM) Attack" },
              { num: "02", col: "green", title: "Remediation & Permanent Prevention", desc: "• <strong>Immediate Fix:</strong> Shut down switch port hosting MAC <code>b8-27-eb-93-11-aa</code>.<br>• <strong>Client Remediation:</strong> Flush ARP cache with <code>netsh interface ip delete arpcache</code>.<br>• <strong>Step 5 Prevention (Hardening):</strong> Enable <strong>Dynamic ARP Inspection (DAI)</strong> and <strong>DHCP Snooping</strong> on Cisco switches.<br>• <strong>Step 6 Documentation:</strong> Document rogue MAC and report incident." }
            ],
            notes: "SLIDE 13: Case Study 3 (ARP Poisoning). Look at `arp -a`. Two IPs with the same MAC address means a Man-in-the-Middle attacker! Introduce Dynamic ARP Inspection (DAI) and DHCP Snooping."
          },
          {
            badge: "ENGINEERING STANDARDS",
            badgeClass: "cyan",
            title: "How to Draw an Elite Logic Flowchart",
            subtitle: "Turning your troubleshooting methodology into a bulletproof decision tree",
            layout: "grid-3",
            cards: [
              { num: "01", col: "cyan", title: "Decision Diamonds", desc: "Every test in your flowchart must be a <strong>testable command</strong> with exactly two exit branches: <strong>[PASS → TRUE]</strong> and <strong>[FAIL → FALSE]</strong>.", cli: "[ping 192.168.1.1]\n   /         \\\n [PASS]     [FAIL]" },
              { num: "02", col: "amber", title: "No Ambiguous Steps", desc: "Never write <em>'Check computer'</em> or <em>'Fix internet'</em>. Write the exact CLI command: <code>ipconfig /flushdns</code>, <code>tracert -d 8.8.8.8</code>, or <code>net start spooler</code>.", tag: "Precision Engineering" },
              { num: "03", col: "green", title: "Terminal Endpoints", desc: "Every path must terminate in either:<br><br>• <strong>[RESOLVED & DOCUMENTED]</strong><br>• <strong>[ESCALATE TO TIER 2 / NET ADMIN]</strong>", tag: "Definitive Closure" }
            ],
            notes: "SLIDE 14: Logic Flowcharts. Explain the rubric for today's lab activity. Every diamond must be an exact CLI command, and every branch must lead to pass/fail next steps."
          },
          {
            badge: "MISSION BRIEFING",
            title: "Deploying to the Interactive Lab",
            subtitle: "Ready your terminal. Open your companion activity worksheet.",
            layout: "launch",
            notes: "SLIDE 15: Mission Launch! Instruct students to open `activity.html` and begin Tier 1 through Tier 5 scenarios."
          }
        ]
      },

      ar: {
        brand: "شبكة بيتي // هندسة الشبكات والأمن السيبراني",
        sub: "منهجية حل المشكلات المعتمدة من CompTIA (الخطوات الست)",
        notes: "ملاحظات المعلم [N]",
        fs: "ملء الشاشة [F]",
        act: "تشغيل ورقة عمل النشاط العملي ←",
        prev: "← السابق",
        next: "التالي →",
        notesHeader: "دليل وملاحظات المعلم // إرشادات الأستاذ L",
        hints: { prev: "السابق", next: "التالي", adv: "تقدم", notes: "ملاحظات", fs: "ملء الشاشة" },
        slides: [
          {
            badge: "الدرس // المنهجية الأساسية لـ CompTIA",
            title: "فرّق تسُد: نموذج الخطوات الست لحل الأعطال",
            subtitle: "العزل المنهجي للأعطال، التشخيص بالبحث الثنائي، وفرز المشكلات المؤسسية",
            layout: "grid-2",
            cards: [
              { num: "01", col: "green", title: "توقف عن التخمين. ابدأ بالعزل المنهجي.", desc: "الفنيون المبتدئون يخمنون ويستبدلون الكابلات عشوائياً. مهندسو الشبكات وخبراء الأمن السيبراني المحترفون يستخدمون <strong>نماذج استنتاجية صارمة</strong>. اليوم ستتقن الإطار المعتمد في اختبارات <strong>CompTIA A+ و Network+ و Security+</strong>.", cli: "root@beattie-net:~# ./isolate_fault.sh --target=\"enterprise-network\"\n[+] Establishing baseline telemetry...\n[+] Initializing 6-step diagnostic protocol...", tag: "معتمد لاختبارات CompTIA A+ و Network+" },
              { num: "02", col: "cyan", title: "خوارزمية البحث الثنائي (Binary Search)", desc: "استكشاف الأعطال خطياً عبر طبقات OSI السبع يستغرق وقتاً طويلاً. عبر تطبيق مبدأ <strong>فرّق تسُد في نقطة المنتصف (الطبقة 3/4)</strong>، ستختزل 50% من نطاق المشكلة بأمر سطر أوامر واحد فقط (`ping 127.0.0.1` ثم `ping gateway` ثم `ping 8.8.8.8` ثم `nslookup`).", cli: "كفاءة الخوارزمية:\n7 اختبارات خطية -> 100% من الوقت المستغرق\nفرّق تسُد (3 اختبارات فقط) -> تقليل وقت الحل (MTTR) بنسبة 57%", tag: "تحسين متوسط وقت الإصلاح (MTTR)" }
            ],
            notes: "الشريحة 1: اجذب انتباه الفصل فوراً. اسأل الطلاب: 'عندما تنقطع شبكة الواي فاي في منزلك، ما هو أول شيء تفعله؟' وضح أن فصل الأسلاك عشوائياً دون معرفة الطبقة المتعطلة تصرف غير مهني. عرّفهم على معيار CompTIA العالمي."
          },
          {
            badge: "واقع سوق العمل",
            badgeClass: "amber",
            title: "التكلفة الباهظة للتخمين العشوائي",
            subtitle: "لماذا يعد التشخيص المنهجي إلزامياً في بيئات العمل ومراكز العمليات السيبرانية",
            layout: "grid-3",
            cards: [
              { num: "01", col: "red", title: "الخسائر المالية لانقطاع الخدمة ($$$)", desc: "في مراكز البيانات المؤسسية، يكلف توقف الشبكة في المتوسط <strong>5,600 دولار في الدقيقة الواحدة</strong>. استبدال القطع عشوائياً يطيل فترات الانقطاع ويكلف الملايين.", tag: "مخاطر تشغيلية ومالية جسيمة" },
              { num: "02", col: "amber", title: "الأضرار الجانبية غير المقصودة", desc: "تعديل الإعدادات أو إعادة تشغيل الموجهات الرئيسية (Routers) دون خطة عمل مدروسة يتسبب غالباً في <strong>تعطيل خدمات تابعة أخرى</strong>، مما يحول تذكرة دعم واحدة إلى خمسين تذكرة.", tag: "تشتت الإعدادات وفوضى الشبكة" },
              { num: "03", col: "green", title: "حلول غير قابلة للتكرار أو التوثيق", desc: "إذا قمت بتعديل ستة إعدادات مختلفة في نفس الوقت وعادت الشبكة للعمل، <strong>أي إعداد منها هو الذي أصلح المشكلة؟</strong> لن تعرف ذلك، وعندما تتكرر المشكلة الأسبوع القادم ستبدأ من الصفر.", tag: "المنهجية العلمية والتوثيق" }
            ],
            notes: "الشريحة 2: سياق الأعمال. ركز على تكلفة توقف الأنظمة في المستشفيات ومراكز التداول المالي. اسأل الطلاب عما يحدث إذا قام فني بإعادة تشغيل محول رئيسي أثناء اختبار مدرسي."
          },
          {
            badge: "معيار CompTIA المعتمد",
            badgeClass: "cyan",
            title: "دورة حياة حل المشكلات الكاملة",
            subtitle: "الخطوات المتسلسلة المعتمدة عالمياً للحصول على شهادات CompTIA الاحترافية",
            layout: "grid-6",
            cards: [
              { num: "1", col: "green", title: "1. تحديد المشكلة", desc: "استجواب المستخدم، حصر التغييرات الأخيرة، فحص سجلات النظام (Logs)، وإعادة تمثيل العطل." },
              { num: "2", col: "cyan", title: "2. صياغة فرضية السبب", desc: "افحص الأمور البديهية أولاً. اختر المنهجية (من أعلى لأسفل، من أسفل لأعلى، أو فرّق تسُد)." },
              { num: "3", col: "amber", title: "3. اختبار الفرضية", desc: "نفّذ اختباراً دقيقاً. إذا ثبتت الفرضية تقدم للحل؛ وإذا بطلت صِغ فرضية جديدة أو صعّد المشكلة." },
              { num: "4", col: "purple", title: "4. خطة العمل والتنفيذ", desc: "ضع خطة عمل تفصيلية، حدد الآثار الجانبية المحتملة وخطة التراجع (Rollback)، ثم نفذ الحل بأمان." },
              { num: "5", col: "green", title: "5. التحقق والوقاية", desc: "تحقق من عمل النظام بالكامل مع المستخدم؛ طبّق تدابير وقائية لمنع تكرار المشكلة مستقبلاً." },
              { num: "6", col: "cyan", title: "6. التوثيق الشامل", desc: "سجل الأعراض، والسبب الجذري، والإجراءات المتخذة، والنتائج في نظام التذاكر وقاعدة المعرفة." }
            ],
            notes: "الشريحة 3: اطلب من الفصل ترديد الخطوات الست معاً بصوت عالٍ: تحديد، فرضية، اختبار، خطة وتنفيذ، تحقق ووقاية، توثيق. أكد أن الخطوتين 5 و 6 هما ما يميز المهندس المحترف عن الفني المبتدئ."
          },
          {
            badge: "الخطوة الأولى بالتفصيل",
            title: "الخطوة 1: تحديد المشكلة والتحقق منها",
            subtitle: "جمع البيانات والقياسات الرقمية قبل لمس أي ملف إعداد في النظام",
            layout: "grid-2",
            cards: [
              { num: "01", col: "green", title: "استجواب المستخدم وحصر التغييرات", desc: "المستخدمون نادراً ما يذكرون السبب الجذري؛ بل يصفون الأعراض الظاهرة (مثل: <em>'الخادم مات'</em>). واجبك كفني محترف:<br><br>• <strong>استجواب المستخدم:</strong> متى بدأت المشكلة؟ ماذا كنت تفعل بالتحديد؟<br>• <strong>التغييرات البيئية:</strong> هل تم تثبيت برامج جديدة؟ هل طُبق تحديث للنظام ليلاً؟<br>• <strong>تكرار العطل:</strong> هل يمكنك إعادة تمثيل نفس الخطأ أمامك؟<br>• <strong>تحديد النطاق:</strong> هل المشكلة في جهاز واحد، أم في شبكة VLAN كاملة، أم في المبنى بأكمله؟" },
              { num: "02", col: "cyan", title: "استخراج السجلات والبيانات الرقمية", desc: "افحص دائماً السجلات الرسمية للنظام قبل بناء أي فرضية:", cli: "# أوامر الفحص في Windows PowerShell:\nGet-EventLog -LogName System -Newest 10 -EntryType Error\nipconfig /all\nTest-NetConnection -ComputerName 10.0.0.1 -Port 443\n\n# الفحص والتحقيق الجنائي في أنظمة Linux:\njournalctl -xe -u networking.service\ndmesg | grep -E \"eth|wlan|link\"" }
            ],
            notes: "الشريحة 4: علم الطلاب كيفية طرح الأسئلة المفتوحة والمغلقة. اسأل: 'ما خطورة تصديق تشخيص المستخدم عندما يقول إن الخادم معطل تماماً؟' يجب دائماً التحقق من السجلات أولاً."
          },
          {
            badge: "الخطوتان 2 و 3 بالتفصيل",
            badgeClass: "cyan",
            title: "الخطوتان 2 و 3: بناء الفرضيات واختبارها",
            subtitle: "توليد الفرضيات والتحقق العلمي السريع بالاستبعاد (Falsification)",
            layout: "grid-2",
            cards: [
              { num: "02", col: "cyan", title: "صياغة فرضية السبب المحتمل", desc: "<strong>افحص الأمور البديهية:</strong> هل كابل الشبكة مفصول؟ هل زر Caps Lock مفعل؟ هل انتهت صلاحية عنوان الـ DHCP؟<br><br>رتب الفرضيات حسب الأرجحية. اختبر دائماً الفرضية الأسهل والأكثر احتمالاً أولاً.", cli: "الفرضية أ (الأعلى احتمالاً): مهلة خادم الـ DNS المحلي انتهت\nالفرضية ب (احتمال متوسط): البوابة الافتراضية فقدت جدول ARP\nالفرضية ج (احتمال ضعيف): انقطاع كابل الألياف الضوئية للمزود في المدينة" },
              { num: "03", col: "amber", title: "اختبار الفرضية للتحقق منها", desc: "نفذ اختبارات محددة ومعزولة تنتج نتيجة ثنائية واضحة: <strong>تم التأكيد (PASS)</strong> أو <strong>تم الاستبعاد (FAIL)</strong>.<br><br><strong>قاعدة ذهبية:</strong> إذا أثبت الاختبار بطلان الفرضية، لا تقم بأي تعديل! صِغ فرضية جديدة أو صعّد البلاغ.", cli: "C:\\> ping 8.8.8.8  -> Reply from 8.8.8.8 (نجاح!)\nC:\\> nslookup google.com -> DNS request timed out (فشل!)\n[+] تم تأكيد الفرضية: توجيه الـ IP سليم؛ بينما خادم الـ DNS معطل." }
            ],
            notes: "الشريحة 5: الاستبعاد العلمي! وضح للطلاب أن فشل الفرضية هو خبر ممتاز لأنه يستبعد مساراً خاطئاً بالكامل. أكد بشدة: لا تقم بأي إصلاح في الخطوة 3؛ الخطوة 3 مخصصة للاختبار فقط!"
          },
          {
            badge: "الخطوة الرابعة بالتفصيل",
            badgeClass: "purple",
            title: "الخطوة 4: وضع خطة العمل والتنفيذ الآمن",
            subtitle: "التنفيذ المنظم مع إدارة التغيير، تقليل المخاطر، وخطة التراجع الفوري",
            layout: "grid-2",
            cards: [
              { num: "01", col: "purple", title: "عناصر خطة العمل المحترفة", desc: "إياك وتطبيق الحلول بعشوائية. تتكون خطة العمل الاحترافية من ثلاثة ركائز أساسية:<br><br>• <strong>خطوات الإصلاح التفصيلية:</strong> الأوامر الدقيقة، ونصوص الإعدادات، والملفات المستهدفة.<br>• <strong>حصر الآثار الجانبية:</strong> هل ستؤدي إعادة تشغيل هذا المنفذ إلى قطع مكالمات الهاتف (VoIP) النشطة في الغرفة 204؟<br>• <strong>بروتوكول التراجع (Rollback):</strong> إذا تسبب التحديث في عطل أكبر، كيف تعيد النظام لحالته السابقة خلال 5 دقائق؟" },
              { num: "02", col: "cyan", title: "نوافذ الصيانة وإذن التعديل", desc: "احصل دائماً على الإذن الرسمي (فريق إدارة التغيير / كبير مهندسي الأنظمة) قبل تعديل البنية التحتية للمؤسسة.", cli: "تذكرة تغيير البنية المؤسسية #8849\nالنطاق: تحديث عنوان IP Helper لشبكة VLAN 20 على المحول الرئيسي\nنافذة الصيانة: 05:00 - 05:15 صباحاً (تأثير منخفض)\nتحليل التأثير: 45 محطة عمل ستجدد عناوين الـ DHCP الخاصة بها\nخطة التراجع: استعادة ملف الإعدادات السابق عبر TFTP /backup/sw01_prev.cfg" }
            ],
            notes: "الشريحة 6: ناقش مع الطلاب مفهوم إدارة التغيير ونوافذ الصيانة وأهمية أخذ لقطات للنظام (Snapshots) قبل التحديث."
          },
          {
            badge: "الخطوتان 5 و 6 بالتفصيل",
            title: "الخطوتان 5 و 6: التحقق والتوثيق المؤسسي",
            subtitle: "إغلاق حلقة الدعم، التحصين الوقائي، وبناء الذاكرة المعرفية للمؤسسة",
            layout: "grid-2",
            cards: [
              { num: "05", col: "green", title: "5. التحقق من النظام والتدابير الوقائية", desc: "<strong>1. التحقق الشامل:</strong> لا تكتفِ بفحص شاشة الأوامر الخاصة بك؛ اطلب من المستخدم إنجاز مهام عمله الفعلية أمامك.<br><br><strong>2. التحصين الوقائي:</strong> لماذا حدث العطل؟ إذا تضرر كابل بسبب الدوس عليه، ركّب مسارات أرضية واقية. وإذا حدث تعارض في العناوين، فعّل خاصية DHCP Snooping." },
              { num: "06", col: "cyan", title: "6. توثيق النتائج والإجراءات في التذكرة", desc: "إذا لم توثق ما قمت به، فالخلل يعتبر كأنه لم يُحل قط. التنسيق القياسي لتوثيق التذاكر:", cli: "تقرير إغلاق تذكرة الدعم الفني\nالعَرَض: محطة العمل 12 تظهر عنوان 169.254.x.x (APIPA)\nالسبب الجذري: نفاد نطاق الـ DHCP 192.168.10.0/24 بنسبة 100%\nالإصلاح المنفذ: توسيع قناع الشبكة إلى /23 وتقليص مدة التأجير إلى 4 ساعات\nالتحقق: حصل الجهاز على 192.168.10.142 وتم الاتصال بالبوابة بنجاح\nالإجراء الوقائي: تفعيل تنبيه تلقائي عند وصول سعة الـ DHCP إلى 80%" }
            ],
            notes: "الشريحة 7: التحقق يجب أن يشمل المستخدم نفسه. ثم اشرح أهمية الصيانة الوقائية والتوثيق القياسي في قواعد المعرفة (KB)."
          },
          {
            badge: "الاستراتيجية الأساسية",
            badgeClass: "cyan",
            title: "البحث الثنائي: منهجية 'فرّق تسُد'",
            subtitle: "اختصار وقت التشخيص للنصف عبر فحص نقطة المنتصف في طبقات OSI السبع",
            layout: "grid-2",
            cards: [
              { num: "01", col: "red", title: "الطريقة البطيئة: الفحص الخطي المتسلسل (7 خطوات)", desc: "فحص الطبقة 1 (الكابل) ← الطبقة 2 (عنوان MAC للمحول) ← الطبقة 3 (عنوان IP البوابة) ← الطبقة 4 (المنفذ) ← الطبقة 5 ← الطبقة 6 ← الطبقة 7 (التطبيق).", cli: "إجمالي الفحوصات المتسلسلة: 7 اختبارات\nالوقت المستغرق: 100%\nمستوى الإحباط: مرتفع جداً" },
              { num: "02", col: "green", title: "طريقة المحترفين: البحث الثنائي عند نقطة المنتصف (3 خطوات)", desc: "ابدأ الفحص مباشرة عند <strong>الطبقة 3 (طبقة الشبكة)</strong>.<br><br>• <strong>إذا نجحت الطبقة 3 (PASS):</strong> فهذا يثبت 100% أن الطبقات 1 و 2 و 3 سليمة تماماً! إياك ولمس الكابل أو منفذ المحول، وانتقل فوراً للطبقات 4 إلى 7.<br><br>• <strong>إذا فشلت الطبقة 3 (FAIL):</strong> المشكلة حتماً في الطبقات 1 إلى 3. لا تضيع وقتك في فحص المتصفح أو جدار الحماية." }
            ],
            notes: "الشريحة 8: ارسم شجرة البحث الثنائي على السبورة. وضح كيف أن فحص الطبقة 3 يقسم مجال البحث إلى نصفين فوراً."
          },
          {
            badge: "سلّم التشخيص الخماسي",
            badgeClass: "amber",
            title: "التسلسل التشخيصي الذهبي للمحترفين",
            subtitle: "احفظ هذه الأوامر الخمسة المتسلسلة لتشخيص أي عطل في شبكات المؤسسات",
            layout: "ladder",
            steps: [
              { num: "1", cmd: "ping 127.0.0.1", title: "اختبار مكدس TCP/IP المحلي (Loopback)", desc: "يتحقق من سلامة تعريف بطاقة الشبكة ومكدس بروتوكولات نظام التشغيل" },
              { num: "2", cmd: "ping 192.168.1.1", title: "اختبار البوابة الافتراضية (مخرج الشبكة المحلية)", desc: "يتحقق من الكابل، مقبس الجدار، منفذ المحول، وواجهة الموجه (الطبقات 1-3)" },
              { num: "3", cmd: "ping 8.8.8.8", title: "اختبار عنوان IP خارجي عام (الإنترنت WAN)", desc: "يتحقق من مودم المزود، ترجمة العناوين NAT، والتوجيه عبر الإنترنت" },
              { num: "4", cmd: "nslookup google.com", title: "اختبار دقة وخادم الـ DNS (الطبقة 7)", desc: "يتحقق من عمل خادم الـ DNS على المنفذ 53 وترجمة أسماء النطاقات" },
              { num: "5", cmd: "Test-NetConnection -Port 443", title: "اختبار منفذ الخدمة والتطبيق", desc: "يتحقق من تشغيل خادم الويب، ومصافحة TLS، وجدار الحماية" }
            ],
            notes: "الشريحة 9: التسلسل الذهبي الخماسي! 1. 127.0.0.1 (البطاقة). 2. البوابة (الشبكة المحلية). 3. 8.8.8.8 (الإنترنت). 4. google.com (DNS). 5. المنفذ 443 (التطبيق). اطلب من الطلاب تدوينها في دفاترهم."
          },
          {
            badge: "عرض عملي تفاعلي",
            badgeClass: "cyan",
            title: "المختبر التجريبي التفاعلي لنقطة المنتصف",
            subtitle: "اضغط على أوامر التشخيص أدناه لتشاهد كيف ينقسم نطاق البحث لحظياً",
            layout: "sim",
            notes: "الشريحة 10: المحاكي التفاعلي. قم باستعراض النقر المباشر أمام الطلاب على جهاز العرض."
          },
          {
            badge: "دراسة حالة 1 // المستوى الأول",
            badgeClass: "amber",
            title: "أزمة عنوان APIPA (169.254.x.x)",
            subtitle: "العَرَض: 8 محطات عمل في المعمل تظهر فجأة 'لا يوجد اتصال بالإنترنت'",
            layout: "grid-2",
            cards: [
              { num: "01", col: "amber", title: "سيناريو الحادثة الفنية", desc: "قام الطلاب بتشغيل الحواسيب في القاعة 104. أضواء بطاقات الشبكة خضراء وثابتة، لكن تشغيل أمر <code>ipconfig</code> أظهر التالي:", cli: "IPv4 Address. . . . . . . . . . . : 169.254.144.82\nSubnet Mask . . . . . . . . . . . : 255.255.0.0\nDefault Gateway . . . . . . . . . : [فارغ تماماً]", tag: "عنونة IP التلقائية الخاصة (APIPA / RFC 3927)" },
              { num: "02", col: "green", title: "خطوات المعالجة بمبدأ فرّق تسُد", desc: "• <strong>الخطوة 1:</strong> الأضواء تعمل ← الطبقتان 1 و 2 سليمتان تماماً.<br>• <strong>الخطوة 2:</strong> الفرضية ← توقف خدمة خادم الـ DHCP أو نفاد العناوين.<br>• <strong>الخطوة 3:</strong> الاختبار ← فحص حالة خدمة الـ DHCP على الخادم.<br>• <strong>الخطوة 4:</strong> الحل ← إعادة تشغيل الخدمة وتوسيع نطاق العناوين.<br>• <strong>الخطوة 5:</strong> التحقق ← تنفيذ <code>ipconfig /renew</code> على الأجهزة واستلام عنوان <code>192.168.10.45</code>.<br>• <strong>الخطوة 6:</strong> التوثيق ← تسجيل توسيع النطاق في نظام التذاكر." }
            ],
            notes: "الشريحة 11: دراسة حالة APIPA. وضح للطلاب سبب ظهور 169.254.0.0/16 وأن أضواء البطاقة الخضراء تعني سلامة الطبقة 1 و 2 فقط."
          },
          {
            badge: "دراسة حالة 2 // حادثة سيبرانية",
            badgeClass: "red",
            title: "تسريب بيانات مشبوه عبر المنفذ 22 (SSH)",
            subtitle: "العَرَض: نظام كشف التسلل (IDS) يطلق تنبيهاً عالي الخطورة لحركة بيانات صادرة ضخمة",
            layout: "grid-2",
            cards: [
              { num: "01", col: "red", title: "الحادثة الأمنية", desc: "أطلق نظام كشف التسلل (IDS) تنبيهاً حرجاً: <strong>محطة العمل 04 (192.168.10.84)</strong> ترسل 2.4 جيجابايت من البيانات المشفرة إلى خادم روسي مشبوه عبر المنفذ 22 (SSH).", cli: "ALERT: [1:2010935:2] ET EXPLOIT Outbound SSH Connection to Threat Intel C2 IP 185.220.101.5\nSrc: 192.168.10.84:54210 -> Dst: 185.220.101.5:22", tag: "الإجراء الأمني الفوري: عزل الجهاز المصاب" },
              { num: "02", col: "amber", title: "الاستجابة للحادثة وفق الخطوات الست", desc: "• <strong>الخطوة 1:</strong> عزل الجهاز فوراً عبر تعطيل منفذ المحول.<br>• <strong>الخطوة 2:</strong> فرضية وجود نفق SSH عكسي وبرمجية خبيثة.<br>• <strong>الخطوة 3:</strong> فحص العمليات بأمر <code>netstat -ano | findstr :22</code>.<br>• <strong>الخطوة 4:</strong> إنهاء العملية الخبيثة وحظر عنوان الخادم الخارجي في جدار الحماية.<br>• <strong>الخطوة 5:</strong> فحص جنائي شامل وإعادة تثبيت النظام من النسخة المعتمدة.<br>• <strong>الخطوة 6:</strong> كتابة تقرير الاستجابة للحوادث وتحديث قواعد جدار الحماية." }
            ],
            notes: "الشريحة 12: دراسة حالة أمن سيبراني. وضح للطلاب أهمية العزل الفوري للجهاز المصاب لمنع المهاجم من التحرك أفقياً في الشبكة."
          },
          {
            badge: "دراسة حالة 3 // هجوم على الطبقة الثانية",
            badgeClass: "purple",
            title: "هجوم انتحال ARP (القرين / Doppelgänger)",
            subtitle: "العَرَض: المستخدمون يواجهون تحذيرات أمنية في المتصفح وتراجعاً شديداً في سرعة الشبكة",
            layout: "grid-2",
            cards: [
              { num: "01", col: "purple", title: "فحص جدول مطابقة العناوين (ARP)", desc: "قمت بتشغيل أمر <code>arp -a</code> على أحد الأجهزة المصابة واكتشفت ما يلي:", cli: "Interface: 192.168.1.105 --- 0x3\n  Internet Address      Physical Address      Type\n  192.168.1.1           b8-27-eb-93-11-aa     dynamic  <-- البوابة الافتراضية\n  192.168.1.55          b8-27-eb-93-11-aa     dynamic  <-- حاسوب طالب!", tag: "التشخيص: هجوم الوسيط (Man-in-the-Middle)" },
              { num: "02", col: "green", title: "الإصلاح والتحصين الدائم", desc: "• <strong>الحل الفوري:</strong> إيقاف منفذ المحول المرتبط بالماك <code>b8-27-eb-93-11-aa</code>.<br>• <strong>تنظيف الأجهزة:</strong> مسح ذاكرة ARP بأمر <code>netsh interface ip delete arpcache</code>.<br>• <strong>الخطوة 5 الوقاية (التحصين):</strong> تفعيل ميزتي <strong>Dynamic ARP Inspection (DAI)</strong> و <strong>DHCP Snooping</strong> على محولات سيسكو.<br>• <strong>الخطوة 6 التوثيق:</strong> تسجيل عنوان MAC المهاجم وإبلاغ الإدارة." }
            ],
            notes: "الشريحة 13: هجوم تسميم ARP. عندما يشترك عنوانان في نفس الماك أدرس، فهذا يعني وجود مهاجم وسيط في الشبكة! اشرح ميزة DAI."
          },
          {
            badge: "معايير الهندسة ورسم المخططات",
            badgeClass: "cyan",
            title: "كيف ترسم مخطط تدفق منطقي احترافي",
            subtitle: "تحويل منهجيتك في التفكير إلى شجرة قرارات برمجية دقيقة لا تقبل اللبس",
            layout: "grid-3",
            cards: [
              { num: "01", col: "cyan", title: "معينات اتخاذ القرار (Diamonds)", desc: "كل اختبار في المخطط يجب أن يكون <strong>أمراً قابلاً للتنفيذ الفعلي</strong> وله مخرجان محددان فقط: <strong>[نجاح ← نعم]</strong> و <strong>[فشل ← لا]</strong>.", cli: "[ping 192.168.1.1]\n   /         \\\n [نجاح]     [فشل]" },
              { num: "02", col: "amber", title: "تجنب العبارات الغامضة", desc: "لا تكتب أبداً عبارات مثل <em>'افحص الحاسوب'</em> أو <em>'أصلح الشبكة'</em>. اكتب الأمر الدقيق: <code>ipconfig /flushdns</code> أو <code>tracert -d 8.8.8.8</code>.", tag: "الدقة الهندسية والاحترافية" },
              { num: "03", col: "green", title: "نقاط النهاية الحاسمة", desc: "يجب أن ينتهي كل مسار بأحد خيارين واضحين:<br><br>• <strong>[تم الحل وتوثيق التذكرة]</strong><br>• <strong>[تصعيد البلاغ للمستوى 2 / مهندس الشبكات]</strong>", tag: "الحسم والإغلاق المنظم" }
            ],
            notes: "الشريحة 14: وضح للطلاب معايير تقييم ورقة النشاط اليوم: الدقة، عدم الغموض، وتحديد مسارات واضحة لكل قرار."
          },
          {
            badge: "توجيهات المهمة",
            title: "الانطلاق إلى ورقة النشاط العملي",
            subtitle: "جهّز الطرفية الخاصة بك وافتح ورقة عمل المختبر المرافقة.",
            layout: "launch",
            notes: "الشريحة 15: اطلب من الطلاب فتح activity.html وبدء العمل على المستويات الخمسة."
          }
        ]
      },

      uk: {
        brand: "МЕРЕЖА БІТТІ // КІБЕРБЕЗПЕКА ТА МЕРЕЖЕВА ІНЖЕНЕРІЯ",
        sub: "6-ЕТАПНА МОДЕЛЬ УСУНЕННЯ НЕСПРАВНОСТЕЙ COMPTIA",
        notes: "Нотатки викладача [N]",
        fs: "На весь екран [F]",
        act: "Запустити практичну роботу →",
        prev: "← НАЗАД",
        next: "ДАЛІ →",
        notesHeader: "НОТАТКИ ДЛЯ ВИКЛАДАЧА // МЕТОДИЧНІ ВКАЗІВКИ",
        hints: { prev: "Назад", next: "Далі", adv: "Вперед", notes: "Нотатки", fs: "На весь екран" },
        slides: [
          {
            badge: "УРОК // БАЗОВА МЕТОДОЛОГІЯ COMPTIA",
            title: "Розділяй і володарюй: 6-етапна модель",
            subtitle: "Систематична ізоляція збоїв, бінарний пошук та корпоративна діагностика",
            layout: "grid-2",
            cards: [
              { num: "01", col: "green", title: "Годі вгадувати. Почніть ізолювати збої.", desc: "Початківці вгадують і навмання міняють кабелі. Корпоративні мережеві інженери та етичні хакери використовують <strong>суворі дедуктивні моделі</strong>. Сьогодні ви опануєте офіційну 6-етапну модель <strong>CompTIA A+, Network+ та Security+</strong>.", cli: "root@beattie-net:~# ./isolate_fault.sh --target=\"enterprise-network\"\n[+] Establishing baseline telemetry...\n[+] Initializing 6-step diagnostic protocol...", tag: "Стандарт CompTIA A+ (220-1101/1102) та Network+" },
              { num: "02", col: "cyan", title: "Алгоритм бінарного пошуку (Divide & Conquer)", desc: "Лінійний пошук через усі 7 рівнів OSI займає багато часу. Застосовуючи <strong>бінарний поділ на середньому рівні OSI (L3/L4)</strong>, ви відсікаєте 50% проблеми однією командою (`ping 127.0.0.1` → `ping gateway` → `ping 8.8.8.8` → `nslookup`).", cli: "Ефективність алгоритму:\n7 послідовних тестів -> 100% часу\nБінарний пошук (3 тести) -> на 57% швидший час вирішення (MTTR)", tag: "Оптимізація середнього часу відновлення (MTTR)" }
            ],
            notes: "СЛАЙД 1: Зацікавте клас. Запитайте: 'Що ви робите вдома, коли зникає інтернет?' Поясніть, що хаотичне смикання дротів — це непрофесійно. Представте 6 кроків CompTIA."
          },
          {
            badge: "РЕАЛЬНІСТЬ КОРПОРАТИВНИХ МЕРЕЖ",
            badgeClass: "amber",
            title: "Висока ціна хаотичного вгадування",
            subtitle: "Чому систематичний підхід є обов'язковим у корпоративній сфері та кібербезпеці",
            layout: "grid-3",
            cards: [
              { num: "01", col: "red", title: "Фінансові збитки від простою ($$$)", desc: "У корпоративних дата-центрах хвилина простою мережі коштує в середньому <strong>$5,600</strong>. Хаотична заміна компонентів без перевірки гіпотези затягує відновлення на години.", tag: "Фінансові та операційні ризики" },
              { num: "02", col: "amber", title: "Супутні пошкодження систем", desc: "Зміна налаштувань, перезавантаження магістральних маршрутизаторів без плану часто порушує роботу <strong>пов'язаних сервісів</strong>, перетворюючи одну заявку на десятки.", tag: "Конфігураційний хаос" },
              { num: "03", col: "green", title: "Неповторюваність результату", desc: "Якщо ви одночасно змінили 6 налаштувань і зв'язок з'явився, <strong>яка дія спрацювала?</strong> Ви не знаєте, і при повторенні збою доведеться починати все спочатку.", tag: "Наукова методологія" }
            ],
            notes: "СЛАЙД 2: Бізнес-контекст. Наголосіть на ціні простою в лікарнях чи банках. Що станеться, якщо перезавантажити комутатор під час шкільного тестування?"
          },
          {
            badge: "СТАНДАРТ COMPTIA",
            badgeClass: "cyan",
            title: "Повний життєвий цикл діагностики",
            subtitle: "Загальноприйнята послідовна методологія, необхідна для сертифікації CompTIA",
            layout: "grid-6",
            cards: [
              { num: "1", col: "green", title: "1. Ідентифікація проблеми", desc: "Опитування користувача, виявлення змін, аналіз системних логів, відтворення симптому." },
              { num: "2", col: "cyan", title: "2. Складання теорії причини", desc: "Перевірка очевидного. Формулювання гіпотези (згори вниз, знизу вгору, або поділ навпіл)." },
              { num: "3", col: "amber", title: "3. Тестування теорії", desc: "Цільовий тест. Якщо підтверджено — перехід до плану; якщо спростовано — нова теорія або ескалація." },
              { num: "4", col: "purple", title: "4. План дій та впровадження", desc: "Складання плану дій, оцінка побічних наслідків, план відкату (Rollback) та безпечне впровадження." },
              { num: "5", col: "green", title: "5. Перевірка та запобігання", desc: "Перевірка працездатності разом із користувачем; впровадження превентивних заходів." },
              { num: "6", col: "cyan", title: "6. Повне документування", desc: "Фіксація симптомів, першопричини, виконаних дій та результату в тікет-системі та базі знань." }
            ],
            notes: "СЛАЙД 3: Повторіть усі 6 кроків уголос: Ідентифікація, Теорія, Тест, План/Впровадження, Перевірка/Запобігання, Документування. Кроки 5 і 6 відрізняють профі від аматора."
          },
          {
            badge: "ЕТАП 1 ДЕТАЛЬНО",
            title: "Етап 1: Ідентифікація проблеми",
            subtitle: "Збір телеметрії та фактів перед зміною будь-якої конфігурації",
            layout: "grid-2",
            cards: [
              { num: "01", col: "green", title: "Опитування та фіксація змін", desc: "Користувачі рідко повідомляють технічну причину; вони кажуть про симптоми (наприклад: <em>'Сервер упав'</em>). Ваша задача:<br><br>• <strong>Опитування:</strong> Коли це почалося? Що ви робили в цей момент?<br>• <strong>Зміни середовища:</strong> Чи встановлювали нове ПЗ? Чи були нічні оновлення ОС?<br>• <strong>Відтворення:</strong> Чи можете ви повторити цей збій прямо зараз?<br>• <strong>Визначення масштабу:</strong> Проблема в одного ПК, у всього VLAN, чи в усій будівлі?" },
              { num: "02", col: "cyan", title: "Збір системних логів та телеметрії", desc: "Завжди аналізуйте логи перед тим, як будувати теорії:", cli: "# Діагностичні команди Windows PowerShell:\nGet-EventLog -LogName System -Newest 10 -EntryType Error\nipconfig /all\nTest-NetConnection -ComputerName 10.0.0.1 -Port 443\n\n# Форензика та аналіз логів Linux:\njournalctl -xe -u networking.service\ndmesg | grep -E \"eth|wlan|link\"" }
            ],
            notes: "СЛАЙД 4: Навчіть ставити відкриті запитання. Чому не можна сліпо довіряти користувачу, коли він каже, що зламався весь сервер? Перевіряйте логи."
          },
          {
            badge: "ЕТАПИ 2 ТА 3 ДЕТАЛЬНО",
            badgeClass: "cyan",
            title: "Етапи 2 і 3: Гіпотези та верифікація",
            subtitle: "Формулювання теорій та їх швидке спростування (Falsification)",
            layout: "grid-2",
            cards: [
              { num: "02", col: "cyan", title: "Складання теорії ймовірної причини", desc: "<strong>Перевірте очевидне:</strong> Чи підключений патч-корд? Чи не увімкнено Caps Lock? Чи не закінчилася оренда DHCP?<br><br>Ранжуйте теорії за ймовірністю. Завжди спочатку перевіряйте найпростішу та найвірогіднішу гіпотезу.", cli: "Теорія А (Найвища ймов.): Тайм-аут локального DNS-резолвера\nТеорія Б (Середня ймов.): Шлюз скинув таблицю ARP\nТеорія В (Низька ймов.): Обрив оптоволокна провайдера" },
              { num: "03", col: "amber", title: "Тестування теорії (Верифікація)", desc: "Виконуйте ізольовані тести з чітким бінарним результатом: <strong>ПІДТВЕРДЖЕНО (PASS)</strong> або <strong>СПРОСТОВАНО (FAIL)</strong>.<br><br><strong>Правило:</strong> Якщо тест спростував теорію, нічого не ремонтуйте! Сформулюйте нову гіпотезу або ескалюйте заявку.", cli: "C:\\> ping 8.8.8.8  -> Відповідь від 8.8.8.8 (PASS!)\nC:\\> nslookup google.com -> DNS request timed out (FAIL!)\n[+] ТЕОРІЮ ПІДТВЕРДЖЕНО: IP-маршрутизація працює; DNS не відповідає." }
            ],
            notes: "СЛАЙД 5: Принцип спростування. Невдалий тест — це чудовий результат, бо він виключає хибний шлях. Наголосіть: на Етапі 3 ми ТІЛЬКИ тестуємо, а не ремонтуємо!"
          },
          {
            badge: "ЕТАП 4 ДЕТАЛЬНО",
            badgeClass: "purple",
            title: "Етап 4: План дій та безпечне впровадження",
            subtitle: "Управління змінами, мінімізація ризиків та процедура відкату (Rollback)",
            layout: "grid-2",
            cards: [
              { num: "01", col: "purple", title: "Складання плану дій", desc: "Ніколи не застосовуйте виправлення наосліп. Професійний план містить три елементи:<br><br>• <strong>Покрокові дії:</strong> Точні команди, синтаксис конфігурації та файли.<br>• <strong>Побічні ефекти:</strong> Чи не перерве перезавантаження порту активні дзвінки IP-телефонії в каб. 204?<br>• <strong>План відкату:</strong> Якщо оновлення пошкодить базу даних, як повернути попередній стан за 5 хвилин?" },
              { num: "02", col: "cyan", title: "Вікна обслуговування та авторизація", desc: "Завжди отримуйте дозвіл (Change Advisory Board / Головний адмін) перед зміною конфігурації корпоративної мережі.", cli: "ЗАЯВКА НА ЗМІНУ #8849\nОбласть: Оновлення IP Helper для VLAN 20 на магістральному комутаторі\nВікно робіт: 05:00 - 05:15 EST (Мінімальний вплив)\nАналіз: 45 робочих станцій оновлять оренду DHCP\nПлан відкату: Відновлення running-config з TFTP /backup/sw01_prev.cfg" }
            ],
            notes: "СЛАЙД 6: Розповісти про Change Management, вікна регламентних робіт та резервні копії перед змінами."
          },
          {
            badge: "ЕТАПИ 5 ТА 6 ДЕТАЛЬНО",
            title: "Етапи 5 і 6: Перевірка та документування",
            subtitle: "Закриття циклу, превентивні заходи та збереження корпоративного досвіду",
            layout: "grid-2",
            cards: [
              { num: "05", col: "green", title: "5. Повна перевірка та запобігання збоям", desc: "<strong>1. Комплексна перевірка:</strong> Не обмежуйтесь консоллю; попросіть користувача виконати його реальну робочу задачу у вашій присутності.<br><br><strong>2. Превентивні заходи:</strong> Чому це сталося? Якщо кабель перетерся, встановіть кабель-канал. Якщо був конфлікт IP, увімкніть DHCP Snooping." },
              { num: "06", col: "cyan", title: "6. Документування у базі знань", desc: "Якщо дія не задокументована — проблема не вирішена. Стандартний звіт за заявкою:", cli: "ЗВІТ ПРО ВИРІШЕННЯ ІНЦИДЕНТУ\nСимптом: ПК 12 показує адресу 169.254.x.x (APIPA)\nПершопричина: Пул DHCP 192.168.10.0/24 вичерпано на 100%\nВиконані дії: Розширено маску підмережі до /23, оренду скорочено до 4 год\nПеревірка: ПК отримав адресу 192.168.10.142; пінг до шлюзу успішний\nПревентивна дія: Налаштовано алерт при заповненні пулу DHCP на 80%" }
            ],
            notes: "СЛАЙД 7: Перевірка повинна виконуватись разом з користувачем. Розкажіть про превентивні заходи та ведення бази знань (KB)."
          },
          {
            badge: "ОСНОВНА СТРАТЕГІЯ",
            badgeClass: "cyan",
            title: "Бінарний пошук 'Розділяй і володарюй'",
            subtitle: "Скорочення часу діагностики вдвічі через тест середньої точки моделі OSI",
            layout: "grid-2",
            cards: [
              { num: "01", col: "red", title: "Повільний шлях: Послідовний прохід OSI (7 кроків)", desc: "Тест Рівня 1 (Кабель) → Рівня 2 (MAC комутатора) → Рівня 3 (IP шлюзу) → Рівня 4 (TCP-порт) → Рівня 5 → Рівня 6 → Рівня 7 (Додаток).", cli: "Всього послідовних тестів: 7\nВитрачений час: 100%\nРівень фрустрації: ВИСОКИЙ" },
              { num: "02", col: "green", title: "Шлях профі: Бінарний поділ навпіл (3 кроки)", desc: "Тестуйте безпосередньо <strong>Рівень 3 (Мережевий рівень)</strong>.<br><br>• <strong>Якщо Рівень 3 ПРАЦЮЄ (PASS):</strong> Рівні 1, 2 і 3 гарантовано справні! Не чіпайте кабель і порт. Одразу переходьте до рівнів 4–7.<br><br>• <strong>Якщо Рівень 3 НЕ ПРАЦЮЄ (FAIL):</strong> Проблема точно на рівнях 1–3. Не гайте час на перевірку браузера чи сертифікатів." }
            ],
            notes: "СЛАЙД 8: Намалюйте дерево бінарного пошуку. Поясніть, що перевірка рівня L3 одразу відсікає половину стеку."
          },
          {
            badge: "5 КРОКІВ ДІАГНОСТИКИ",
            badgeClass: "amber",
            title: "Золота послідовність діагностики мережі",
            subtitle: "Запам'ятайте ці 5 послідовних команд для розв'язання будь-якої мережевої проблеми",
            layout: "ladder",
            steps: [
              { num: "1", cmd: "ping 127.0.0.1", title: "Тест локального стеку TCP/IP", desc: "Перевіряє драйвер мережевої карти та стек протоколів ОС" },
              { num: "2", cmd: "ping 192.168.1.1", title: "Тест локального шлюзу (вихід з LAN)", desc: "Перевіряє патч-корд, розетку, порт комутатора та інтерфейс роутера (L1-L3)" },
              { num: "3", cmd: "ping 8.8.8.8", title: "Тест зовнішньої публічної IP-адреси (WAN)", desc: "Перевіряє модем провайдера, NAT-маршрутизацію та інтернет-канал" },
              { num: "4", cmd: "nslookup google.com", title: "Тест розпізнавання DNS (Рівень 7)", desc: "Перевіряє DNS-сервер на порті 53, кеш та резолвінг доменних імен" },
              { num: "5", cmd: "Test-NetConnection -Port 443", title: "Тест порту додатка та сервісу", desc: "Перевіряє веб-сервер, сертифікат TLS та правила брандмауера" }
            ],
            notes: "СЛАЙД 9: Золотий алгоритм. 1. 127.0.0.1 (NIC). 2. Шлюз (LAN). 3. 8.8.8.8 (WAN). 4. google.com (DNS). 5. Порт 443 (App). Учні мають записати це в конспект."
          },
          {
            badge: "ІНТЕРАКТИВНИЙ ДЕМО-СТЕНД",
            badgeClass: "cyan",
            title: "Інтерактивний симулятор бінарного пошуку",
            subtitle: "Натискайте діагностичні команди нижче, щоб побачити поділ простору збою",
            layout: "sim",
            notes: "СЛАЙД 10: Інтерактивний стенд. Продемонструйте на проєкторі логіку відсікання помилок."
          },
          {
            badge: "ПРАКТИЧНИЙ КЕЙС 1 // TIER 1",
            badgeClass: "amber",
            title: "Збій APIPA (Адреса 169.254.x.x)",
            subtitle: "Симптом: 8 ПК у комп'ютерному класі раптово втратили доступ до мережі",
            layout: "grid-2",
            cards: [
              { num: "01", col: "amber", title: "Опис інциденту", desc: "Студенти увімкнули комп'ютери в каб. 104. Індикатори лінку світяться зеленим, але команда <code>ipconfig</code> видає:", cli: "IPv4 Address. . . . . . . . . . . : 169.254.144.82\nSubnet Mask . . . . . . . . . . . : 255.255.0.0\nDefault Gateway . . . . . . . . . : [ПОРОЖНЬО]", tag: "Автоматична приватна IP-адресація (APIPA / RFC 3927)" },
              { num: "02", col: "green", title: "Алгоритм вирішення 'Розділяй і володарюй'", desc: "• <strong>Крок 1:</strong> Лінки горять → Фізичні рівні 1 і 2 в нормі.<br>• <strong>Крок 2:</strong> Теорія → Служба DHCP впала або закінчився пул адрес.<br>• <strong>Крок 3:</strong> Тест → Перевірка служби DHCP на сервері.<br>• <strong>Крок 4:</strong> Дія → Перезапуск служби та розширення пулу.<br>• <strong>Крок 5:</strong> Перевірка → Виконання <code>ipconfig /renew</code> на ПК, отримано <code>192.168.10.45</code>.<br>• <strong>Крок 6:</strong> Документування → Фіксація розширення пулу DHCP у тікеті." }
            ],
            notes: "СЛАЙД 11: Кейс APIPA. Поясніть діапазон 169.254.0.0/16. Індикатори лінку активні, бо фізичний рівень працює, а збій на рівні сервісу DHCP."
          },
          {
            badge: "ПРАКТИЧНИЙ КЕЙС 2 // ІНЦИДЕНТ КІБЕРБЕЗПЕКИ",
            badgeClass: "red",
            title: "Підозріла ексфільтрація даних через SSH (Порт 22)",
            subtitle: "Симптом: Система виявлення вторгнень (IDS) сигналізує про витік трафіку",
            layout: "grid-2",
            cards: [
              { num: "01", col: "red", title: "Інцидент безпеки", desc: "Система IDS зафіксувала критичний алерт: <strong>ПК-04 (192.168.10.84)</strong> передає 2.4 ГБ зашифрованого трафіку на підозрілий зарубіжний сервер через порт 22 (SSH).", cli: "ALERT: [1:2010935:2] ET EXPLOIT Outbound SSH Connection to Threat Intel C2 IP 185.220.101.5\nSrc: 192.168.10.84:54210 -> Dst: 185.220.101.5:22", tag: "Невідкладна дія: Ізоляція скомпрометованого ПК" },
              { num: "02", col: "amber", title: "Реагування за 6 кроками", desc: "• <strong>Крок 1:</strong> Ізолювати хост (відключити порт комутатора).<br>• <strong>Крок 2:</strong> Теорія про зворотний SSH-тунель зловмисника.<br>• <strong>Крок 3:</strong> Перевірка процесів командою <code>netstat -ano | findstr :22</code>.<br>• <strong>Крок 4:</strong> Знищення процесу шкідника, блокування IP на фаєрволі.<br>• <strong>Крок 5:</strong> Антивірусне сканування, перевстановлення ОС з чистого образу.<br>• <strong>Крок 6:</strong> Складання звіту Incident Response та оновлення правил фаєрволу." }
            ],
            notes: "СЛАЙД 12: Реагування на кіберінцидент. Чому важливо негайно ізолювати хост від мережі, щоб запобігти горизонтальному просуванню атаки."
          },
          {
            badge: "ПРАКТИЧНИЙ КЕЙС 3 // АТАКА НА РІВНІ L2",
            badgeClass: "purple",
            title: "Атака ARP-спуфінгу (Двійник / Doppelgänger)",
            subtitle: "Симптом: Помилки сертифікатів SSL/TLS у браузері та раптове падіння швидкості",
            layout: "grid-2",
            cards: [
              { num: "01", col: "purple", title: "Аналіз таблиці ARP", desc: "Ви виконали команду <code>arp -a</code> на комп'ютері жертви і виявили аномалію:", cli: "Interface: 192.168.1.105 --- 0x3\n  Internet Address      Physical Address      Type\n  192.168.1.1           b8-27-eb-93-11-aa     dynamic  <-- Основний шлюз\n  192.168.1.55          b8-27-eb-93-11-aa     dynamic  <-- Ноутбук студента!", tag: "Діагноз: Атака посередника (Man-in-the-Middle)" },
              { num: "02", col: "green", title: "Усунення та захист комутатора", desc: "• <strong>Невідкладні дії:</strong> Вимкнути порт комутатора з MAC <code>b8-27-eb-93-11-aa</code>.<br>• <strong>Очищення клієнта:</strong> Скинути кеш ARP: <code>netsh interface ip delete arpcache</code>.<br>• <strong>Крок 5 (Захист L2):</strong> Увімкнути <strong>Dynamic ARP Inspection (DAI)</strong> та <strong>DHCP Snooping</strong> на комутаторах Cisco.<br>• <strong>Крок 6 (Звіт):</strong> Зафіксувати MAC порушника у звіті." }
            ],
            notes: "СЛАЙД 13: Отруєння ARP. Якщо дві IP-адреси мають однаковий MAC, у мережі діє атака Man-in-the-Middle! Поясніть захист через DAI."
          },
          {
            badge: "ІНЖЕНЕРНІ СТАНДАРТИ",
            badgeClass: "cyan",
            title: "Як побудувати бездоганну блок-схему",
            subtitle: "Перетворення логіки діагностики на точне дерево прийняття рішень",
            layout: "grid-3",
            cards: [
              { num: "01", col: "cyan", title: "Ромби прийняття рішень", desc: "Кожен тест у блок-схемі має бути <strong>конкретною командою CLI</strong> з двома чіткими виходами: <strong>[УСПІХ → ТАК]</strong> та <strong>[ЗБІЙ → НІ]</strong>.", cli: "[ping 192.168.1.1]\n   /         \\\n [УСПІХ]     [ЗБІЙ]" },
              { num: "02", col: "amber", title: "Жодних розмитих формулювань", desc: "Ніколи не пишіть <em>'Перевірити ПК'</em> або <em>'Полагодити мережу'</em>. Записуйте чітку команду: <code>ipconfig /flushdns</code> або <code>tracert -d 8.8.8.8</code>.", tag: "Інженерна точність" },
              { num: "03", col: "green", title: "Кінцеві точки процесів", desc: "Кожна гілка повинна завершуватися одним з результатів:<br><br>• <strong>[ПРОБЛЕМУ ВИРІШЕНО ТА ЗДОКУМЕНТОВАНО]</strong><br>• <strong>[ЕСКАЛАЦІЯ НА РІВЕНЬ 2 / АДМІНІСТРАТОР]</strong>", tag: "Чітке завершення" }
            ],
            notes: "СЛАЙД 14: Критерії оцінювання блок-схеми: точність команд, бінарні розгалуження та логічне завершення."
          },
          {
            badge: "ПОЧАТОК ПРАКТИКИ",
            title: "Перехід до інтерактивної практичної роботи",
            subtitle: "Відкрийте консоль та перейдіть до робочого зошита лабораторної роботи.",
            layout: "launch",
            notes: "СЛАЙД 15: Старт практичної частини. Учні відкривають activity.html та переходять до завдань."
          }
        ]
      }
    };

    let currentSlide = 1;
    const totalSlides = 15;
    let currentLang = 'en';

    function renderSlide() {
      const db = SLIDES_DB[currentLang] || SLIDES_DB.en;
      const sData = db.slides[currentSlide - 1];
      const stage = document.getElementById('stage');

      // Update header UI text
      document.getElementById('brand-text').textContent = db.brand;
      document.getElementById('brand-sub').textContent = db.sub;
      document.getElementById('txt-notes').textContent = db.notes;
      document.getElementById('txt-fs').textContent = db.fs;
      document.getElementById('txt-act').textContent = db.act;
      document.getElementById('btn-prev').innerHTML = db.prev;
      document.getElementById('btn-next').innerHTML = db.next;
      document.getElementById('txt-notes-header').textContent = db.notesHeader;

      document.getElementById('hint-prev').innerHTML = `<kbd>&larr;</kbd> ${db.hints.prev}`;
      document.getElementById('hint-next').innerHTML = `<kbd>&rarr;</kbd> ${db.hints.next}`;
      document.getElementById('hint-adv').innerHTML = `<kbd>Space</kbd> ${db.hints.adv}`;
      document.getElementById('hint-notes').innerHTML = `<kbd>N</kbd> ${db.hints.notes}`;
      document.getElementById('hint-fs').innerHTML = `<kbd>F</kbd> ${db.hints.fs}`;

      let contentHtml = '';
      const bClass = sData.badgeClass ? ` ${sData.badgeClass}` : '';

      if (sData.layout === 'grid-2' || sData.layout === 'grid-3' || sData.layout === 'grid-6') {
        const cardHtmls = sData.cards.map(c => `
          <div class="card" ${c.col ? `style="border-left: 4px solid var(--${c.col});"` : ''}>
            ${c.num ? `<div class="card-num ${c.col || ''}">${c.num}</div>` : ''}
            <h2 class="card-title">${c.title}</h2>
            <div class="card-desc">${c.desc}</div>
            ${c.cli ? `<div class="cli-box ${c.col || ''}">${c.cli}</div>` : ''}
            ${c.tag ? `<div class="card-tag" style="color:var(--${c.col || 'green'});">${c.tag}</div>` : ''}
          </div>
        `).join('');

        contentHtml = `
          <div class="slide-badge${bClass}">${sData.badge}</div>
          <h1 class="slide-title">${sData.title}</h1>
          <p class="slide-subtitle">${sData.subtitle}</p>
          <div class="${sData.layout}">
            ${cardHtmls}
          </div>
        `;
      } else if (sData.layout === 'ladder') {
        const ladderHtmls = sData.steps.map(st => `
          <div class="card" style="padding:0.7rem 1.1rem; flex-direction:row; align-items:center; justify-content:space-between;">
            <div><strong style="color:var(--cyan);">${st.num}. ${st.title}:</strong> <code>${st.cmd}</code></div>
            <span style="color:var(--text-muted); font-size:0.8rem;">${st.desc}</span>
          </div>
        `).join('');

        contentHtml = `
          <div class="slide-badge${bClass}">${sData.badge}</div>
          <h1 class="slide-title">${sData.title}</h1>
          <p class="slide-subtitle">${sData.subtitle}</p>
          <div style="display:flex; flex-direction:column; gap:0.7rem; flex:1;">
            ${ladderHtmls}
          </div>
        `;
      } else if (sData.layout === 'sim') {
        const simLabels = {
          en: { prompt: "SELECT DIAGNOSTIC COMMAND TO EXECUTE:", loop: "Loopback Adapter", gw: "Default Gateway (LAN)", wan: "External Public IP (WAN)", dns: "Domain Name (DNS)", tel: "Live Diagnostic Telemetry", initial: "Click any command on the left to initiate the binary search protocol..." },
          ar: { prompt: "اختر أمر الفحص والتشخيص لتنفيذه:", loop: "محول الاسترجاع المحلي (Loopback)", gw: "البوابة الافتراضية (الشبكة المحلية)", wan: "عنوان IP خارجي عام (الإنترنت)", dns: "خادم أسماء النطاقات (DNS)", tel: "شاشة القياسات والنتائج اللحظية", initial: "اضغط على أي أمر من القائمة لتشغيل بروتوكول البحث الثنائي..." },
          uk: { prompt: "ОБЕРІТЬ КОМАНДУ ДЛЯ ВИКОНАННЯ:", loop: "Локальний стек (Loopback)", gw: "Основний шлюз (LAN)", wan: "Зовнішня IP-адреса (WAN)", dns: "Доменне ім'я (DNS)", tel: "Телеметрія виконання в реальному часі", initial: "Натисніть будь-яку команду ліворуч для запуску бінарного пошуку..." }
        }[currentLang] || { prompt: "SELECT DIAGNOSTIC COMMAND:", loop: "Loopback", gw: "Gateway", wan: "WAN IP", dns: "DNS", tel: "Telemetry", initial: "Click any command..." };

        contentHtml = `
          <div class="slide-badge${bClass}">${sData.badge}</div>
          <h1 class="slide-title">${sData.title}</h1>
          <p class="slide-subtitle">${sData.subtitle}</p>
          <div class="grid-2">
            <div class="sim-container">
              <div style="font-size:0.85rem; color:var(--text-muted); font-weight:700;">${simLabels.prompt}</div>
              <div class="osi-ladder">
                <div class="osi-step" onclick="runSim(1)">
                  <div class="osi-step-left"><span class="osi-num">01</span><div><div class="osi-name">${simLabels.loop}</div><div class="osi-cmd">ping 127.0.0.1</div></div></div>
                  <span id="sim-status-1" class="osi-status untested">READY</span>
                </div>
                <div class="osi-step" onclick="runSim(2)">
                  <div class="osi-step-left"><span class="osi-num">02</span><div><div class="osi-name">${simLabels.gw}</div><div class="osi-cmd">ping 192.168.1.1</div></div></div>
                  <span id="sim-status-2" class="osi-status untested">READY</span>
                </div>
                <div class="osi-step" onclick="runSim(3)">
                  <div class="osi-step-left"><span class="osi-num">03</span><div><div class="osi-name">${simLabels.wan}</div><div class="osi-cmd">ping 8.8.8.8</div></div></div>
                  <span id="sim-status-3" class="osi-status untested">READY</span>
                </div>
                <div class="osi-step" onclick="runSim(4)">
                  <div class="osi-step-left"><span class="osi-num">04</span><div><div class="osi-name">${simLabels.dns}</div><div class="osi-cmd">nslookup google.com</div></div></div>
                  <span id="sim-status-4" class="osi-status untested">READY</span>
                </div>
              </div>
            </div>
            <div class="card" style="justify-content:flex-start;">
              <h2 class="card-title">${simLabels.tel}</h2>
              <div id="sim-output" class="cli-box" style="height: 220px; overflow-y: auto;">${simLabels.initial}</div>
              <div id="sim-verdict" style="margin-top: 0.8rem; font-size: 0.88rem; color: var(--green); font-weight: 700;"></div>
            </div>
          </div>
        `;
      } else if (sData.layout === 'launch') {
        const launchLabels = {
          en: { title: "Today's Lab Directives", items: ["1. Open the Divide & Conquer Lab Activity.", "2. Work through the 5 Progressive Scenarios (Physical → APIPA → DNS → Security Incident → ARP Attack).", "3. Use the built-in Virtual Terminal to test CLI commands.", "4. Construct your Logic Flowchart Trees.", "5. Export your completed work as a PDF for grading!"], ready: "Ready to Begin?", sub: "Launch the interactive student workbench now.", btn: "[ OPEN LAB ACTIVITY HUB ]" },
          ar: { title: "توجيهات النشاط العملي اليوم", items: ["1. افتح ورقة عمل النشاط العملي (Divide & Conquer Workbench).", "2. شخّص المستويات الخمسة المتدرجة (الطبقة الفيزيائية ← خلل APIPA ← عطل DNS ← حادثة أمنية ← هجوم ARP).", "3. استخدم الطرفية الافتراضية المدمجة لتجربة الأوامر عملياً.", "4. ابنِ مخططات التدفق المنطقي الثنائية.", "5. صدّر عملك المكتمل بصيغة PDF للتقييم والدرجات!"], ready: "جاهز للانطلاق؟", sub: "افتح منصة العمل التفاعلية للطلاب الآن.", btn: "[ فتح منصة النشاط العملي ]" },
          uk: { title: "Завдання сьогоднішньої практики", items: ["1. Відкрийте практичну роботу (Divide & Conquer Workbench).", "2. Пройдіть 5 послідовних рівнів (Фізичний → APIPA → DNS → Кіберінцидент → Атака ARP).", "3. Використовуйте віртуальний термінал для виконання діагностичних команд.", "4. Побудуйте логічні блок-схеми бінарного пошуку.", "5. Експортуйте готову роботу у формат PDF для оцінювання!"], ready: "Готові розпочати?", sub: "Запустіть інтерактивний робочий простір прямо зараз.", btn: "[ ВІДКРИТИ ПРАКТИЧНУ РОБОТУ ]" }
        }[currentLang] || { title: "Directives", items: [], ready: "Ready?", sub: "", btn: "Open" };

        contentHtml = `
          <div class="slide-badge${bClass}">${sData.badge}</div>
          <h1 class="slide-title">${sData.title}</h1>
          <p class="slide-subtitle">${sData.subtitle}</p>
          <div class="grid-2">
            <div class="card" style="border: 2px solid var(--green);">
              <h2 class="card-title" style="color:var(--green); font-size:1.3rem;">${launchLabels.title}</h2>
              <ul style="margin: 0.8rem 0 0 1.2rem; color: var(--text-muted); font-size: 0.9rem; line-height: 2;">
                ${launchLabels.items.map(it => `<li>${it}</li>`).join('')}
              </ul>
            </div>
            <div class="card" style="justify-content:center; align-items:center; text-align:center; background:rgba(57,255,158,0.03);">
              <div style="font-size:3rem; margin-bottom:0.8rem;">⚡</div>
              <h3 style="font-size:1.3rem; color:#fff; font-family:'Space Grotesk';">${launchLabels.ready}</h3>
              <p style="color:var(--text-muted); font-size:0.85rem; margin:0.6rem 0 1.2rem;">${launchLabels.sub}</p>
              <a href="activity.html" class="btn-ctrl" style="background:var(--green); color:#000; font-weight:800; font-size:0.9rem; padding:0.7rem 1.6rem; border-radius:6px; text-decoration:none;">
                ${launchLabels.btn}
              </a>
            </div>
          </div>
        `;
      }

      stage.innerHTML = `<section class="slide active">${contentHtml}</section>`;

      // Update counter and progress bar
      document.getElementById('slide-counter').textContent = `${String(currentSlide).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;
      document.getElementById('progress-fill').style.width = `${(currentSlide / totalSlides) * 100}%`;

      // Update presenter notes
      document.getElementById('presenter-content').textContent = sData.notes || "";
    }

    function nextSlide() {
      if (currentSlide < totalSlides) {
        currentSlide++;
        renderSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 1) {
        currentSlide--;
        renderSlide();
      }
    }

    function toggleNotes() {
      document.getElementById('presenter-drawer').classList.toggle('open');
      document.getElementById('btn-notes').classList.toggle('active');
    }

    function toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => alert(err.message));
      } else {
        document.exitFullscreen();
      }
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'Space' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key.toLowerCase() === 'n') {
        toggleNotes();
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullScreen();
      } else if (e.key === 'Home') {
        currentSlide = 1;
        renderSlide();
      } else if (e.key === 'End') {
        currentSlide = totalSlides;
        renderSlide();
      }
    });

    function runSim(step) {
      const output = document.getElementById('sim-output');
      const verdict = document.getElementById('sim-verdict');
      const s1 = document.getElementById('sim-status-1');
      const s2 = document.getElementById('sim-status-2');
      const s3 = document.getElementById('sim-status-3');
      const s4 = document.getElementById('sim-status-4');

      if (step === 1) {
        s1.className = 'osi-status pass'; s1.textContent = 'PASS';
        output.textContent = `C:\\> ping 127.0.0.1\n\nPinging 127.0.0.1 with 32 bytes of data:\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\n\n[+] LOOPBACK OK: Local TCP/IP software stack and NIC driver are 100% functional.`;
        verdict.textContent = currentLang === 'ar' ? "[+] مكدس البروتوكولات المحلي سليم 100%." : currentLang === 'uk' ? "[+] Локальний стек TCP/IP справний на 100%." : "[+] LOOPBACK OK: Local TCP/IP stack is healthy.";
      } else if (step === 2) {
        s2.className = 'osi-status pass'; s2.textContent = 'PASS';
        output.textContent = `C:\\> ping 192.168.1.1\n\nPinging 192.168.1.1 with 32 bytes of data:\nReply from 192.168.1.1: bytes=32 time=1ms TTL=64\n\n[+] LOCAL LAN LINK UP! Physical cable, wall jack, switch port, and router interface verified.`;
        verdict.textContent = currentLang === 'ar' ? "[+] تم الوصول للبوابة: الكابل والمحول سليم تماماً! استبعاد 50% من نطاق المشكلة." : currentLang === 'uk' ? "[+] Шлюз доступний: Кабель і комутатор справні! Відсічено 50% проблеми." : "[+] GATEWAY REACHABLE: The problem is NOT your cable or switch! Problem space reduced by 50%.";
      } else if (step === 3) {
        s3.className = 'osi-status pass'; s3.textContent = 'PASS';
        output.textContent = `C:\\> ping 8.8.8.8\n\nPinging 8.8.8.8 with 32 bytes of data:\nReply from 8.8.8.8: bytes=32 time=14ms TTL=117\n\n[+] WAN IP ROUTING OK: Default route, NAT, and ISP modem connection are active!`;
        verdict.textContent = currentLang === 'ar' ? "[+] اتصال الإنترنت الخارجي سليم: الخلل يكمن حتماً في الطبقة السابعة (DNS أو التطبيق)." : currentLang === 'uk' ? "[+] Зовнішній інтернет працює: Збій гарантовано на рівні 7 (DNS або додаток)." : "[+] WAN REACHABLE: Full external routing active. Problem must be in Layer 7 (DNS/App).";
      } else if (step === 4) {
        s4.className = 'osi-status fail'; s4.textContent = 'FAIL';
        output.textContent = `C:\\> nslookup google.com\n\nServer:  UnKnown\nAddress:  192.168.1.1\n\n*** DNS request to 192.168.1.1 timed out.\n\n[-] ROOT CAUSE PINPOINTED: DNS Resolver timed out! Local IP routing is healthy, but DNS configuration is dead.`;
        verdict.innerHTML = currentLang === 'ar' ? "<span style='color:var(--red);'>[-] تم تحديد السبب الجذري:</span> عنوان خادم الـ DNS المسجل في إعدادات المحول غير صالح أو متوقف!" : currentLang === 'uk' ? "<span style='color:var(--red);'>[-] ПЕРШОПРИЧИНУ ЗНАЙДЕНО:</span> Невірний або застарілий DNS-сервер у налаштуваннях адаптера!" : "<span style='color:var(--red);'>[-] ROOT CAUSE FOUND:</span> Stale/Incorrect DNS Resolver IP in network adapter settings!";
      }
    }

    function setLanguage(lang) {
      currentLang = lang;
      document.documentElement.lang = lang;
      document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
      localStorage.setItem('presentation_lang', lang);

      document.querySelectorAll('#lang-en, #lang-ar, #lang-uk').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`lang-${lang}`);
      if (activeBtn) activeBtn.classList.add('active');

      renderSlide();
    }

    const savedLang = localStorage.getItem('presentation_lang') || 'en';
    setLanguage(savedLang);
  </script>
</body>
</html>
"""

with open(presentation_html_path, "w", encoding="utf-8") as f:
    f.write(presentation_py)

print(f"Generated presentation.html -> {presentation_html_path}")

# ==============================================================================
# 2. GENERATE ACTIVITY.HTML WITH FULL DYNAMIC MULTILINGUAL ENGINE
# ==============================================================================
activity_html_path = os.path.join(TARGET_DIR, "activity.html")

activity_py = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lab Activity // CompTIA 6-Step Troubleshooting Workbench</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg: #040608;
      --panel: #090e13;
      --panel-elevated: #0f1720;
      --line: #1c2b26;
      --line-bright: #2d424b;
      --green: #39ff9e;
      --green-glow: rgba(57, 255, 158, 0.3);
      --green-dim: #164e37;
      --cyan: #38bdf8;
      --amber: #ffb454;
      --red: #ff5c72;
      --purple: #a855f7;
      --text: #d9f5e6;
      --text-muted: #79998d;
      --text-dim: #496359;
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      padding: 0;
      min-height: 100%;
      background: var(--bg);
      color: var(--text);
      font-family: 'JetBrains Mono', 'Courier New', monospace;
    }

    :root:lang(ar) {
      font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif;
    }

    [dir="rtl"] { text-align: start; }
    [dir="rtl"] code, [dir="rtl"] pre, [dir="rtl"] .font-mono, [dir="rtl"] .cli-term, [dir="rtl"] input.cli-input, [dir="rtl"] .term-output {
      direction: ltr !important;
      unicode-bidi: isolate;
      text-align: left;
    }

    @media screen {
      body {
        background-image:
          linear-gradient(rgba(57,255,158,0.04) 1px, transparent 1px),
          linear-gradient(90deg, rgba(57,255,158,0.04) 1px, transparent 1px);
        background-size: 36px 36px;
        background-color: var(--bg);
        position: relative;
        overflow-x: hidden;
      }
      body::before {
        content: ""; position: fixed; inset: 0; pointer-events: none;
        background: repeating-linear-gradient(to bottom, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 2px, rgba(0,0,0,0.18) 3px, rgba(0,0,0,0) 4px);
        mix-blend-mode: multiply; z-index: 5;
      }
      body::after {
        content: ""; position: fixed; inset: 0; pointer-events: none;
        background: radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,0.65) 100%);
        z-index: 4;
      }
      .panel {
        background: linear-gradient(180deg, var(--panel), #060a0d);
        border: 1px solid var(--line);
        border-radius: 8px;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
      }
      .panel::before {
        content: ""; position: absolute; top: -1px; left: -1px; right: -1px; bottom: -1px; border: 1px solid transparent;
        background: linear-gradient(120deg, rgba(57,255,158,0.35), transparent 30%, transparent 70%, rgba(56,189,248,0.3)) border-box;
        -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
        border-radius: 8px;
      }
      .panel-head { border-bottom: 1px solid var(--line); }
      h1 {
        color: #eafff2;
        text-shadow: 0 0 8px rgba(57,255,158,0.35), 2px 0 0 rgba(255,92,114,0.25), -2px 0 0 rgba(84,180,255,0.25);
      }
      .student-input {
        background: rgba(4, 7, 10, 0.7);
        border: 1px solid var(--line);
        color: #fff;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        font-family: inherit;
        font-size: 0.9rem;
        width: 100%;
        transition: all 0.2s ease;
      }
      .student-input:focus {
        outline: none;
        border-color: var(--green);
        box-shadow: 0 0 10px var(--green-glow);
        background: rgba(9, 14, 19, 0.95);
      }
    }

    .wrap { position: relative; z-index: 2; min-height: 100vh; display: flex; flex-direction: column; padding: 3vh 5vw 6vh; }
    
    .topbar {
      display: flex; justify-content: space-between; align-items: baseline;
      font-size: clamp(0.68rem, 1vw, 0.85rem); color: var(--text-muted); letter-spacing: 0.08em;
      border-bottom: 1px solid var(--line); padding-bottom: 0.8em; margin-bottom: 3vh;
    }
    .topbar a { color: var(--text-muted); text-decoration: none; }
    .topbar a:hover { color: var(--green); }
    .topbar .dot { color: var(--green); }
    .blink { animation: blink 1.1s steps(1) infinite; }
    @keyframes blink { 50% { opacity: 0; } }

    header { text-align: center; margin-bottom: 4vh; }
    .prompt-line { font-size: clamp(0.75rem, 1.1vw, 0.95rem); color: var(--green); margin-bottom: 0.8em; letter-spacing: 0.03em; }
    .prompt-line .path { color: var(--amber); }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1.1; margin: 0; font-weight: 700;
    }
    .subtitle { margin-top: 0.6em; margin-bottom: 1.5em; font-size: clamp(0.85rem, 1.2vw, 1.05rem); color: var(--text-muted); letter-spacing: 0.15em; text-transform: uppercase; }
    .subtitle::before, .subtitle::after { content: "//"; color: var(--green-dim); margin: 0 0.6em; }

    .action-bar {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 2.5rem;
    }

    .btn-act {
      background: rgba(57,255,158,0.06);
      border: 1px solid var(--green);
      color: var(--green);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      padding: 0.7em 1.4em;
      cursor: pointer;
      border-radius: 4px;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
    }
    .btn-act:hover {
      background: rgba(57,255,158,0.18);
      box-shadow: 0 0 15px var(--green-glow);
      transform: translateY(-1px);
    }
    .btn-act.cyan { border-color: var(--cyan); color: var(--cyan); background: rgba(56,189,248,0.06); }
    .btn-act.cyan:hover { background: rgba(56,189,248,0.18); box-shadow: 0 0 15px rgba(56,189,248,0.4); }
    .btn-act.amber { border-color: var(--amber); color: var(--amber); background: rgba(255,180,84,0.06); }
    .btn-act.amber:hover { background: rgba(255,180,84,0.18); box-shadow: 0 0 15px rgba(255,180,84,0.4); }

    main { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2.5rem; }
    .panel { width: 100%; max-width: 1050px; }
    .panel-head {
      display: flex; align-items: center; justify-content: space-between; padding: 0.8em 1.4em;
      font-size: clamp(0.7rem, 1vw, 0.82rem); color: var(--text-muted); letter-spacing: 0.1em; text-transform: uppercase;
      font-weight: 700;
    }
    .panel-head .lights span { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 6px; }
    .lights .r { background: var(--red); } .lights .a { background: var(--amber); } .lights .g { background: var(--green); }

    .panel-body { padding: 2em; }
    
    .name-block {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: 1.5rem;
      margin-bottom: 1.8rem;
      font-family: 'Space Grotesk', sans-serif;
    }
    .name-field { display: flex; flex-direction: column; gap: 0.3rem; }
    .name-field label { color: var(--green); font-weight: 700; font-family: 'JetBrains Mono'; font-size: 0.8rem; letter-spacing: 0.05em; }

    .scenario-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 700; color: #fff; margin: 0 0 0.6em 0; display: flex; align-items: center; justify-content: space-between; }
    .scenario-title .tag { 
      font-size: 0.55em; vertical-align: middle; padding: 0.3em 0.7em; 
      border: 1px solid var(--amber); color: var(--amber); border-radius: 3px; font-family: 'JetBrains Mono'; font-weight: 800; letter-spacing: 0.1em;
    }
    .tag.hard { border-color: var(--red); color: var(--red); }
    .tag.easy { border-color: var(--green); color: var(--green); }
    .tag.cyan { border-color: var(--cyan); color: var(--cyan); }
    
    .situation {
      font-size: 0.95rem; color: var(--text); line-height: 1.6; margin-bottom: 1.5em; padding: 1rem 1.2rem;
      background: rgba(0,0,0,0.5); border-left: 3px solid var(--cyan); border-radius: 0 6px 6px 0;
    }
    
    .terminal-sim {
      background: #020305;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 1rem 1.2rem;
      margin-bottom: 1.5rem;
    }
    .term-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--text-muted);
      font-size: 0.75rem;
      margin-bottom: 0.8rem;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      padding-bottom: 0.4rem;
    }
    .term-btn-group { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.8rem; }
    .term-btn {
      background: var(--panel-elevated);
      border: 1px solid var(--line-bright);
      color: var(--cyan);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      padding: 0.3rem 0.7rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .term-btn:hover { border-color: var(--green); color: var(--green); }
    .term-output {
      background: #000;
      color: var(--green);
      padding: 0.8rem;
      border-radius: 4px;
      font-size: 0.82rem;
      min-height: 80px;
      max-height: 180px;
      overflow-y: auto;
      white-space: pre-wrap;
    }

    .step-block { margin-bottom: 1.8rem; }
    .step-label {
      font-size: 0.85rem; font-weight: 800; color: var(--green); margin-bottom: 0.4em; letter-spacing: 0.06em;
      display: flex; align-items: center; gap: 0.5rem;
    }
    .step-label.cyan { color: var(--cyan); }
    .step-label.amber { color: var(--amber); }
    .step-prompt { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.6em; line-height: 1.5; }

    .teacher-key-box {
      display: none;
      background: rgba(255, 180, 84, 0.08);
      border: 1px solid var(--amber);
      border-radius: 6px;
      padding: 1.2rem 1.4rem;
      margin-top: 1.5rem;
      font-size: 0.85rem;
      color: #fed7aa;
      line-height: 1.6;
    }
    .teacher-key-box.visible { display: block; }
    .teacher-key-title {
      color: var(--amber);
      font-weight: 800;
      letter-spacing: 0.08em;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      text-transform: uppercase;
      font-size: 0.8rem;
    }

    footer { text-align: center; margin-top: 4vh; color: var(--text-dim); font-size: clamp(0.72rem, 1vw, 0.86rem); letter-spacing: 0.06em; }
    footer .cursor { color: var(--green); }

    @media print {
      body { background: #ffffff !important; color: #000000 !important; font-family: Arial, sans-serif !important; }
      .topbar, footer, .prompt-line, header h1, .subtitle, .action-bar, .term-btn-group, .term-output { display: none !important; }
      .wrap { padding: 0 !important; }
      main { gap: 1.5rem !important; }
      .panel { background: #ffffff !important; border: 1px solid #000000 !important; page-break-inside: avoid; margin-bottom: 25px; box-shadow: none !important; }
      .panel::before { display: none !important; }
      .panel-head { border-bottom: 1px solid #000000 !important; color: #000000 !important; background: #f0f0f0 !important; padding: 0.5em 1em !important; }
      .lights { display: none !important; }
      .scenario-title { color: #000000 !important; font-size: 1.2rem !important; font-weight: bold !important; }
      .situation { color: #222222 !important; border-left: 3px solid #666666 !important; background: #fafafa !important; padding: 0.8em !important; }
      .step-label { color: #000000 !important; font-weight: bold !important; font-size: 0.85rem !important; }
      .step-prompt { color: #333333 !important; font-size: 0.85rem !important; }
      .student-input {
        background: transparent !important;
        border: none !important;
        border-bottom: 1px solid #777777 !important;
        border-radius: 0 !important;
        color: #000000 !important;
        padding: 0.2rem 0 !important;
        font-size: 0.85rem !important;
        min-height: 2em !important;
      }
      .tag { border-color: #000000 !important; color: #000000 !important; }
      .print-header { display: block !important; text-align: center; margin-bottom: 1.5rem; border-bottom: 2px solid #000; padding-bottom: 0.5rem; }
      .print-header h2 { margin: 0; font-size: 1.4rem; }
      .print-header p { margin: 0.2rem 0 0; font-size: 0.85rem; color: #444; }
    }

    .print-header { display: none; }
  </style>
</head>
<body>
  <div class="wrap">
    
    <div class="print-header">
      <h2 id="prt-school">A.W. Beattie Career Center &middot; Network Engineering &amp; Cybersecurity</h2>
      <p id="prt-title">Lab Activity: Divide &amp; Conquer // The CompTIA 6-Step Troubleshooting Model</p>
    </div>

    <div class="topbar">
      <span id="act-top-brand"><span class="dot">●</span> BEATTIE-NET // NETWORK ENGINEERING &amp; CYBERSECURITY</span>
      <span>MR. L <span class="blink">_</span></span>
    </div>

    <header>
      <div class="prompt-line"><span class="path">mrl@beattie-tech</span>:~$ ./run_activity.sh --module="Troubleshooting"</div>
      <h1 id="act-main-title">Divide &amp; Conquer Lab Workbench</h1>
      <div class="subtitle" id="act-sub-title">The CompTIA 6-Step Troubleshooting Model</div>
      
      <div class="action-bar">
        <button class="btn-act" onclick="window.print()">
          📄 <span id="btn-txt-print">Export / Print Student Worksheet (PDF)</span>
        </button>

        <button id="btn-toggle-key" class="btn-act amber" onclick="toggleAnswerKey()">
          🔑 <span id="key-label">Show Teacher Answer Key &amp; Rubric</span>
        </button>

        <a href="presentation.html" class="btn-act cyan">
          📺 <span id="btn-txt-pres">Open Slide Presentation →</span>
        </a>

        <div style="display:flex; background:var(--panel-elevated); border:1px solid var(--line-bright); border-radius:4px; padding:2px; font-size:0.75rem;">
          <button id="lang-en" class="btn-act" onclick="setLanguage('en')" style="border:none; padding:0.3rem 0.6rem;">EN</button>
          <button id="lang-ar" class="btn-act" onclick="setLanguage('ar')" style="border:none; padding:0.3rem 0.6rem;">عربي</button>
          <button id="lang-uk" class="btn-act" onclick="setLanguage('uk')" style="border:none; padding:0.3rem 0.6rem;">УКР</button>
        </div>
      </div>
    </header>

    <main id="activity-main">
      <!-- Dynamically rendered by renderActivity() -->
    </main>

    <footer>
      <span id="act-footer">END OF TRANSMISSION</span> <span class="cursor blink">█</span>
    </footer>
  </div>

  <script>
    const ACT_DB = {
      en: {
        school: "A.W. Beattie Career Center · Network Engineering & Cybersecurity",
        prtTitle: "Lab Activity: Divide & Conquer // The CompTIA 6-Step Troubleshooting Model",
        topBrand: "● BEATTIE-NET // NETWORK ENGINEERING & CYBERSECURITY",
        mainTitle: "Divide & Conquer Lab Workbench",
        subTitle: "The CompTIA 6-Step Troubleshooting Model",
        btnPrint: "Export / Print Student Worksheet (PDF)",
        btnKeyShow: "Show Teacher Answer Key & Rubric",
        btnKeyHide: "Hide Teacher Answer Key",
        btnPres: "Open Slide Presentation →",
        footer: "END OF TRANSMISSION",
        studId: {
          header: "STUDENT IDENTIFICATION & METHODOLOGY RUBRIC",
          nameLabel: "STUDENT NAME",
          dateLabel: "DATE",
          periodLabel: "PERIOD / SECTION",
          namePh: "e.g. John Doe",
          periodPh: "e.g. AM-1",
          missionTitle: "MISSION DIRECTIVE:",
          missionText: "For each scenario below, apply the formal <strong>CompTIA 6-Step Troubleshooting Model</strong> using the <strong>Divide & Conquer (Binary Search)</strong> methodology. Use the interactive virtual terminals to run diagnostic commands, then document your findings and action plan in the structured fields below.",
          missionFormula: "[1] Identify problem → [2] Establish theory → [3] Test theory → [4] Plan & implement fix → [5] Verify & prevent → [6] Document outcomes."
        },
        scenarios: [
          {
            num: 1,
            head: "LEVEL 1: PHYSICAL LAYER // LAYER 1 & 2",
            title: "The Silent Jack",
            tag: "DIFFICULTY: NOVICE · 100 PTS",
            tagClass: "easy",
            situation: "<strong>SITUATION:</strong> A student punches down a new Cat6 UTP cable into patch panel port 14 and wires the keystone wall jack in Room 204. They plug a test workstation into the jack using a known-good patch cable. The NIC link LEDs stay completely dark, and Windows reports: <code>\"Network Cable Unplugged.\"</code>",
            termTitle: "VIRTUAL TERMINAL // WORKSTATION-ROOM204",
            termSub: "CLI DIAGNOSTIC SANDBOX",
            termInitial: "Click a diagnostic button above to inspect endpoint telemetry...",
            termBtns: [
              { key: "ipconfig", label: "run: ipconfig /all" },
              { key: "link", label: "run: Test-NetConnection -InterfaceIndex 3" },
              { key: "tester", label: "run: check_cable_tester_output" }
            ],
            steps: [
              { label: "[STEP 1 & 2] // IDENTIFY PROBLEM & ESTABLISH THEORY", prompt: "What physical components must be checked first? State two probable physical root causes for this Layer 1 failure.", ph: "Enter your identification and theory..." },
              { label: "[STEP 3 & 4] // TEST THEORY & IMPLEMENT ACTION PLAN", prompt: "What hardware tool will you use to test the cable run? If the wiremap shows pins 1 and 2 are reversed (miswire), what is your step-by-step fix?", ph: "Enter test tool and remediation steps..." },
              { label: "[STEP 5 & 6] // VERIFY SYSTEM & DOCUMENT IN TICKET", prompt: "How do you verify full functionality (Step 5), and what exact resolution text should be recorded in the helpdesk ticket (Step 6)?", ph: "Enter verification test and ticket resolution log..." }
            ],
            keyTitle: "🔑 TEACHER ANSWER KEY & RUBRIC // SCENARIO 1",
            keyContent: "<strong>Step 1 & 2:</strong> Check NIC link lights, patch cable on both ends, switch port status. Theories: Keystone jack punchdown wire reversed (miswire), cable split pair, bad punchdown blade connection, or switch port disabled.<br><strong>Step 3 & 4:</strong> Use a digital Cable Continuity Tester / Wiremapper. If pins 1 & 2 are crossed, re-punch the keystone jack following TIA/EIA-568B standard using a 110 punchdown tool with cut blade facing out.<br><strong>Step 5 & 6:</strong> Verify link light goes solid green at 1 Gbps, workstation acquires IP via DHCP, and pings gateway. Ticket Doc: <em>'Re-punched Room 204 Port 14 keystone jack to T-568B to resolve pin 1-2 cross. Verified 1Gbps link & DHCP acquisition.'</em>"
          },
          {
            num: 2,
            head: "LEVEL 2: NETWORK LAYER // LAYER 3 (DHCP & IPV4)",
            title: "The APIPA 169.254 Anomaly",
            tag: "DIFFICULTY: NOVICE · 150 PTS",
            tagClass: "easy",
            situation: "<strong>SITUATION:</strong> All 12 computers in Lab B suddenly lose network connectivity simultaneously. Physical link LEDs on both the PCs and the switch are green. You run <code>ipconfig</code> on PC-01 and see IPv4 address <code>169.254.88.204</code> with subnet mask <code>255.255.0.0</code> and a blank default gateway.",
            termTitle: "VIRTUAL TERMINAL // LAB-B-PC01",
            termSub: "CLI DIAGNOSTIC SANDBOX",
            termInitial: "Click a diagnostic button above to inspect endpoint telemetry...",
            termBtns: [
              { key: "ipconfig", label: "run: ipconfig /all" },
              { key: "ping_loop", label: "run: ping 127.0.0.1" },
              { key: "renew", label: "run: ipconfig /renew" },
              { key: "dhcp_status", label: "run: Get-DhcpServerv4Scope -ComputerName 'DC01'" }
            ],
            steps: [
              { label: "[STEP 1 & 2] // IDENTIFY PROBLEM & ESTABLISH THEORY", prompt: "What does the 169.254.x.x address indicate? Since link lights are on, what network service is failing?", ph: "Explain APIPA and identify the failed service..." },
              { label: "[STEP 3 & 4] // TEST THEORY & IMPLEMENT ACTION PLAN", prompt: "How do you test the DHCP service? If the DHCP scope pool is 100% full, what is your remediation plan?", ph: "Explain testing command and how to fix scope exhaustion..." },
              { label: "[STEP 5 & 6] // VERIFY SYSTEM & PREVENTATIVE HARDENING", prompt: "What CLI command forces the clients to get a new IP? What preventative measure stops this from recurring?", ph: "Command to force IP lease and preventative setting..." }
            ],
            keyTitle: "🔑 TEACHER ANSWER KEY & RUBRIC // SCENARIO 2",
            keyContent: "<strong>Step 1 & 2:</strong> 169.254.x.x is APIPA (Automatic Private IP Addressing / RFC 3927). It proves Layer 1 & 2 are UP, but the client broadcasted DHCPDISCOVER and received no DHCPOFFER. The DHCP Server service is offline or scope is exhausted.<br><strong>Step 3 & 4:</strong> Check DHCP Server console/service. If scope is exhausted, expand the subnet (e.g. from /24 to /23) or reduce DHCP lease time from 8 days to 4 hours to reclaim stale leases.<br><strong>Step 5 & 6:</strong> Run <code>ipconfig /release</code> followed by <code>ipconfig /renew</code>. Preventative: configure automated 80% scope capacity threshold alerts in Windows Server / Syslog."
          },
          {
            num: 3,
            head: "LEVEL 3: TRANSPORT & APPLICATION LAYER // DNS & FIREWALL",
            title: "The DNS Dilemma",
            tag: "DIFFICULTY: INTERMEDIATE · 200 PTS",
            tagClass: "cyan",
            situation: "<strong>SITUATION:</strong> A teacher reports: <em>'The internet is completely down in my classroom!'</em> You open the command prompt on her workstation. You can successfully <code>ping 8.8.8.8</code> with 12ms latency, but when you run <code>ping google.com</code>, you get: <code>\"Ping request could not find host google.com. Please check the name and try again.\"</code>",
            termTitle: "VIRTUAL TERMINAL // TEACHER-WS01",
            termSub: "CLI DIAGNOSTIC SANDBOX",
            termInitial: "Click a diagnostic button above to inspect endpoint telemetry...",
            termBtns: [
              { key: "ping_ip", label: "run: ping 8.8.8.8" },
              { key: "ping_dns", label: "run: ping google.com" },
              { key: "nslookup", label: "run: nslookup google.com" },
              { key: "ipconfig_dns", label: "run: ipconfig /displaydns" }
            ],
            steps: [
              { label: "[STEP 1 & 2] // IDENTIFY PROBLEM & ESTABLISH THEORY", prompt: "What does the successful 8.8.8.8 ping prove about Layers 1, 2, and 3? What protocol is failing on google.com?", ph: "Analyze what the successful vs failed ping proves..." },
              { label: "[STEP 3 & 4] // TEST THEORY & IMPLEMENT ACTION PLAN", prompt: "What command tests DNS resolution specifically? If the adapter had a rogue DNS IP (10.0.0.99) manually configured, how do you fix it?", ph: "Testing command and configuration fix..." },
              { label: "[STEP 5 & 6] // VERIFY SYSTEM & PREVENTATIVE HARDENING", prompt: "What command clears the local DNS cache? Write the exact 1-sentence resolution note for the ticket.", ph: "Cache clear command and ticket resolution text..." }
            ],
            keyTitle: "🔑 TEACHER ANSWER KEY & RUBRIC // SCENARIO 3",
            keyContent: "<strong>Step 1 & 2:</strong> Successful ping to 8.8.8.8 proves physical link, local gateway, NAT, and WAN internet routing (Layers 1-3) are 100% operational! The failure on hostname proves DNS (Domain Name System, UDP/TCP Port 53) at Layer 7 is failing.<br><strong>Step 3 & 4:</strong> Test with <code>nslookup google.com</code>. Fix: Set IPv4 adapter properties to <em>'Obtain DNS server address automatically'</em> via DHCP or set to verified enterprise DNS servers (e.g. 1.1.1.1, 8.8.8.8).<br><strong>Step 5 & 6:</strong> Run <code>ipconfig /flushdns</code>. Ticket Doc: <em>'Removed static rogue DNS address 10.0.0.99; set adapter to DHCP DNS auto-discovery and flushed local DNS resolver cache. Verified web browsing to google.com.'</em>"
          },
          {
            num: 4,
            head: "LEVEL 4: INCIDENT RESPONSE // CYBERSECURITY TRIAGE",
            title: "Suspicious Outbound Port 22 Exfiltration",
            tag: "DIFFICULTY: ADVANCED · 250 PTS",
            tagClass: "hard",
            situation: "<strong>SITUATION:</strong> Your Security Operations Center (SOC) IDS fires a critical severity alert. Workstation-19 (192.168.10.84) in the CAD lab has established an active outbound connection on <strong>Port 22 (SSH)</strong> to an unclassified IP in Bulgaria (185.220.101.5), transferring over 3.2 GB of compressed data.",
            termTitle: "VIRTUAL TERMINAL // WORKSTATION-19 FORENSIC SHELL",
            termSub: "CLI DIAGNOSTIC SANDBOX",
            termInitial: "Click a diagnostic button above to inspect endpoint telemetry...",
            termBtns: [
              { key: "netstat", label: "run: netstat -ano | findstr :22" },
              { key: "tasklist", label: "run: tasklist /fi \"PID eq 4820\"" },
              { key: "firewall", label: "run: netsh advfirewall firewall show rule name=all" }
            ],
            steps: [
              { label: "[STEP 1 & 2] // IDENTIFY PROBLEM & ESTABLISH THEORY", prompt: "What is your IMMEDIATE first operational action (Step 1)? What protocol runs on Port 22, and what is the attacker doing?", ph: "Immediate action and threat theory..." },
              { label: "[STEP 3 & 4] // TEST THEORY & IMPLEMENT ACTION PLAN", prompt: "What CLI command links the network socket to the rogue process PID? How do you terminate the process and neutralize persistence?", ph: "Process inspection command and neutralization steps..." },
              { label: "[STEP 5 & 6] // VERIFY SYSTEM & PREVENTATIVE HARDENING", prompt: "What firewall egress rule should be implemented to prevent unauthorized outbound SSH from student workstations in the future?", ph: "Firewall egress policy and post-incident documentation..." }
            ],
            keyTitle: "🔑 TEACHER ANSWER KEY & RUBRIC // SCENARIO 4",
            keyContent: "<strong>Step 1 & 2:</strong> Immediate Action: Isolate the endpoint from the network (unplug cable or shut switch port) to prevent further data loss or lateral movement. Port 22 is SSH (Secure Shell). Attacker is running a reverse SSH tunnel for data exfiltration.<br><strong>Step 3 & 4:</strong> Run <code>netstat -ano | findstr :22</code> to identify the PID (e.g. PID 4820), then <code>taskkill /PID 4820 /F</code>. Inspect Task Scheduler and Startup registry keys for persistence scripts.<br><strong>Step 5 & 6:</strong> Preventative: Block outbound Port 22 egress on edge firewall for all subnets except designated bastion hosts. Run malware scan, re-image system from golden image, and document incident response report."
          },
          {
            num: 5,
            head: "LEVEL 5: ENTERPRISE SECURITY // LAYER 2 CYBER ATTACK",
            title: "The Doppelgänger ARP Attack",
            tag: "DIFFICULTY: EXPERT · 300 PTS",
            tagClass: "hard",
            situation: "<strong>SITUATION:</strong> Users on VLAN 10 report random web browser SSL/TLS certificate warnings (e.g. <em>'Your connection is not private - invalid certificate authority'</em>) and dropped connections. You inspect the victim workstation and check the ARP cache.",
            termTitle: "VIRTUAL TERMINAL // VICTIM-WS04",
            termSub: "CLI DIAGNOSTIC SANDBOX",
            termInitial: "Click a diagnostic button above to inspect endpoint telemetry...",
            termBtns: [
              { key: "arp", label: "run: arp -a" },
              { key: "tracert", label: "run: tracert -d 8.8.8.8" },
              { key: "switch_mac", label: "run: show mac address-table | include b827" }
            ],
            steps: [
              { label: "[STEP 1 & 2] // IDENTIFY PROBLEM & ESTABLISH THEORY", prompt: "Look at the <code>arp -a</code> table. Why do two different IP addresses have the exact same MAC address? Name the exact Layer 2 cyber attack.", ph: "Explain the ARP anomaly and name the cyber attack..." },
              { label: "[STEP 3 & 4] // TEST THEORY & IMPLEMENT ACTION PLAN", prompt: "How do you trace the rogue MAC to a physical switch port? What immediate action stops the attack?", ph: "Switch tracing command and containment action..." },
              { label: "[STEP 5 & 6] // VERIFY SYSTEM & ENTERPRISE HARDENING", prompt: "What two enterprise Cisco switch security features (Step 5) permanently block ARP spoofing and rogue DHCP servers forever?", ph: "Enterprise switch security features (DAI / DHCP Snooping)..." }
            ],
            keyTitle: "🔑 TEACHER ANSWER KEY & RUBRIC // SCENARIO 5",
            keyContent: "<strong>Step 1 & 2:</strong> ARP Spoofing / ARP Cache Poisoning (Man-in-the-Middle). A rogue device is emitting gratuitous ARP replies claiming the Default Gateway IP (192.168.1.1) belongs to its own MAC address (b8-27-eb-93-11-aa) to intercept and decrypt user traffic.<br><strong>Step 3 & 4:</strong> Run <code>show mac address-table | include b827</code> on core switch to find the physical port (e.g. GigabitEthernet 0/12). Issue <code>shutdown</code> command on that port to sever the attacker.<br><strong>Step 5 & 6:</strong> Enable <strong>Dynamic ARP Inspection (DAI)</strong> and <strong>DHCP Snooping</strong> on all access switches, combined with <strong>Port Security (Sticky MAC)</strong>. Flush victim ARP cache with <code>netsh interface ip delete arpcache</code>. Document in security incident log."
          }
        ]
      },

      ar: {
        school: "مركز بيتي المهني والتقني · هندسة الشبكات والأمن السيبراني",
        prtTitle: "ورقة عمل النشاط العملي: منهجية فرّق تسُد // نموذج حل المشكلات المعتمد من CompTIA",
        topBrand: "● شبكة بيتي // هندسة الشبكات والأمن السيبراني",
        mainTitle: "منصة ورقة العمل التفاعلية: فرّق تسُد",
        subTitle: "منهجية حل المشكلات المعتمدة من CompTIA (الخطوات الست)",
        btnPrint: "تصدير / طباعة ورقة العمل (PDF)",
        btnKeyShow: "عرض دليل المعلم والإجابات النموذجية",
        btnKeyHide: "إخفاء إجابات المعلم",
        btnPres: "فتح العرض التقديمي للدرس ←",
        footer: "نهاية الإرسال والتقرير",
        studId: {
          header: "بيانات الطالب ومعايير التقييم والمنهجية",
          nameLabel: "اسم الطالب",
          dateLabel: "التاريخ",
          periodLabel: "الفترة / الشعبة",
          namePh: "مثال: أحمد محمد",
          periodPh: "مثال: الفترة الصباحية 1",
          missionTitle: "توجيهات المهمة:",
          missionText: "لكل سيناريو أدناه، طبّق <strong>نموذج الخطوات الست لحل الأعطال المعتمد من CompTIA</strong> باستخدام استراتيجية <strong>فرّق تسُد (البحث الثنائي)</strong>. استخدم الطرفيات الافتراضية المدمجة لتنفيذ أوامر التشخيص، ثم وثّق استنتاجاتك وخطة عملك في الحقول المخصصة.",
          missionFormula: "[1] تحديد المشكلة ← [2] صياغة الفرضية ← [3] اختبار الفرضية ← [4] خطة العمل والتنفيذ ← [5] التحقق والوقاية ← [6] توثيق النتائج."
        },
        scenarios: [
          {
            num: 1,
            head: "المستوى 1: الطبقة الفيزيائية // الطبقتان 1 و 2",
            title: "المقبس الصامت",
            tag: "المستوى: مبتدئ · 100 نقطة",
            tagClass: "easy",
            situation: "<strong>السيناريو:</strong> قام طالب بكبس كابل Cat6 UTP جديد في لوحة التوزيع (Patch Panel) المنفذ 14، وثبّت مقبس الجدار في القاعة 204. عند توصيل حاسوب فحص بالمقبس باستخدام كابل سليم، ظلت أضواء بطاقة الشبكة (NIC LEDs) مطفأة تماماً، وظهرت رسالة في Windows: <code>\"كابل الشبكة غير متصل.\"</code>",
            termTitle: "الطرفية الافتراضية // حاسوب القاعة 204",
            termSub: "بيئة تشخيص الأوامر المباشرة",
            termInitial: "اضغط على أحد أزرار التشخيص أعلاه لفحص القياسات الرقمية للمنفذ...",
            termBtns: [
              { key: "ipconfig", label: "تشغيل: ipconfig /all" },
              { key: "link", label: "تشغيل: Test-NetConnection -InterfaceIndex 3" },
              { key: "tester", label: "تشغيل: check_cable_tester_output" }
            ],
            steps: [
              { label: "[الخطوتان 1 و 2] // تحديد المشكلة وبناء الفرضية", prompt: "ما هي المكونات الفيزيائية التي يجب فحصها أولاً؟ اذكر سببين محتملين لعطل الطبقة الأولى هذا.", ph: "اكتب تحديد المشكلة والفرضية..." },
              { label: "[الخطوتان 3 و 4] // اختبار الفرضية وتنفيذ خطة العمل", prompt: "ما هي الأداة التي ستستخدمها لفحص التوصيل؟ إذا أظهر الفاحص انعكاس السلكين 1 و 2، ما هي خطوات الإصلاح؟", ph: "اكتب أداة الفحص وخطوات الإصلاح..." },
              { label: "[الخطوتان 5 و 6] // التحقق من النظام وتوثيق التذكرة", prompt: "كيف تتحقق من عمل النظام بالكامل (الخطوة 5)، وما هو النص الدقيق الذي ستسجله لإغلاق التذكرة (الخطوة 6)؟", ph: "اكتب اختبار التحقق ونص توثيق التذكرة..." }
            ],
            keyTitle: "🔑 دليل وإجابات المعلم // السيناريو الأول",
            keyContent: "<strong>الخطوتان 1 و 2:</strong> فحص أضواء بطاقة الشبكة، كابل التوصيل على الطرفين، وحالة منفذ المحول. الفرضيات: انعكاس ألوان الأسلاك في المقبس (Miswire)، انقطاع زوج أسلاك، أو تعطيل منفذ المحول.<br><strong>الخطوتان 3 و 4:</strong> استخدام فاحص الكابلات الرقمي (Cable Tester / Wiremapper). إذا انعكس السلكان 1 و 2، أعد كبس مقبس الجدار وفق معيار TIA/EIA-568B باستخدام أداة الكبس 110.<br><strong>الخطوتان 5 و 6:</strong> التحقق من إضاءة مؤشر الشبكة باللون الأخضر بسرعة 1Gbps واستلام IP عبر DHCP والتواصل مع البوابة. نص التوثيق: <em>'تمت إعادة كبس مقبس القاعة 204 المنفذ 14 وفق معيار T-568B لحل انعكاس السلكين 1-2. تم التحقق من سرعة 1Gbps وعمل الـ DHCP.'</em>"
          },
          {
            num: 2,
            head: "المستوى 2: طبقة الشبكة // الطبقة 3 (DHCP و IPV4)",
            title: "خلل عنوان APIPA (169.254)",
            tag: "المستوى: مبتدئ · 150 نقطة",
            tagClass: "easy",
            situation: "<strong>السيناريو:</strong> فقدت جميع أجهزة الحاسوب الـ 12 في المختبر B الاتصال بالشبكة فجأة في نفس اللحظة. أضواء بطاقات الشبكة في الأجهزة والمحول خضراء ومضيئة. عند تشغيل <code>ipconfig</code> على الجهاز الأول، ظهر العنوان <code>169.254.88.204</code> مع قناع <code>255.255.0.0</code> وبوابة افتراضية فارغة.",
            termTitle: "الطرفية الافتراضية // حاسوب المعمل B-01",
            termSub: "بيئة تشخيص الأوامر المباشرة",
            termInitial: "اضغط على أحد أزرار التشخيص أعلاه لفحص القياسات الرقمية للمنفذ...",
            termBtns: [
              { key: "ipconfig", label: "تشغيل: ipconfig /all" },
              { key: "ping_loop", label: "تشغيل: ping 127.0.0.1" },
              { key: "renew", label: "تشغيل: ipconfig /renew" },
              { key: "dhcp_status", label: "تشغيل: Get-DhcpServerv4Scope -ComputerName 'DC01'" }
            ],
            steps: [
              { label: "[الخطوتان 1 و 2] // تحديد المشكلة وبناء الفرضية", prompt: "ماذا يعني العنوان 169.254.x.x؟ بما أن أضواء التوصيل تعمل، ما هي الخدمة المتوقفة؟", ph: "اشرح عنوان APIPA والخدمة المتوقفة..." },
              { label: "[الخطوتان 3 و 4] // اختبار الفرضية وتنفيذ خطة العمل", prompt: "كيف تفحص خدمة الـ DHCP؟ إذا كان نطاق العناوين ممتلئاً بنسبة 100%، ما هي خطة العلاج؟", ph: "اكتب أمر الفحص وطريقة حل نفاد النطاق..." },
              { label: "[الخطوتان 5 و 6] // التحقق من النظام والتحصين الوقائي", prompt: "ما هو الأمر الذي يجبر الأجهزة على طلب عنوان جديد؟ ما هو الإجراء الوقائي لمنع تكرار ذلك؟", ph: "أمر تجديد العنوان والإجراء الوقائي..." }
            ],
            keyTitle: "🔑 دليل وإجابات المعلم // السيناريو الثاني",
            keyContent: "<strong>الخطوتان 1 و 2:</strong> 169.254.x.x هو عنوان APIPA (RFC 3927). يثبت سلامة الطبقتين 1 و 2، لكن الجهاز أرسل طلب DHCP ولم يتلق أي رد. خادم الـ DHCP متوقف أو نطاق العناوين ممتلئ بالكامل.<br><strong>الخطوتان 3 و 4:</strong> فحص خادم الـ DHCP. إذا نفدت العناوين، وسّع قناع الشبكة (من /24 إلى /23) أو قلّص مدة تأجير العناوين من 8 أيام إلى 4 ساعات لاسترجاع العناوين غير المستخدمة.<br><strong>الخطوتان 5 و 6:</strong> تشغيل <code>ipconfig /release</code> ثم <code>ipconfig /renew</code>. الإجراء الوقائي: تفعيل تنبيهات تلقائية عند وصول استهلاك نطاق الـ DHCP إلى 80%."
          },
          {
            num: 3,
            head: "المستوى 3: طبقة التطبيق والنقل // DNS وجدار الحماية",
            title: "معضلة خادم الـ DNS",
            tag: "المستوى: متوسط · 200 نقطة",
            tagClass: "cyan",
            situation: "<strong>السيناريو:</strong> أبلغت معلمة قائلة: <em>'الإنترنت معطل تماماً في فصلي!'</em> قمت بفتح موجه الأوامر على جهازها، واستطعت بنجاح تنفيذ <code>ping 8.8.8.8</code> بزمن استجابة 12ms، ولكن عند كتابة <code>ping google.com</code> ظهر الخطأ: <code>\"Ping request could not find host google.com.\"</code>",
            termTitle: "الطرفية الافتراضية // حاسوب المعلمة",
            termSub: "بيئة تشخيص الأوامر المباشرة",
            termInitial: "اضغط على أحد أزرار التشخيص أعلاه لفحص القياسات الرقمية للمنفذ...",
            termBtns: [
              { key: "ping_ip", label: "تشغيل: ping 8.8.8.8" },
              { key: "ping_dns", label: "تشغيل: ping google.com" },
              { key: "nslookup", label: "تشغيل: nslookup google.com" },
              { key: "ipconfig_dns", label: "تشغيل: ipconfig /displaydns" }
            ],
            steps: [
              { label: "[الخطوتان 1 و 2] // تحديد المشكلة وبناء الفرضية", prompt: "ماذا يثبت نجاح أمر ping 8.8.8.8 بالنسبة للطبقات 1 و 2 و 3؟ ما البروتوكول المتعطل عند طلب google.com؟", ph: "حلل ما يثبته نجاح الـ ping وفشله..." },
              { label: "[الخطوتان 3 و 4] // اختبار الفرضية وتنفيذ خطة العمل", prompt: "ما الأمر المخصص لاختبار دقة الـ DNS؟ إذا وُجد عنوان DNS يدوي خاطئ (10.0.0.99)، كيف تصلحه؟", ph: "أمر فحص الـ DNS وكيفية إصلاح الإعدادات..." },
              { label: "[الخطوتان 5 و 6] // التحقق من النظام والتحصين الوقائي", prompt: "ما الأمر الذي يمسح ذاكرة التخزين المؤقت للـ DNS محلياً؟ اكتب نص التوثيق الدقيق للتذكرة.", ph: "أمر مسح الكاش ونص توثيق التذكرة..." }
            ],
            keyTitle: "🔑 دليل وإجابات المعلم // السيناريو الثالث",
            keyContent: "<strong>الخطوتان 1 و 2:</strong> نجاح الاتصال بـ 8.8.8.8 يثبت بنسبة 100% سلامة الكابل والبوابة والراوتر والإنترنت (الطبقات 1-3)! الفشل في الاسم يثبت عطل بروتوكول DNS (المنفذ 53) في الطبقة السابعة.<br><strong>الخطوتان 3 و 4:</strong> الفحص بأمر <code>nslookup google.com</code>. الإصلاح: ضبط خيارات المحول على 'الحصول على عنوان DNS تلقائياً' عبر DHCP أو وضع عناوين معتمدة (1.1.1.1, 8.8.8.8).<br><strong>الخطوتان 5 و 6:</strong> تشغيل <code>ipconfig /flushdns</code>. نص التوثيق: <em>'تم حذف عنوان DNS اليدوي الخاطئ 10.0.0.99 وتفعيل الاكتشاف التلقائي عبر DHCP ومسح كاش الـ DNS. تم التحقق من تصفح المواقع بنجاح.'</em>"
          },
          {
            num: 4,
            head: "المستوى 4: الاستجابة للحوادث // فرز أمني سيبراني",
            title: "تسريب بيانات مشبوه عبر المنفذ 22 (SSH)",
            tag: "المستوى: متقدم · 250 نقطة",
            tagClass: "hard",
            situation: "<strong>السيناريو:</strong> أطلق نظام كشف التسلل (IDS) تنبيهاً حرجاً: محطة العمل 19 (192.168.10.84) في معمل التصميم أنشأت اتصالاً صادراً نشطاً عبر <strong>المنفذ 22 (SSH)</strong> إلى خادم خارجي في بلغاريا (185.220.101.5)، ونقلت أكثر من 3.2 جيجابايت من البيانات المضغوطة.",
            termTitle: "الطرفية الافتراضية // طرفية التحقيق الجنائي",
            termSub: "بيئة تشخيص الأوامر المباشرة",
            termInitial: "اضغط على أحد أزرار التشخيص أعلاه لفحص القياسات الرقمية للمنفذ...",
            termBtns: [
              { key: "netstat", label: "تشغيل: netstat -ano | findstr :22" },
              { key: "tasklist", label: "تشغيل: tasklist /fi \"PID eq 4820\"" },
              { key: "firewall", label: "تشغيل: netsh advfirewall firewall show rule name=all" }
            ],
            steps: [
              { label: "[الخطوتان 1 و 2] // تحديد المشكلة وبناء الفرضية", prompt: "ما هو الإجراء التشغيلي الفوري الواجب اتخاذه أولاً (الخطوة 1)؟ ما البروتوكول العامل على المنفذ 22 وماذا يفعل المهاجم؟", ph: "الإجراء الفوري وفرضية التهديد السيبراني..." },
              { label: "[الخطوتان 3 و 4] // اختبار الفرضية وتنفيذ خطة العمل", prompt: "ما الأمر الذي يربط اتصال الشبكة برقم العملية (PID) الخبيثة؟ كيف تنهي العملية وتلغي استمراريتها؟", ph: "أمر فحص العمليات وخطوات إيقاف التهديد..." },
              { label: "[الخطوتان 5 و 6] // التحقق من النظام والتحصين الوقائي", prompt: "ما قاعدة جدار الحماية الصادرة الواجب تطبيقها لمنع اتصالات SSH غير المصرح بها من أجهزة الطلاب مستقبلاً؟", ph: "قاعدة جدار الحماية وتوثيق الحادثة..." }
            ],
            keyTitle: "🔑 دليل وإجابات المعلم // السيناريو الرابع",
            keyContent: "<strong>الخطوتان 1 و 2:</strong> الإجراء الفوري: عزل الجهاز المصاب عن الشبكة فوراً (فصل الكابل أو تعطيل منفذ المحول) لمنع استمرار التسريب والتحرك الجانبي. المنفذ 22 هو SSH والمهاجم يستخدم نفقاً عكسياً لسرقة البيانات.<br><strong>الخطوتان 3 و 4:</strong> تشغيل <code>netstat -ano | findstr :22</code> لمعرفة رقم العملية (PID 4820)، ثم إنهاؤها بأمر <code>taskkill /PID 4820 /F</code> وفحص مهام الويندوز المجدولة ومفاتيح السجل.<br><strong>الخطوتان 5 و 6:</strong> الإجراء الوقائي: حظر حركة الخروج (Egress) للمنفذ 22 على جدار الحماية لجميع الشبكات باستثناء خوادم الإدارة المصرحة. إجراء فحص جنائي كامل وإعادة تثبيت النظام وتوثيق تقرير الاستجابة للحادثة."
          },
          {
            num: 5,
            head: "المستوى 5: أمن المؤسسات // هجوم على الطبقة الثانية",
            title: "هجوم انتحال ARP (القرين / Doppelgänger)",
            tag: "المستوى: خبير · 300 نقطة",
            tagClass: "hard",
            situation: "<strong>السيناريو:</strong> أبلغ مستخدمو شبكة VLAN 10 عن ظهور تحذيرات شهادات SSL/TLS في المتصفحات (مثل: <em>'الاتصال ليس خاصاً'</em>) وانقطاعات متكررة. قمت بفحص محطة عمل أحد الضحايا واستعرضت جدول الـ ARP.",
            termTitle: "الطرفية الافتراضية // حاسوب الضحية 04",
            termSub: "بيئة تشخيص الأوامر المباشرة",
            termInitial: "اضغط على أحد أزرار التشخيص أعلاه لفحص القياسات الرقمية للمنفذ...",
            termBtns: [
              { key: "arp", label: "تشغيل: arp -a" },
              { key: "tracert", label: "تشغيل: tracert -d 8.8.8.8" },
              { key: "switch_mac", label: "تشغيل: show mac address-table | include b827" }
            ],
            steps: [
              { label: "[الخطوتان 1 و 2] // تحديد المشكلة وبناء الفرضية", prompt: "انظر إلى جدول <code>arp -a</code>. لماذا يشترك عنوانا IP مختلفان في نفس عنوان الـ MAC؟ سمّ الهجوم بدقة.", ph: "اشرح شذوذ جدول ARP وسمّ الهجوم السيبراني..." },
              { label: "[الخطوتان 3 و 4] // اختبار الفرضية وتنفيذ خطة العمل", prompt: "كيف تتبع عنوان الـ MAC المهاجم لمعرفة منفذ المحول الفيزيائي المتصل به؟ ما الإجراء الفوري لإيقاف الهجوم؟", ph: "أمر تتبع الماك على المحول وإجراء الإيقاف..." },
              { label: "[الخطوتان 5 و 6] // التحقق من النظام والتحصين الوقائي", prompt: "ما الميزتان الأمنيتان في محولات سيسكو (الخطوة 5) اللتان تحظران انتحال ARP وخوادم DHCP الوهمية نهائياً؟", ph: "ميزات حماية المحولات (DAI / DHCP Snooping)..." }
            ],
            keyTitle: "🔑 دليل وإجابات المعلم // السيناريو الخامس",
            keyContent: "<strong>الخطوتان 1 و 2:</strong> هجوم انتحال وتسميم جدول ARP (هجوم الوسيط Man-in-the-Middle). يقوم جهاز مهاجم بإرسال ردود ARP كاذبة مدعياً أن عنوان البوابة (192.168.1.1) يخص عنوان الماك التابع له (b8-27-eb-93-11-aa) لاعتراض وتفكيك تشفير بيانات المستخدمين.<br><strong>الخطوتان 3 و 4:</strong> تشغيل <code>show mac address-table | include b827</code> على المحول الرئيسي لمعرفة المنفذ، ثم تنفيذ أمر <code>shutdown</code> على المنفذ لفصل المهاجم فوراً.<br><strong>الخطوتان 5 و 6:</strong> تفعيل ميزتي <strong>Dynamic ARP Inspection (DAI)</strong> و <strong>DHCP Snooping</strong> على جميع محولات الوصول مع ميزة Port Security. مسح كاش الـ ARP بأمر <code>netsh interface ip delete arpcache</code> وتوثيق الحادثة."
          }
        ]
      },

      uk: {
        school: "Професійно-технічний центр імені А.В. Бітті · Мережева інженерія та кібербезпека",
        prtTitle: "Практична робота: Розділяй і володарюй // 6-етапна модель CompTIA",
        topBrand: "● МЕРЕЖА БІТТІ // КІБЕРБЕЗПЕКА ТА МЕРЕЖЕВА ІНЖЕНЕРІЯ",
        mainTitle: "Практичний простір: Розділяй і володарюй",
        subTitle: "6-етапна модель усунення несправностей CompTIA",
        btnPrint: "Експорт / Друк практичної роботи (PDF)",
        btnKeyShow: "Показати відповіді та критерії для викладача",
        btnKeyHide: "Сховати відповіді викладача",
        btnPres: "Відкрити презентацію уроку →",
        footer: "КІНЕЦЬ ПЕРЕДАЧІ ТА ЗВІТУ",
        studId: {
          header: "ДАНІ СТУДЕНТА ТА КРИТЕРІЇ ОЦІНЮВАННЯ",
          nameLabel: "ІМ'Я ТА ПРІЗВИЩЕ СТУДЕНТА",
          dateLabel: "ДАТА",
          periodLabel: "ГРУПА / ЗМІНА",
          namePh: "наприклад: Олексій Шевченко",
          periodPh: "наприклад: Ранкова зміна 1",
          missionTitle: "ЗАВДАННЯ ПРАКТИКУМУ:",
          missionText: "Для кожного зі сценаріїв нижче застосуйте офіційну <strong>6-етапну модель усунення несправностей CompTIA</strong> за методологією <strong>бінарного пошуку (Розділяй і володарюй)</strong>. Використовуйте віртуальні консолі для діагностики та фіксуйте план дій у полях нижче.",
          missionFormula: "[1] Ідентифікація → [2] Теорія → [3] Тест → [4] План та впровадження → [5] Перевірка та превентивні дії → [6] Документування."
        },
        scenarios: [
          {
            num: 1,
            head: "РІВЕНЬ 1: ФІЗИЧНИЙ РІВЕНЬ // РІВНІ 1 ТА 2",
            title: "Мовчазний роз'єм",
            tag: "СКЛАДНІСТЬ: ПОЧАТКІВЕЦЬ · 100 БАЛІВ",
            tagClass: "easy",
            situation: "<strong>СИТУАЦІЯ:</strong> Студент розвів кабель Cat6 UTP у патч-панель (порт 14) та підключив розетку в ауд. 204. При підключенні тестового ПК робочим патч-кордом індикатори порту не світяться, а Windows повідомляє: <code>\"Мережевий кабель не підключено.\"</code>",
            termTitle: "ВІРТУАЛЬНИЙ ТЕРМІНАЛ // ПК-АУДИТОРІЯ 204",
            termSub: "ДІАГНОСТИЧНИЙ СТЕНД КОНСОЛІ",
            termInitial: "Натисніть кнопку діагностики вгорі для аналізу телеметрії...",
            termBtns: [
              { key: "ipconfig", label: "виконати: ipconfig /all" },
              { key: "link", label: "виконати: Test-NetConnection -InterfaceIndex 3" },
              { key: "tester", label: "виконати: check_cable_tester_output" }
            ],
            steps: [
              { label: "[ЕТАПИ 1 ТА 2] // ІДЕНТИФІКАЦІЯ ПРОБЛЕМИ ТА ТЕОРІЯ", prompt: "Які фізичні компоненти треба перевірити насамперед? Назвіть 2 ймовірні причини збою на Рівні 1.", ph: "Опишіть ідентифікацію та гіпотезу..." },
              { label: "[ЕТАПИ 3 ТА 4] // ТЕСТУВАННЯ ТЕОРІЇ ТА ПЛАН ДІЙ", prompt: "Який інструмент перевірить кабель? Якщо розпіновка показує переплутані жили 1 і 2, які кроки відновлення?", ph: "Вкажіть прилад тестування та план ремонту..." },
              { label: "[ЕТАПИ 5 ТА 6] // ПЕРЕВІРКА ТА ДОКУМЕНТУВАННЯ У ТІКЕТІ", prompt: "Як перевірити повну працездатність (Етап 5) та який текст звіту записати в заявку (Етап 6)?", ph: "Опишіть тест перевірки та запис у заявку..." }
            ],
            keyTitle: "🔑 ВІДПОВІДІ ТА КРИТЕРІЇ ДЛЯ ВИКЛАДАЧА // СЦЕНАРІЙ 1",
            keyContent: "<strong>Етапи 1 і 2:</strong> Перевірити індикатори NIC, патч-корд з обох боків, стан порту комутатора. Теорії: Переплутані жили в розетці (Miswire), пошкодження жили або вимкнений порт.<br><strong>Етапи 3 і 4:</strong> Використати цифровий кабельний тестер (Wiremapper). Якщо жили 1 і 2 перехрещені, перезакрити розетку за стандартом TIA/EIA-568B за допомогою ударного інструменту 110.<br><strong>Етапи 5 і 6:</strong> Переконатися, що лінк горить зеленим на 1Gbps, ПК отримав IP через DHCP і пінгує шлюз. Запис у тікет: <em>'Перероблено розетку ауд. 204 (порт 14) за стандартом T-568B для усунення перехрещення жил 1-2. Перевірено лінк 1Gbps та DHCP.'</em>"
          },
          {
            num: 2,
            head: "РІВЕНЬ 2: МЕРЕЖЕВИЙ РІВЕНЬ // L3 (DHCP ТА IPV4)",
            title: "Аномалія APIPA (169.254)",
            tag: "СКЛАДНІСТЬ: ПОЧАТКІВЕЦЬ · 150 БАЛІВ",
            tagClass: "easy",
            situation: "<strong>СИТУАЦІЯ:</strong> Усі 12 комп'ютерів у лабораторії B раптово втратили інтернет. Індикатори лінку на ПК та світчі світяться зеленим. Команда <code>ipconfig</code> на ПК-01 показує адресу <code>169.254.88.204</code>, маску <code>255.255.0.0</code> та порожній шлюз.",
            termTitle: "ВІРТУАЛЬНИЙ ТЕРМІНАЛ // ЛАБ-B-ПК01",
            termSub: "ДІАГНОСТИЧНИЙ СТЕНД КОНСОЛІ",
            termInitial: "Натисніть кнопку діагностики вгорі для аналізу телеметрії...",
            termBtns: [
              { key: "ipconfig", label: "виконати: ipconfig /all" },
              { key: "ping_loop", label: "виконати: ping 127.0.0.1" },
              { key: "renew", label: "виконати: ipconfig /renew" },
              { key: "dhcp_status", label: "виконати: Get-DhcpServerv4Scope -ComputerName 'DC01'" }
            ],
            steps: [
              { label: "[ЕТАПИ 1 ТА 2] // ІДЕНТИФІКАЦІЯ ПРОБЛЕМИ ТА ТЕОРІЯ", prompt: "Що означає адреса 169.254.x.x? Якщо фізичний лінк є, яка мережева служба дала збій?", ph: "Поясніть статус APIPA та несправну службу..." },
              { label: "[ЕТАПИ 3 ТА 4] // ТЕСТУВАННЯ ТЕОРІЇ ТА ПЛАН ДІЙ", prompt: "Як перевірити службу DHCP? Якщо пул адрес заповнено на 100%, який план вирішення?", ph: "Команда діагностики та спосіб вирішення з пулом..." },
              { label: "[ЕТАПИ 5 ТА 6] // ПЕРЕВІРКА ТА ПРЕВЕНТИВНІ ЗАХОДИ", prompt: "Яка команда змушує ПК запросити нову IP-адресу? Який превентивний захід попередить рецидив?", ph: "Команда оновлення IP та превентивні дії..." }
            ],
            keyTitle: "🔑 ВІДПОВІДІ ТА КРИТЕРІЇ ДЛЯ ВИКЛАДАЧА // СЦЕНАРІЙ 2",
            keyContent: "<strong>Етапи 1 і 2:</strong> 169.254.x.x — це адресація APIPA (RFC 3927). Вона доводить справність L1 та L2, але ПК не отримав відповіді на DHCPDISCOVER. Служба DHCP зупинилася або пул адрес вичерпано.<br><strong>Етапи 3 і 4:</strong> Перевірити сервер DHCP. Якщо пул вичерпано, розширити підмережу (з /24 до /23) або зменшити час оренди з 8 днів до 4 годин для повернення неактивних адрес.<br><strong>Етапи 5 і 6:</strong> Виконати <code>ipconfig /release</code> та <code>ipconfig /renew</code>. Превентивна дія: налаштувати автоматичні сповіщення при досягненні 80% ємності пулу DHCP."
          },
          {
            num: 3,
            head: "РІВЕНЬ 3: ТРАНСПОРТНИЙ ТА ПРИКЛАДНИЙ РІВНІ // DNS ТА ФАЄРВОЛ",
            title: "Дилема DNS",
            tag: "СКЛАДНІСТЬ: СЕРЕДНЯ · 200 БАЛІВ",
            tagClass: "cyan",
            situation: "<strong>СИТУАЦІЯ:</strong> Викладач повідомляє: <em>'У моєму класі зовсім не працює інтернет!'</em> У консолі на її ПК команда <code>ping 8.8.8.8</code> успішно проходить з часом 12ms, але команда <code>ping google.com</code> видає помилку: <code>\"Ping request could not find host google.com.\"</code>",
            termTitle: "ВІРТУАЛЬНИЙ ТЕРМІНАЛ // ПК-ВИКЛАДАЧА",
            termSub: "ДІАГНОСТИЧНИЙ СТЕНД КОНСОЛІ",
            termInitial: "Натисніть кнопку діагностики вгорі для аналізу телеметрії...",
            termBtns: [
              { key: "ping_ip", label: "виконати: ping 8.8.8.8" },
              { key: "ping_dns", label: "виконати: ping google.com" },
              { key: "nslookup", label: "виконати: nslookup google.com" },
              { key: "ipconfig_dns", label: "виконати: ipconfig /displaydns" }
            ],
            steps: [
              { label: "[ЕТАПИ 1 ТА 2] // ІДЕНТИФІКАЦІЯ ПРОБЛЕМИ ТА ТЕОРІЯ", prompt: "Що доводить успішний пінг 8.8.8.8 для рівнів 1, 2 і 3? Який протокол не працює для google.com?", ph: "Проаналізуйте результат успішного та невдалого пінгу..." },
              { label: "[ЕТАПИ 3 ТА 4] // ТЕСТУВАННЯ ТЕОРІЇ ТА ПЛАН ДІЙ", prompt: "Яка команда тестує розпізнавання імен DNS? Якщо адаптер мав помилковий DNS (10.0.0.99), як це виправити?", ph: "Команда перевірки DNS та виправлення конфігурації..." },
              { label: "[ЕТАПИ 5 ТА 6] // ПЕРЕВІРКА ТА ПРЕВЕНТИВНІ ЗАХОДИ", prompt: "Яка команда очищує локальний кеш DNS? Напишіть точний текст закриття заявки.", ph: "Команда очищення кешу та текст звіту..." }
            ],
            keyTitle: "🔑 ВІДПОВІДІ ТА КРИТЕРІЇ ДЛЯ ВИКЛАДАЧА // СЦЕНАРІЙ 3",
            keyContent: "<strong>Етапи 1 і 2:</strong> Успішний пінг до 8.8.8.8 на 100% підтверджує справність фізичного кабелю, шлюзу, NAT та інтернет-каналу (L1-L3)! Збій на доменному імені доводить несправність DNS (порт 53) на 7 рівні.<br><strong>Етапи 3 і 4:</strong> Тест командою <code>nslookup google.com</code>. Виправлення: Увімкнути 'Отримувати адресу DNS-сервера автоматично' через DHCP або прописати корпоративні DNS (1.1.1.1, 8.8.8.8).<br><strong>Етапи 5 і 6:</strong> Виконати <code>ipconfig /flushdns</code>. Звіт: <em>'Видалено некоректний статичний DNS 10.0.0.99, увімкнено автоотримання через DHCP та очищено кеш DNS-резолвера. Доступ до сайтів відновлено.'</em>"
          },
          {
            num: 4,
            head: "РІВЕНЬ 4: РЕАГУВАННЯ НА ІНЦИДЕНТИ // КІБЕРБЕЗПЕКА",
            title: "Підозріла ексфільтрація через SSH (Порт 22)",
            tag: "СКЛАДНІСТЬ: ПРОСУНУТИЙ · 250 БАЛІВ",
            tagClass: "hard",
            situation: "<strong>СИТУАЦІЯ:</strong> Система IDS зафіксувала критичний алерт: ПК-19 (192.168.10.84) у лабораторії САПР встановив активне вихідне з'єднання на <strong>Порт 22 (SSH)</strong> до закордонного сервера в Болгарії (185.220.101.5), передавши понад 3.2 ГБ стиснених даних.",
            termTitle: "ВІРТУАЛЬНИЙ ТЕРМІНАЛ // ФОРЕНЗИК-КОНСОЛЬ ПК-19",
            termSub: "ДІАГНОСТИЧНИЙ СТЕНД КОНСОЛІ",
            termInitial: "Натисніть кнопку діагностики вгорі для аналізу телеметрії...",
            termBtns: [
              { key: "netstat", label: "виконати: netstat -ano | findstr :22" },
              { key: "tasklist", label: "виконати: tasklist /fi \"PID eq 4820\"" },
              { key: "firewall", label: "виконати: netsh advfirewall firewall show rule name=all" }
            ],
            steps: [
              { label: "[ЕТАПИ 1 ТА 2] // ІДЕНТИФІКАЦІЯ ПРОБЛЕМИ ТА ТЕОРІЯ", prompt: "Яка ваша НЕВІДКЛАДНА дія (Етап 1)? Який протокол працює на порті 22 та що робить зловмисник?", ph: "Першочергова дія та аналіз загрози..." },
              { label: "[ЕТАПИ 3 ТА 4] // ТЕСТУВАННЯ ТЕОРІЇ ТА ПЛАН ДІЙ", prompt: "Яка команда пов'язує мережеве з'єднання з номером процесу (PID)? Як знешкодити шкідливий процес?", ph: "Команда виявлення PID та кроки нейтралізації..." },
              { label: "[ЕТАПИ 5 ТА 6] // ПЕРЕВІРКА ТА ПРЕВЕНТИВНІ ЗАХОДИ", prompt: "Яке правило вихідної фільтрації фаєрволу попередить несанкціонований SSH з комп'ютерів студентів?", ph: "Політика фаєрволу та документація інциденту..." }
            ],
            keyTitle: "🔑 ВІДПОВІДІ ТА КРИТЕРІЇ ДЛЯ ВИКЛАДАЧА // СЦЕНАРІЙ 4",
            keyContent: "<strong>Етапи 1 і 2:</strong> Невідкладна дія: Ізолювати хост від мережі (відключити кабель або порт світча) для запобігання витоку та бічного переміщення атаки. Порт 22 — це SSH, через який організовано реверс-тунель.<br><strong>Етапи 3 і 4:</strong> Виконати <code>netstat -ano | findstr :22</code> для визначення PID (PID 4820), завершити процес через <code>taskkill /PID 4820 /F</code> та перевірити планувальник завдань.<br><strong>Етапи 5 і 6:</strong> Заблокувати вихідний порт 22 на прикордонному фаєрволі для студентських підмереж. Провести сканування, перевстановити чистий образ ОС та скласти звіт Incident Response."
          },
          {
            num: 5,
            head: "РІВЕНЬ 5: КОРПОРАТИВНА БЕЗПЕКА // АТАКА РІВНЯ L2",
            title: "Атака ARP-спуфінгу (Двійник / Doppelgänger)",
            tag: "СКЛАДНІСТЬ: ЕКСПЕРТ · 300 БАЛІВ",
            tagClass: "hard",
            situation: "<strong>СИТУАЦІЯ:</strong> Користувачі VLAN 10 скаржаться на попередження сертифікатів SSL/TLS у браузерах (<em>'Підключення не конфіденційне'</em>) та постійні обриви зв'язку. Ви перевіряєте таблицю ARP на комп'ютері користувача.",
            termTitle: "ВІРТУАЛЬНИЙ ТЕРМІНАЛ // ПК-ЖЕРТВИ-04",
            termSub: "ДІАГНОСТИЧНИЙ СТЕНД КОНСОЛІ",
            termInitial: "Натисніть кнопку діагностики вгорі для аналізу телеметрії...",
            termBtns: [
              { key: "arp", label: "виконати: arp -a" },
              { key: "tracert", label: "виконати: tracert -d 8.8.8.8" },
              { key: "switch_mac", label: "виконати: show mac address-table | include b827" }
            ],
            steps: [
              { label: "[ЕТАПИ 1 ТА 2] // ІДЕНТИФІКАЦІЯ ПРОБЛЕМИ ТА ТЕОРІЯ", prompt: "Подивіться на таблицю <code>arp -a</code>. Чому дві різні IP-адреси мають однаковий MAC? Назвіть атаку.", ph: "Поясніть аномалію ARP та вкажіть назву атаки..." },
              { label: "[ЕТАПИ 3 ТА 4] // ТЕСТУВАННЯ ТЕОРІЇ ТА ПЛАН ДІЙ", prompt: "Як виявити фізичний порт комутатора за MAC-адресою атакуючого? Що негайно зупинить атаку?", ph: "Команда пошуку на комутаторі та ізоляція..." },
              { label: "[ЕТАПИ 5 ТА 6] // ПЕРЕВІРКА ТА ПРЕВЕНТИВНІ ЗАХОДИ", prompt: "Які дві технології комутаторів Cisco (Етап 5) назавжди блокують отруєння ARP та фіктивні сервери DHCP?", ph: "Функції безпеки комутаторів (DAI / DHCP Snooping)..." }
            ],
            keyTitle: "🔑 ВІДПОВІДІ ТА КРИТЕРІЇ ДЛЯ ВИКЛАДАЧА // СЦЕНАРІЙ 5",
            keyContent: "<strong>Етапи 1 і 2:</strong> Отруєння кешу ARP / ARP Spoofing (Атака Man-in-the-Middle). Шкідливий пристрій генерує фіктивні ARP-відповіді, заявляючи, що IP шлюзу (192.168.1.1) відповідає його власному MAC (b8-27-eb-93-11-aa) для перехоплення та розшифрування трафіку.<br><strong>Етапи 3 і 4:</strong> Виконати <code>show mac address-table | include b827</code> на комутаторі та вимкнути порт командою <code>shutdown</code>.<br><strong>Етапи 5 і 6:</strong> Увімкнути <strong>Dynamic ARP Inspection (DAI)</strong> та <strong>DHCP Snooping</strong> на комутаторах доступу разом з Port Security. Очистити кеш ARP клієнта: <code>netsh interface ip delete arpcache</code>. Зафіксувати інцидент."
          }
        ]
      }
    };

    const TERM_DATA = {
      1: {
        'ipconfig': "Windows IP Configuration\n\nEthernet adapter Ethernet0:\n   Media State . . . . . . . . . . . : Media disconnected\n   Description . . . . . . . . . . . : Intel(R) I211 Gigabit Network Connection",
        'link': "Test-NetConnection -InterfaceIndex 3\n\nInterfaceAlias               : Ethernet0\nInterfaceIndex               : 3\nOperationalStatus            : Down\nMediaConnectionState         : Disconnected",
        'tester': "HARDWARE CABLE TESTER REPORT (Klein Tools Scout Pro 3):\n[PASS] Length: 42 meters (Cat6 UTP)\n[FAIL] WIREMAP ANOMALY:\n   Tester Pin 1 -> Remote Pin 2\n   Tester Pin 2 -> Remote Pin 1\n   Pins 3, 4, 5, 6, 7, 8 -> Straight Through (OK)\nRESULT: MISWIRE (Reversed Pair 1-2 on Room 204 Keystone Jack)"
      },
      2: {
        'ipconfig': "Windows IP Configuration\n\nEthernet adapter Ethernet0:\n   IPv4 Address. . . . . . . . . . . : 169.254.88.204\n   Subnet Mask . . . . . . . . . . . : 255.255.0.0\n   Default Gateway . . . . . . . . . : \n   DHCP Enabled. . . . . . . . . . . : Yes",
        'ping_loop': "Pinging 127.0.0.1 with 32 bytes of data:\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\n[+] TCP/IP Software Stack is HEALTHY.",
        'renew': "C:\\> ipconfig /renew\n\nAn error occurred while renewing interface Ethernet0 : unable to contact your DHCP server. Request has timed out.",
        'dhcp_status': "PS C:\\> Get-DhcpServerv4Scope -ComputerName 'DC01'\n\nScopeId         SubnetMask      Name           State    StartRange      EndRange        LeasesInUse  AvailableLeases\n-------         ----------      ----           -----    ----------      --------        -----------  ---------------\n192.168.10.0    255.255.255.0   Lab_B_VLAN     Active   192.168.10.50   192.168.10.254  204 (100%)   0 (0% EXHAUSTED)"
      },
      3: {
        'ping_ip': "Pinging 8.8.8.8 with 32 bytes of data:\nReply from 8.8.8.8: bytes=32 time=12ms TTL=117\n[+] WAN IP Routing and Gateway are 100% OPERATIONAL.",
        'ping_dns': "C:\\> ping google.com\nPing request could not find host google.com. Please check the name and try again.",
        'nslookup': "C:\\> nslookup google.com\nServer:  UnKnown\nAddress:  10.0.0.99\n\n*** DNS request to 10.0.0.99 timed out.\n*** Request to UnKnown timed-out after 2 seconds.\n*** DNS FAILURE: Host unreachable.",
        'ipconfig_dns': "Windows IP Configuration\n\n   DNS Servers . . . . . . . . . . . : 10.0.0.99 (STALE / INVALID STATIC OVERRIDE)\n   NetBIOS over Tcpip. . . . . . . . : Enabled"
      },
      4: {
        'netstat': "Active Connections\n  Proto  Local Address          Foreign Address        State           PID\n  TCP    192.168.10.84:54210    185.220.101.5:22       ESTABLISHED     4820",
        'tasklist': "Image Name                     PID Session Name        Session#    Mem Usage\n========================= ======== ================ =========== ============\nputty_persist.exe             4820 Console                    1     14,240 K",
        'firewall': "Rule Name: Rogue Outbound SSH Rule\n----------------------------------------------------------------------\nEnabled: Yes\nDirection: Out\nAction: Allow\nProtocol: TCP\nRemotePort: 22"
      },
      5: {
        'arp': "Interface: 192.168.1.105 --- 0x3\n  Internet Address      Physical Address      Type\n  192.168.1.1           b8-27-eb-93-11-aa     dynamic   <-- (DEFAULT GATEWAY)\n  192.168.1.55          b8-27-eb-93-11-aa     dynamic   <-- (STUDENT LAPTOP - DUPLICATE MAC!)",
        'tracert': "Tracing route to 8.8.8.8 over a maximum of 30 hops:\n  1    <1 ms    <1 ms    <1 ms  192.168.1.55 (MITM PROXY INTERCEPT!)\n  2     1 ms     1 ms     1 ms  192.168.1.1",
        'switch_mac': "Core-Switch-01# show mac address-table | include b827\nVLAN    Mac Address       Type       Ports\n----    -----------       ----       -----\n10      b827.eb93.11aa    DYNAMIC    Gi0/12  (Room 104 Drop 6)"
      }
    };

    let currentLang = 'en';

    function renderActivity() {
      const db = ACT_DB[currentLang] || ACT_DB.en;
      
      // Update headers and titles
      document.getElementById('prt-school').textContent = db.school;
      document.getElementById('prt-title').textContent = db.prtTitle;
      document.getElementById('act-top-brand').innerHTML = `<span class="dot">●</span> ${db.topBrand.replace('● ', '')}`;
      document.getElementById('act-main-title').textContent = db.mainTitle;
      document.getElementById('act-sub-title').textContent = db.subTitle;
      document.getElementById('btn-txt-print').textContent = db.btnPrint;
      document.getElementById('btn-txt-pres').textContent = db.btnPres;
      document.getElementById('act-footer').textContent = db.footer;

      const isKeyVisible = document.querySelectorAll('.teacher-key-box.visible').length > 0;
      document.getElementById('key-label').textContent = isKeyVisible ? db.btnKeyHide : db.btnKeyShow;

      const mainEl = document.getElementById('activity-main');

      // 1. Student ID Panel
      let html = `
        <div class="panel">
          <div class="panel-head">
            <span class="lights"><span class="r"></span><span class="a"></span><span class="g"></span> auth.log</span>
            <span>${db.studId.header}</span>
          </div>
          <div class="panel-body">
            <div class="name-block">
              <div class="name-field">
                <label>${db.studId.nameLabel}</label>
                <input id="stud-name" type="text" class="student-input" placeholder="${db.studId.namePh}">
              </div>
              <div class="name-field">
                <label>${db.studId.dateLabel}</label>
                <input id="stud-date" type="date" class="student-input">
              </div>
              <div class="name-field">
                <label>${db.studId.periodLabel}</label>
                <input id="stud-period" type="text" class="student-input" placeholder="${db.studId.periodPh}">
              </div>
            </div>

            <div style="font-size:0.88rem; color:var(--text-muted); border: 1px dashed var(--line); padding: 1.2rem; border-radius: 6px; line-height: 1.7; background: rgba(0,0,0,0.4);">
              <strong style="color:var(--green);">${db.studId.missionTitle}</strong> ${db.studId.missionText}
              <div style="margin-top: 0.6rem; color: var(--cyan); font-size: 0.8rem;">
                ${db.studId.missionFormula}
              </div>
            </div>
          </div>
        </div>
      `;

      // 2. Render all 5 Scenarios
      db.scenarios.forEach((sc, sIdx) => {
        const sNum = sc.num;
        const btnGroupHtml = sc.termBtns.map(b => `
          <button class="term-btn" onclick="runTerm(${sNum}, '${b.key}')">${b.label}</button>
        `).join('');

        const stepsHtml = sc.steps.map((st, stepIdx) => {
          const colClass = stepIdx === 1 ? ' cyan' : stepIdx === 2 ? ' amber' : '';
          const qId = `q${sNum}-${stepIdx + 1}`;
          return `
            <div class="step-block">
              <div class="step-label${colClass}">${st.label}</div>
              <div class="step-prompt">${st.prompt}</div>
              <input id="${qId}" type="text" class="student-input" placeholder="${st.ph}">
            </div>
          `;
        }).join('');

        html += `
          <div class="panel" id="sec-scen-${sNum}">
            <div class="panel-head">
              <span class="lights"><span class="r"></span><span class="a"></span><span class="g"></span> scenario_0${sNum}.log</span>
              <span>${sc.head}</span>
            </div>
            <div class="panel-body">
              <div class="scenario-title">
                <span>${sc.title}</span>
                <span class="tag ${sc.tagClass}">${sc.tag}</span>
              </div>
              
              <div class="situation">
                ${sc.situation}
              </div>

              <div class="terminal-sim">
                <div class="term-header">
                  <span>${sc.termTitle}</span>
                  <span>${sc.termSub}</span>
                </div>
                <div class="term-btn-group">
                  ${btnGroupHtml}
                </div>
                <div id="term-out-${sNum}" class="term-output">${sc.termInitial}</div>
              </div>
              
              ${stepsHtml}

              <div class="teacher-key-box${isKeyVisible ? ' visible' : ''}" id="key-${sNum}">
                <div class="teacher-key-title">${sc.keyTitle}</div>
                ${sc.keyContent}
              </div>
            </div>
          </div>
        `;
      });

      mainEl.innerHTML = html;

      // Restore values from localStorage
      restoreFormValues();
    }

    function runTerm(scenNum, cmdKey) {
      const outputElem = document.getElementById(`term-out-${scenNum}`);
      if (TERM_DATA[scenNum] && TERM_DATA[scenNum][cmdKey]) {
        outputElem.textContent = TERM_DATA[scenNum][cmdKey];
      }
    }

    function toggleAnswerKey() {
      const db = ACT_DB[currentLang] || ACT_DB.en;
      const keyBoxes = document.querySelectorAll('.teacher-key-box');
      const isVisible = keyBoxes.length > 0 && keyBoxes[0].classList.contains('visible');
      keyBoxes.forEach(b => b.classList.toggle('visible', !isVisible));
      document.getElementById('key-label').textContent = isVisible ? db.btnKeyShow : db.btnKeyHide;
    }

    const INPUT_IDS = [
      'stud-name', 'stud-date', 'stud-period',
      'q1-1', 'q1-2', 'q1-3',
      'q2-1', 'q2-2', 'q2-3',
      'q3-1', 'q3-2', 'q3-3',
      'q4-1', 'q4-2', 'q4-3',
      'q5-1', 'q5-2', 'q5-3'
    ];

    function restoreFormValues() {
      INPUT_IDS.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          const saved = localStorage.getItem(`trouble_${id}`);
          if (saved) el.value = saved;
          el.addEventListener('input', () => {
            localStorage.setItem(`trouble_${id}`, el.value);
          });
        }
      });

      const dateInput = document.getElementById('stud-date');
      if (dateInput && !dateInput.value) {
        dateInput.value = new Date().toISOString().split('T')[0];
      }
    }

    function setLanguage(lang) {
      currentLang = lang;
      document.documentElement.lang = lang;
      document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
      localStorage.setItem('activity_lang', lang);

      document.querySelectorAll('#lang-en, #lang-ar, #lang-uk').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`lang-${lang}`);
      if (activeBtn) activeBtn.classList.add('active');

      renderActivity();
    }

    const savedLang = localStorage.getItem('activity_lang') || 'en';
    setLanguage(savedLang);

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('key') === 'true') {
      toggleAnswerKey();
    }
  </script>
</body>
</html>
"""

with open(activity_html_path, "w", encoding="utf-8") as f:
    f.write(activity_py)

print(f"Generated activity.html -> {activity_html_path}")

# ==============================================================================
# 3. GENERATE INDEX.HTML WITH FULL DYNAMIC MULTILINGUAL ENGINE
# ==============================================================================
index_html_path = os.path.join(TARGET_DIR, "index.html")

index_py = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Beattie-Net // CompTIA 6-Step Troubleshooting Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #040608;
      --panel: #090e13;
      --panel-elevated: #101720;
      --line: #1c2b26;
      --green: #39ff9e;
      --cyan: #38bdf8;
      --amber: #ffb454;
      --text: #e2f4ea;
      --text-muted: #829a90;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'JetBrains Mono', monospace;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      background-image: linear-gradient(rgba(57,255,158,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(57,255,158,0.04) 1px, transparent 1px);
      background-size: 36px 36px;
    }
    :root:lang(ar) {
      font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif;
    }
    [dir="rtl"] { text-align: start; }
    .hub-card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 2.5rem 3rem;
      max-width: 900px;
      width: 100%;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8);
      position: relative;
    }
    .top-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .badge {
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--green);
      background: rgba(57,255,158,0.08);
      border: 1px solid var(--green);
      padding: 0.3rem 0.8rem;
      border-radius: 4px;
    }
    .lang-btns {
      display: flex;
      gap: 0.3rem;
      background: var(--panel-elevated);
      border: 1px solid var(--line);
      padding: 2px;
      border-radius: 4px;
    }
    .lang-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: inherit;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.25rem 0.6rem;
      border-radius: 3px;
      cursor: pointer;
    }
    .lang-btn.active {
      background: rgba(57,255,158,0.15);
      color: var(--green);
    }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2.2rem;
      color: #fff;
      margin-bottom: 0.5rem;
    }
    p { color: var(--text-muted); font-size: 0.92rem; line-height: 1.6; margin-bottom: 2rem; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
    .nav-box {
      background: var(--panel-elevated);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 1.5rem;
      text-decoration: none;
      color: var(--text);
      display: flex;
      flex-direction: column;
      transition: all 0.2s ease;
    }
    .nav-box:hover {
      border-color: var(--green);
      transform: translateY(-2px);
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .nav-box-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.15rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 0.4rem;
    }
    .nav-box-desc { font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; }
    .nav-box-tag { margin-top: auto; padding-top: 1rem; font-size: 0.75rem; color: var(--green); font-weight: 700; }
  </style>
</head>
<body>
  <div class="hub-card">
    <div class="top-row">
      <div class="badge" id="hub-badge">CTE CURRICULUM // MR. LINGSCH-BEATTIE</div>
      <div class="lang-btns">
        <button id="l-en" class="lang-btn active" onclick="setLang('en')">EN</button>
        <button id="l-ar" class="lang-btn" onclick="setLang('ar')">عربي</button>
        <button id="l-uk" class="lang-btn" onclick="setLang('uk')">УКР</button>
      </div>
    </div>
    
    <h1 id="hub-title">Divide &amp; Conquer Troubleshooting Hub</h1>
    <p id="hub-desc">A.W. Beattie Career Center · Network Engineering &amp; Cybersecurity. Master the CompTIA 6-Step Troubleshooting Framework &amp; Binary Search Logic.</p>

    <div class="grid">
      <a href="presentation.html" class="nav-box" style="border-left: 4px solid var(--green);">
        <div class="nav-box-title" id="card1-title">📺 Slide Deck Presentation</div>
        <div class="nav-box-desc" id="card1-desc">Interactive 15-slide master lesson with live Midpoint Sandbox, presenter teaching notes, and keyboard controls.</div>
        <div class="nav-box-tag" id="card1-tag">Launch Slides (HTML) →</div>
      </a>

      <a href="activity.html" class="nav-box" style="border-left: 4px solid var(--cyan);">
        <div class="nav-box-title" id="card2-title" style="color:var(--cyan);">⚡ Interactive Lab Activity</div>
        <div class="nav-box-desc" id="card2-desc">5 progressive troubleshooting tiers, interactive CLI terminal emulator, auto-saving forms, and printable worksheet PDF export.</div>
        <div class="nav-box-tag" id="card2-tag" style="color:var(--cyan);">Open Student Workbench →</div>
      </a>

      <a href="activity.html?key=true" class="nav-box" style="border-left: 4px solid var(--amber);">
        <div class="nav-box-title" id="card3-title" style="color:var(--amber);">🔑 Teacher Answer Key &amp; Rubric</div>
        <div class="nav-box-desc" id="card3-desc">Instructor review mode displaying complete answers, model flowchart logic, and grading criteria for all 5 scenarios.</div>
        <div class="nav-box-tag" id="card3-tag" style="color:var(--amber);">Open Teacher Rubric →</div>
      </a>

      <a href="Divide_and_Conquer_Mastery.pptx" download class="nav-box" style="border-left: 4px solid #94a3b8;">
        <div class="nav-box-title" id="card4-title">📥 Native PowerPoint (.PPTX)</div>
        <div class="nav-box-desc" id="card4-desc">16:9 widescreen presentation deck ready for classroom projectors and offline PowerPoint presentations.</div>
        <div class="nav-box-tag" id="card4-tag" style="color:#fff;">Download PPTX File →</div>
      </a>
    </div>
  </div>

  <script>
    const HUB_DB = {
      en: {
        badge: "CTE CURRICULUM // MR. LINGSCH-BEATTIE",
        title: "Divide & Conquer Troubleshooting Hub",
        desc: "A.W. Beattie Career Center · Network Engineering & Cybersecurity. Master the CompTIA 6-Step Troubleshooting Framework & Binary Search Logic.",
        c1: { title: "📺 Slide Deck Presentation", desc: "Interactive 15-slide master lesson with live Midpoint Sandbox, presenter teaching notes, and keyboard controls.", tag: "Launch Slides (HTML) →" },
        c2: { title: "⚡ Interactive Lab Activity", desc: "5 progressive troubleshooting tiers, interactive CLI terminal emulator, auto-saving forms, and printable worksheet PDF export.", tag: "Open Student Workbench →" },
        c3: { title: "🔑 Teacher Answer Key & Rubric", desc: "Instructor review mode displaying complete answers, model flowchart logic, and grading criteria for all 5 scenarios.", tag: "Open Teacher Rubric →" },
        c4: { title: "📥 Native PowerPoint (.PPTX)", desc: "16:9 widescreen presentation deck ready for classroom projectors and offline PowerPoint presentations.", tag: "Download PPTX File →" }
      },
      ar: {
        badge: "المنهاج التعليمي المهني // الأستاذ LINGSCH-BEATTIE",
        title: "مركز حل المشكلات: منهجية فرّق تسُد",
        desc: "مركز بيتي المهني والتقني · هندسة الشبكات والأمن السيبراني. احتراف خطوات CompTIA الست لحل الأعطال وخوارزمية البحث الثنائي.",
        c1: { title: "📺 العرض التقديمي للدرس", desc: "درس تفاعلي متقدم من 15 شريحة مع محاكي نقطة المنتصف، ملاحظات المعلم، والتحكم بلوحة المفاتيح.", tag: "بدء العرض التقديمي ←" },
        c2: { title: "⚡ ورقة عمل النشاط العملي", desc: "5 مستويات متدرجة، محاكي طرفية سطر الأوامر، حفظ تلقائي للإجابات، وتصدير ورقة عمل PDF جاهزة للطباعة.", tag: "فتح منصة النشاط للطلاب ←" },
        c3: { title: "🔑 دليل وإجابات المعلم", desc: "وضع مراجعة المعلم لعرض الإجابات النموذجية، مخططات التدفق، ومعايير تقييم المستويات الخمسة.", tag: "فتح نموذج إجابات المعلم ←" },
        c4: { title: "📥 عرض تقديمي أصلي (PPTX)", desc: "ملف PowerPoint بتنسيق 16:9 عريض جاهز للعرض على أجهزة العرض في الفصل دون اتصال بالإنترنت.", tag: "تحميل ملف البوربوينت ←" }
      },
      uk: {
        badge: "НАВЧАЛЬНА ПРОГРАМА // ВИКЛАДАЧ LINGSCH-BEATTIE",
        title: "Портал діагностики: Розділяй і володарюй",
        desc: "Професійно-технічний центр імені А.В. Бітті · Мережева інженерія та кібербезпека. Опануйте 6-етапну модель CompTIA та логіку бінарного пошуку.",
        c1: { title: "📺 Презентація уроку", desc: "Інтерактивний урок на 15 слайдів із симулятором бінарного пошуку, нотатками викладача та керуванням з клавіатури.", tag: "Запустити слайди (HTML) →" },
        c2: { title: "⚡ Практична робота", desc: "5 прогресивних рівнів складності, віртуальний термінал, автозбереження відповідей та друк у PDF.", tag: "Відкрити практичну роботу →" },
        c3: { title: "🔑 Відповіді та критерії викладача", desc: "Режим перевірки для викладача з повними відповідями, блок-схемами та шкалою оцінювання.", tag: "Відкрити критерії оцінювання →" },
        c4: { title: "📥 Презентація PowerPoint (.PPTX)", desc: "Широкоформатна презентація 16:9 для проєкторів та офлайн-використання.", tag: "Завантажити файл PPTX →" }
      }
    };

    function setLang(lang) {
      document.documentElement.lang = lang;
      document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
      localStorage.setItem('hub_lang', lang);

      document.querySelectorAll('#l-en, #l-ar, #l-uk').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`l-${lang}`);
      if (activeBtn) activeBtn.classList.add('active');

      const data = HUB_DB[lang] || HUB_DB.en;
      document.getElementById('hub-badge').textContent = data.badge;
      document.getElementById('hub-title').textContent = data.title;
      document.getElementById('hub-desc').textContent = data.desc;

      document.getElementById('card1-title').textContent = data.c1.title;
      document.getElementById('card1-desc').textContent = data.c1.desc;
      document.getElementById('card1-tag').textContent = data.c1.tag;

      document.getElementById('card2-title').textContent = data.c2.title;
      document.getElementById('card2-desc').textContent = data.c2.desc;
      document.getElementById('card2-tag').textContent = data.c2.tag;

      document.getElementById('card3-title').textContent = data.c3.title;
      document.getElementById('card3-desc').textContent = data.c3.desc;
      document.getElementById('card3-tag').textContent = data.c3.tag;

      document.getElementById('card4-title').textContent = data.c4.title;
      document.getElementById('card4-desc').textContent = data.c4.desc;
      document.getElementById('card4-tag').textContent = data.c4.tag;
    }

    const saved = localStorage.getItem('hub_lang') || 'en';
    setLang(saved);
  </script>
</body>
</html>
"""

with open(index_html_path, "w", encoding="utf-8") as f:
    f.write(index_py)

print(f"Generated index.html -> {index_html_path}")
print("ALL MULTILINGUAL ASSETS GENERATED SUCCESSFULLY!")

