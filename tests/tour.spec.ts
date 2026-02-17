import { test, expect } from './fixtures';

test('tour step 1 completion continues to step 2', async ({ page }) => {
  await page.goto('/tour/terminal-challenge');

  await expect(page.getByRole('heading', { name: /challenge 1/i })).toBeVisible();
  await page.getByTestId('terminal-input').fill('help');
  await page.getByTestId('terminal-run').click();
  await page.getByTestId('terminal-input').fill('pwd');
  await page.getByTestId('terminal-run').click();

  await page.locator('[data-workspace-action="check"]').click();
  await expect(page.getByTestId('workspace-progress')).toHaveText(/100%|\d+%/);

  await page.getByTestId('tour-next-link').click();
  await expect(page).toHaveURL(/\/tour\/quiz-challenge/);
});
