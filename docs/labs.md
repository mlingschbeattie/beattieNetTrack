# Adding a New Lab

This project uses an iframe-first lab model with workspace controls and shared progress.

## 1) Add lab metadata + instructions

Create a new file in `src/content/labs/<slug>.mdx`:

```mdx
---
title: My Lab
description: What students do.
slug: my-lab
track: cybersecurity-foundations
module: Daily Workflow
order: 120
difficulty: Beginner
estMinutes: 25
labPath: /labs/my-lab/index.html
checkLabel: Check Lab
submitLabel: Submit Lab
---

Lab instructions in markdown/MDX.
```

## 2) Add runtime lab files

Create:

- `public/labs/my-lab/index.html`
- Include `<link rel="stylesheet" href="/styles/lab-shared.css" />`
- Include `<script src="/labs/runtime/lab-api.js"></script>`

Register handlers inside your lab page:

```js
window.ClassroomProgress.on('check', () => ({ passed: true, progress: 100, message: 'Checks passed' }));
window.ClassroomProgress.on('submit', () => ({ passed: true, progress: 100, message: 'Submitted' }));
window.ClassroomProgress.on('reset', () => ({ passed: true, progress: 0, message: 'Reset' }));
```

## 3) Route usage

Your lab is automatically available at:

- `/labs/my-lab`
- `/workspace/lab/my-lab`
- `/tracks/<track>/labs/my-lab` (when `track` is set)

## 4) Track integration

Labs appear on track pages when:

- `track` matches the track slug
- `module` matches the section title in track content frontmatter

## 5) Progress model

Workspace controls write completion through `src/lib/progressStore.ts`.
Use the lab API `check/submit/reset` messages to signal pass/fail and progress.

## Validation checklist

- Workspace renders split panes + bottom control bar.
- `Ctrl+Enter` triggers submit/check.
- Lab iframe loads and responds to Run/Check/Submit/Reset.
- `lab-shared.css` is present in iframe.
- Completion updates track progress indicators.
