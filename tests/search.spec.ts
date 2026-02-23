import { test, expect } from './fixtures';

test('global search overlay opens, finds terminal lab, navigates, and closes', async ({ page }) => {
  await page.goto('/');
  const shortcutModifier = process.platform === 'darwin' ? 'Meta' : 'Control';
  await page.waitForSelector('html[data-search-ready="true"]');

  await page.keyboard.press(`${shortcutModifier}+KeyK`);
  const overlay = page.locator('#global-search-overlay');
  await expect(overlay).toBeVisible();

  const input = page.locator('#global-search-input');
  await input.fill('terminal');

  const results = page.locator('#global-search-results');
  await expect(results).toContainText(/terminal-basics|Terminal Basics/i);

  await page.locator('#global-search-results a[href="/labs/terminal-basics"]').first().click();
  await expect(page).toHaveURL(/\/labs\/terminal-basics$/);
  await page.waitForSelector('html[data-search-ready="true"]');

  await page.keyboard.press(`${shortcutModifier}+KeyK`);
  await expect(overlay).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(overlay).toBeHidden();
});
