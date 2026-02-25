import { test, expect } from './fixtures';

test('terminal basics lab runner renders and accepts input', async ({ page }) => {
  await page.goto('/labs/terminal-basics');

  await expect(page.getByTestId('lab-runner')).toBeVisible();
  await expect(page.getByTestId('lab-step-count')).toHaveText('Step 1 of 3');
  await expect(page.getByTestId('lab-input')).toBeVisible();
  await expect(page.getByTestId('lab-submit')).toBeVisible();
});

test('terminal sandbox lab executes deterministic commands and emits submit/reset payloads', async ({ page }) => {
  await page.goto('/labs/terminal-sandbox-basics');

  await expect(page.getByTestId('terminal-sandbox-runner')).toBeVisible();

  await page.evaluate(() => {
    (window as unknown as { __sandboxResults?: unknown[] }).__sandboxResults = [];
    window.addEventListener('workspace:result', (event) => {
      const payload = (event as CustomEvent).detail;
      if (payload?.slug === 'terminal-sandbox-basics') {
        const bag = (window as unknown as { __sandboxResults?: unknown[] }).__sandboxResults;
        if (Array.isArray(bag)) bag.push(payload);
      }
    });
  });

  const input = page.getByTestId('terminal-input');
  const run = page.getByTestId('terminal-run');

  await input.fill('pwd');
  await run.click();

  await input.fill('mkdir project');
  await run.click();

  await input.fill('cd project');
  await run.click();

  await input.fill('touch note.txt');
  await run.click();

  await input.fill('ls');
  await run.click();

  await expect(page.getByTestId('terminal-output')).toContainText('/home/student');
  await expect(page.getByTestId('terminal-output')).toContainText('note.txt');
  await expect(page.getByTestId('terminal-checks')).toContainText('Create project folder');

  const reset = page.getByTestId('terminal-reset');
  await reset.click();
  await expect(input).toHaveValue('');

  const labProgressAfterReset = await page.evaluate(() => {
    const raw = window.localStorage.getItem('beattie_progress_v1');
    if (!raw) return null;
    const parsed = JSON.parse(raw) as {
      labs?: Record<string, { completed?: boolean; completedAt?: string | null; xpAwarded?: boolean; xpEarned?: number }>;
    };
    return parsed.labs?.['terminal-sandbox-basics'] ?? null;
  });

  expect(labProgressAfterReset?.completed).toBe(true);
  expect(typeof labProgressAfterReset?.completedAt).toBe('string');
  expect(labProgressAfterReset?.xpAwarded).toBe(true);
  expect(labProgressAfterReset?.xpEarned).toBe(25);

  const results = await page.evaluate(() =>
    (window as unknown as { __sandboxResults?: Array<Record<string, unknown>> }).__sandboxResults ?? []
  );

  const submitEvent = results.find((entry) => entry.action === 'submit');
  const resetEvent = results.find((entry) => entry.action === 'reset');

  expect(submitEvent).toBeTruthy();
  expect(resetEvent).toBeTruthy();
  expect(Object.keys(submitEvent ?? {}).sort()).toEqual(['action', 'checks', 'message', 'passed', 'progress', 'slug']);
  expect(Object.keys(resetEvent ?? {}).sort()).toEqual(['action', 'checks', 'message', 'passed', 'progress', 'slug']);
});
