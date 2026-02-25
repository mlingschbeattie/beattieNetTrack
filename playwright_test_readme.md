# 🚀 Local Development & Visual Testing Guide

This project uses:

- **Astro** for the site framework
- **MDX + Content Collections** for lessons/tracks
- **Playwright** for visual regression testing (UI safety net)

The goal is simple:

> The UI should never accidentally break again.

---

# 📦 First Time Setup

From the repo root:

```bash
cd site
npm install
Install Playwright browsers (required once per machine):

npx playwright install
🧠 Daily Development Workflow
Start the dev server
npm run dev
Then open:

http://localhost:4321
Hot reload is enabled.

🎨 Code Quality Checks
Lint
npm run lint
Format code
npm run format
Check formatting only
npm run format:check
Run these before committing.

🧪 Visual Regression Testing (IMPORTANT)
Playwright takes screenshots of key pages and compares them pixel-for-pixel.

If the UI changes unexpectedly, tests FAIL.

This protects against:

layout shifts

broken CSS

sidebar/nav bugs

accidental redesigns

bad AI refactors

Run visual tests
npm run test:visual
What happens:

Dev server starts

Playwright loads pages

Screenshots are compared to saved baselines

Test fails if anything visually changed

Update snapshots (ONLY for intentional UI changes)
If you intentionally improved the UI:

npm run test:visual:update
This:

overwrites old screenshots

sets the new look as the baseline

⚠️ Do NOT run casually.

Treat this like:

"Yes, this design is the new official UI."

Full CI check (recommended before big merges)
npm run test:ci
Runs:

lint

format check

visual tests

Use this as your pre-flight checklist.

📚 Content Authoring
Lessons live in:

src/content/lessons/
Tracks live in:

src/content/tracks/
Add a lesson
Create:

src/content/lessons/my-lesson.mdx
Example:

---
title: My Lesson
slug: my-lesson
difficulty: medium
tags: [networking]
estimatedMinutes: 20
---

# My Lesson

Content goes here.
Add a track
Create:

src/content/tracks/my-track.json (or .ts/.md depending on config)
Define:

sections

lesson order

metadata

Tracks control:

sidebar ordering

prev/next navigation

progress %

🔄 Migrating Legacy HTML
Use the migration helper:

node scripts/migrate-batch.mjs --inputDir ../legacy --glob "*.html"
This:

creates MDX stubs

preserves titles

stores legacyUrl

wraps old HTML safely

Then clean each lesson manually.

🧱 Project Structure
site/
  src/
    components/
    layouts/
    pages/
    content/
    lib/
  scripts/
  tests/
Legacy site remains separate and untouched.

🛟 Troubleshooting
Playwright fails randomly
Run:

npm run test:visual:update
ONLY if the change is expected.

Port already in use
Change port:

npm run dev -- --port 3000
Reset node modules
rm -rf node_modules
npm install
✅ Recommended Daily Flow
npm run dev

build feature

npm run test:visual

commit

only run test:visual:update if UI intentionally changed