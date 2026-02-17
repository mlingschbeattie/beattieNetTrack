import { test, expect } from './fixtures';

test('code runner executes and prints output', async ({ page }) => {
  await page.goto('/labs/code-basics');

  await expect(page.getByTestId('activity-card').first()).toBeVisible();
  await expect(page.getByTestId('code-runner')).toBeVisible();
  await page.getByTestId('code-editor').fill(
    'const packets = [12, 15, 20, 18];\nconst total = packets.reduce((sum, value) => sum + value, 0);\nconsole.log(`Total packets: ${total}`);'
  );

  await page.getByTestId('code-run').click();
  await expect(page.getByTestId('code-output')).toContainText('Total packets: 65');

  const editorFitsContainer = await page.evaluate(() => {
    const runner = document.querySelector('[data-testid="code-runner"]') as HTMLElement | null;
    const editor = document.querySelector('[data-testid="code-editor"]') as HTMLElement | null;
    if (!runner || !editor) return false;
    return editor.scrollWidth <= editor.clientWidth + 1 && runner.getBoundingClientRect().width > 0;
  });
  expect(editorFitsContainer).toBe(true);
});
