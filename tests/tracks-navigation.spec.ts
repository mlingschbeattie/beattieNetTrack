import { test, expect } from './fixtures';

test('learning tracks nav goes to primary hub and opens PC technician track', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: /^Learning Tracks$/i }).click();

  await expect(page).toHaveURL(/\/tracks$/);
  await expect(page.getByRole('heading', { name: /Learning Tracks/i })).toBeVisible();

  await page.getByRole('link', { name: /PC Technician/i }).first().click();

  await expect(page).toHaveURL(/\/tracks\/pc-technician$/);
  await expect(page.locator('.track-section').first()).toBeVisible();
  await expect(page.locator('.track-section .card').first()).toBeVisible();
});

test('tracks landing shows primary tracks', async ({ page }) => {
  await page.goto('/tracks');

  await expect(page.getByRole('link', { name: /PC Technician/i }).first()).toBeVisible();
  await expect(page.getByRole('link', { name: /Network Engineer/i }).first()).toBeVisible();
  await expect(page.getByRole('link', { name: /Cybersecurity Engineer/i }).first()).toBeVisible();
});

test('legacy archived page remains discoverable with link back to current tracks', async ({ page }) => {
  await page.goto('/tracks/legacy');

  await expect(page.getByRole('heading', { name: /legacy track \(archived\)/i })).toBeVisible();
  await expect(page.getByRole('link', { name: /open current tracks/i })).toHaveAttribute('href', '/tracks');
});

test('legacy lab opens in workspace iframe shell', async ({ page }) => {
  await page.goto('/workspace/lab/pc-tech-legacy-hardware-lab');

  await expect(page.getByTestId('lab-iframe')).toBeVisible();
});

test('assessment quiz workspace shell loads', async ({ page }) => {
  await page.goto('/workspace/quiz/assessment-1-1-1');

  const runner = page.getByTestId('quiz-runner');
  await expect(runner).toBeVisible();
  await expect(runner.getByRole('heading', { name: /Assessment 1\.1\.1 Basics of Computing/i })).toBeVisible();
});

test('dashboard Continue link goes to canonical activity route (no /workspace/)', async ({ page }) => {
  await page.goto('/');
  // click the Cybersecurity Foundations Continue link
  const selector = '[data-track-continue-link][data-track-slug="cybersecurity-foundations"]';
  await page.locator(selector).click();
  await page.waitForLoadState('networkidle');

  const url = page.url();
  expect(url.includes('/workspace/')).toBeFalsy();

  // destination should show a visible H1 heading
  await expect(page.locator('h1').first()).toBeVisible();
});
