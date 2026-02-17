import { test, expect } from './fixtures';

test('tracks page keeps key layout boxes stable after hydration', async ({ page }) => {
  await page.goto('/tracks/cybersecurity-foundations');
  await page.waitForLoadState('networkidle');

  const capture = async () => {
    const nav = await page.locator('.top-nav').first().boundingBox();
    const breadcrumb = await page.locator('.breadcrumb-row').first().boundingBox();
    const hero = await page.locator('.hero').first().boundingBox();
    const moduleSection = await page.locator('.track-section').first().boundingBox();

    if (!nav || !breadcrumb || !hero || !moduleSection) {
      throw new Error('Expected track layout containers were not found.');
    }

    return { nav, breadcrumb, hero, moduleSection };
  };

  const before = await capture();

  await page.mouse.wheel(0, 120);
  await page.waitForTimeout(1200);

  const after = await capture();

  expect(Math.abs(after.nav.height - before.nav.height)).toBeLessThan(2);
  expect(Math.abs(after.breadcrumb.height - before.breadcrumb.height)).toBeLessThan(2);
  expect(Math.abs(after.hero.height - before.hero.height)).toBeLessThan(2);
  expect(Math.abs(after.moduleSection.height - before.moduleSection.height)).toBeLessThan(2);
});
