import { type Page } from '@playwright/test';
import { test, expect } from './fixtures';

// Deterministic visual baseline should be captured against production-like output:
// 1) npm run build
// 2) npm run preview -- --host 127.0.0.1 --port 4321
// 3) npx playwright test tests/visual.spec.ts --update-snapshots

const disableMotionCss = `
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
    caret-color: transparent !important;
  }

  input, textarea, [contenteditable="true"] {
    caret-color: transparent !important;
  }

  [data-testid="status-xp"],
  [data-testid="status-streak"],
  [data-testid="status-level"],
  [data-testid="status-track"],
  .sidebar-progress__stats,
  .progress-pill,
  .xp-total,
  .streak-count {
    visibility: hidden !important;
  }
`;

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.clear();
  });
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.addStyleTag({ content: disableMotionCss });
});

const waitForStableUi = async (page: Page) => {
  await page.waitForLoadState('networkidle');
  // wait for readiness classes only when their corresponding UI slots exist on the page
  await page.waitForFunction(() => {
    const hasProgressSlot = Boolean(document.querySelector('[data-progress-slot]'));
    const hasSidebarProgressSlot = Boolean(document.querySelector('[data-sidebar-progress-slot]'));
    const progressReady = document.documentElement.classList.contains('progress-ready');
    const sidebarReady = document.documentElement.classList.contains('sidebar-ready');
    return (!hasProgressSlot || progressReady) && (!hasSidebarProgressSlot || sidebarReady);
  });
  await page.evaluate(async () => {
    if (document.fonts?.ready) {
      await document.fonts.ready;
    }
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
};

const captureStableScreenshot = async (page: Page, name: string) => {
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot(name, { fullPage: true });
};

test('home page', async ({ page }) => {
  await page.goto('/');
  await captureStableScreenshot(page, 'home.png');
});

test('track page', async ({ page }) => {
  await page.goto('/tracks/cybersecurity-foundations');
  await page.locator('.sidebar-progress').waitFor({ state: 'visible' });
  await captureStableScreenshot(page, 'track.png');
});

test('lesson page', async ({ page }) => {
  await page.goto('/lessons/intro-to-cybersecurity');
  await page.locator('.sidebar-progress').waitFor({ state: 'visible' });
  await captureStableScreenshot(page, 'lesson.png');
});

test('lesson page (mobile)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/lessons/intro-to-cybersecurity');
  await page.locator('.sidebar-progress').waitFor({ state: 'visible' });
  await captureStableScreenshot(page, 'lesson-mobile.png');
});

test('legacy page', async ({ page }) => {
  await page.goto('/legacy/a-plus-networking.html');
  await captureStableScreenshot(page, 'legacy.png');
});

test('quizzes page', async ({ page }) => {
  await page.goto('/quizzes');
  await captureStableScreenshot(page, 'quizzes.png');
});

test('quiz runner page', async ({ page }) => {
  await page.goto('/quizzes/a-plus-hardware');
  await captureStableScreenshot(page, 'quiz-runner.png');
});
