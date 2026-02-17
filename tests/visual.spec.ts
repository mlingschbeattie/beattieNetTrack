import { type Page } from '@playwright/test';
import { test, expect } from './fixtures';

const disableMotionCss = `
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }
`;

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.clear();
  });
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

test('home page', async ({ page }) => {
  await page.goto('/');
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot('home.png', { fullPage: true });
});

test('track page', async ({ page }) => {
  await page.goto('/tracks/cybersecurity-foundations');
  await page.locator('.sidebar-progress').waitFor({ state: 'visible' });
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot('track.png', { fullPage: true });
});

test('lesson page', async ({ page }) => {
  await page.goto('/lessons/intro-to-cybersecurity');
  await page.locator('.sidebar-progress').waitFor({ state: 'visible' });
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot('lesson.png', { fullPage: true });
});

test('lesson page (mobile)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/lessons/intro-to-cybersecurity');
  await page.locator('.sidebar-progress').waitFor({ state: 'visible' });
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot('lesson-mobile.png', { fullPage: true });
});

test('legacy page', async ({ page }) => {
  await page.goto('/legacy/a-plus-networking.html');
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot('legacy.png', { fullPage: true });
});

test('quizzes page', async ({ page }) => {
  await page.goto('/quizzes');
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot('quizzes.png', { fullPage: true });
});

test('quiz runner page', async ({ page }) => {
  await page.goto('/quizzes/a-plus-hardware');
  await waitForStableUi(page);
  await expect(page).toHaveScreenshot('quiz-runner.png', { fullPage: true });
});
