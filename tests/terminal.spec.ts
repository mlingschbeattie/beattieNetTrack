import { test, expect } from './fixtures';

test('terminal basics lab runner renders and accepts input', async ({ page }) => {
  await page.goto('/labs/terminal-basics');

  await expect(page.getByTestId('lab-runner')).toBeVisible();
  await expect(page.getByTestId('lab-step-count')).toHaveText('Step 1 of 3');
  await expect(page.getByTestId('lab-input')).toBeVisible();
  await expect(page.getByTestId('lab-submit')).toBeVisible();
});
