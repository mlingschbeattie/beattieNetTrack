import { test, expect } from './fixtures';

test('study guides listing renders and navigates to first guide detail', async ({ page }) => {
  await page.goto('/study-guides');

  const cards = page.locator('.card-grid.card-grid--three .card.card--glass');
  await expect(cards).toHaveCount(3);

  await cards.first().locator('a').click();

  await expect(page).toHaveURL(/\/study-guides\/hardware-fundamentals$/);
  await expect(page.getByRole('heading', { name: /Hardware Fundamentals/i })).toBeVisible();
});
