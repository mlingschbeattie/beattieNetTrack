import { test, expect } from './fixtures';

test('complete a quiz updates progress', async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on('pageerror', (error) => consoleErrors.push(error.message));
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });

  await page.goto('/quizzes');
  await page.evaluate(() => {
    window.localStorage.clear();
  });
  await page.reload();
  await expect(page.getByRole('heading', { name: /quiz catalog/i })).toBeVisible();
  await expect(page.getByRole('heading', { name: /network fundamentals checkpoint/i })).toBeVisible();
  await page.locator('a[href="/quizzes/network-fundamentals-checkpoint"]').first().click();

  for (let i = 0; i < 20; i += 1) {
    const shortInput = page.getByTestId('quiz-short-input');
    if (await shortInput.isVisible().catch(() => false)) {
      await shortInput.fill('route print');
    } else {
      await page.locator('.quiz-option').first().click();
    }

    const submitButton = page.getByTestId('quiz-submit');
    if (await submitButton.isVisible()) {
      break;
    }

    const nextButton = page.getByRole('button', { name: /next/i });
    await expect(nextButton).toBeEnabled();
    await nextButton.click();
  }

  await page.getByTestId('quiz-submit').click();

  await expect(page.getByTestId('quiz-results')).toBeVisible();

  await page.goto('/quizzes');
  await expect(page.getByText(/best:\s*\d+%/i)).toBeVisible();

  const stored = await page.evaluate(() => window.localStorage.getItem('beattie_progress_v1'));
  expect(stored).toContain('"quizzes"');

  expect(consoleErrors).toHaveLength(0);
});
