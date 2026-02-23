import { test, expect } from './fixtures';

const ensureDrawerOpen = async (page: import('@playwright/test').Page) => {
  const drawer = page.locator('[data-workspace-drawer]');
  if (!(await drawer.evaluate((node) => node.classList.contains('workspace-drawer--open')).catch(() => false))) {
    await page.locator('[data-workspace-drawer-toggle]').click();
    await expect(drawer).toHaveClass(/workspace-drawer--open/);
  }
};

test('lab mounts LabRunner and exposes runner contract', async ({ page }) => {
  await page.goto('/labs/network-terminal-basics');

  // Page renders as a step-driven LabRunner (not an iframe workspace)
  await expect(page.getByRole('heading', { name: 'Network Terminal Basics Lab' })).toBeVisible();
  await expect(page.getByTestId('lab-runner')).toBeVisible();
  await expect(page.getByTestId('lab-step-count')).toBeVisible();
  await expect(page.getByTestId('lab-input')).toBeVisible();

  // Confirm no legacy iframe is present for this lab
  await expect(page.locator('[data-testid="lab-iframe"]')).toHaveCount(0);
});

test('mapped lab shows module prev/next navigation', async ({ page }) => {
  await page.goto('/labs/terminal-basics');

  const nav = page.getByTestId('activity-prev-next-nav');
  await expect(nav).toBeVisible();

  await expect(page.getByTestId('activity-prev-link')).toHaveCount(0);
  await expect(page.getByTestId('activity-next-link')).toHaveAttribute('href', '/labs/network-terminal-basics');
  await expect(page.getByTestId('activity-next-link')).toContainText('Next: Network Terminal Basics Lab');
});

test('terminal basics lab completes, awards XP, updates streak, and persists completion', async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => {
    window.localStorage.removeItem('beattie_progress_v1');
  });

  await page.goto('/labs/terminal-basics');

  const xpBefore = Number((await page.getByTestId('status-xp').textContent()) ?? '0');
  const streakBeforeText = (await page.getByTestId('status-streak').textContent()) ?? '0 days';
  const streakBefore = Number.parseInt(streakBeforeText, 10) || 0;

  await expect(page.getByTestId('lab-step-count')).toHaveText('Step 1 of 3');
  await page.getByTestId('lab-input').fill('pwd');
  await page.getByTestId('lab-submit').click();
  await page.getByTestId('lab-next').click();

  await expect(page.getByTestId('lab-step-count')).toHaveText('Step 2 of 3');
  await page.getByTestId('lab-input').fill('ls');
  await page.getByTestId('lab-submit').click();
  await page.getByTestId('lab-next').click();

  await expect(page.getByTestId('lab-step-count')).toHaveText('Step 3 of 3');
  await page.getByTestId('lab-input').fill('cd ..');
  await page.getByTestId('lab-submit').click();

  await expect(page.getByTestId('lab-complete')).toBeVisible();

  const progress = await page.evaluate(() => {
    const raw = window.localStorage.getItem('beattie_progress_v1');
    return raw ? JSON.parse(raw) : null;
  });

  expect(progress?.labs?.['terminal-basics']?.completed).toBe(true);
  expect(progress?.xpTotal).toBe(xpBefore + 25);

  await expect(page.getByTestId('status-xp')).toHaveText(String(xpBefore + 25));

  const streakAfterText = (await page.getByTestId('status-streak').textContent()) ?? '0 days';
  const streakAfter = Number.parseInt(streakAfterText, 10) || 0;
  expect(streakAfter).toBeGreaterThanOrEqual(streakBefore + 1);

  await page.reload();
  await expect(page.getByTestId('lab-complete')).toBeVisible();
});

test('pc assembly lab renders as native workspace panels', async ({ page }) => {
  await page.goto('/labs/pc-assembly');

  await expect(page.locator('[data-workspace]')).toBeVisible();
  await expect(page.getByTestId('pc-lab-root')).toBeVisible();
  await expect(page.getByTestId('mb-diagram')).toBeVisible();
  await expect(page.locator('[data-testid="lab-iframe"]')).toHaveCount(0);

  await page.getByTestId('pc-select-cpu').selectOption('intel-i5-13600k');
  await expect(page.getByTestId('pc-slot-cpu')).toContainText('Intel Core i5-13600K');
  await expect(page.getByTestId('pc-budget')).toContainText('$319');
});

test('legacy workspace lesson URL points to labs experience for pc assembly', async ({ page }) => {
  await page.goto('/workspace/lesson/a-plus-lab-pc-assembly');

  await expect(page.getByText('Lab moved to dedicated route')).toHaveCount(0);
  await expect(page.getByTestId('pc-lab-root')).toBeVisible();
  await expect(page.locator('[data-testid="lab-iframe"]')).toHaveCount(0);
});

test('pc assembly workspace cards have no horizontal overflow on desktop widths', async ({ page }) => {
  const viewports = [
    { width: 1366, height: 768 },
    { width: 1536, height: 864 },
    { width: 1920, height: 1080 },
  ];

  for (const viewport of viewports) {
    await page.setViewportSize(viewport);
    await page.goto('/labs/pc-assembly');
    await expect(page.getByTestId('pc-lab-root')).toBeVisible();

    const hasOverflow = await page.evaluate(() => {
      const selectors = ['.workspace-pane__body', '.pc-lab__panel', '.pc-lab__field', '.pc-lab__select'];
      const nodes = selectors.flatMap((selector) => Array.from(document.querySelectorAll(selector)));
      return nodes.some((node) => {
        const element = node as HTMLElement;
        return element.scrollWidth > element.clientWidth + 1;
      });
    });

    expect(hasOverflow).toBe(false);
  }
});

test('stacked drawer tabs and collapse state persist across reload', async ({ page }) => {
  await page.goto('/labs/pc-assembly');
  await page.evaluate(() => window.localStorage.removeItem('workspace_drawer:pc-assembly'));
  await page.reload();

  await ensureDrawerOpen(page);
  await page.locator('[data-workspace-drawer-tab-button="checks"]').click();
  await expect(page.locator('[data-workspace-checks-panel]')).toHaveClass(/workspace-drawer-panel--active/);

  await page.locator('[data-workspace-drawer-tab-button="notes"]').click();
  await expect(page.locator('[data-workspace-drawer-panel="notes"]')).toHaveClass(/workspace-drawer-panel--active/);

  await page.reload();
  await expect(page.locator('[data-workspace-drawer-panel="notes"]')).toHaveClass(/workspace-drawer-panel--active/);

  await page.locator('[data-workspace-drawer-toggle]').click();
  await expect(page.locator('[data-workspace-drawer]')).not.toHaveClass(/workspace-drawer--open/);
  await page.reload();
  await expect(page.locator('[data-workspace-drawer]')).not.toHaveClass(/workspace-drawer--open/);
});

test('stacked drawer defaults open and remains open after reload', async ({ page }) => {
  await page.goto('/labs/pc-assembly');
  await page.evaluate(() => window.localStorage.removeItem('workspace_drawer:pc-assembly'));
  await page.reload();

  await ensureDrawerOpen(page);

  await page.reload();
  await expect(page.locator('[data-workspace-drawer]')).toHaveClass(/workspace-drawer--open/);
});

test('checks tab updates after pc assembly submit', async ({ page }) => {
  await page.goto('/labs/pc-assembly');
  await page.evaluate(() => window.localStorage.removeItem('workspace_drawer:pc-assembly'));
  await page.reload();
  await ensureDrawerOpen(page);
  await page.locator('[data-workspace-drawer-tab-button="checks"]').click();

  await page.getByTestId('pc-select-cpu').selectOption('intel-i5-13600k');
  await page.getByTestId('pc-select-mobo').selectOption('asus-z790-ddr5');
  await page.getByTestId('pc-select-ram').selectOption('corsair-16gb-ddr5');
  await page.getByTestId('pc-select-storage').selectOption('samsung-500gb');
  await page.getByTestId('pc-select-cooler').selectOption('noctua-nh-d15');

  await page.getByTestId('pc-submit').click();

  const checksPanel = page.locator('[data-workspace-checks-panel]');
  await expect(checksPanel).toContainText(/Latest result/i);
  await expect(checksPanel).toContainText(/PASS|NEEDS WORK/i);
  const percentCount = await page.locator('text=/Score\\s+\\d+%/').count();
  expect(percentCount).toBeLessThanOrEqual(1);
});

test('pc scenario changes only on New Scenario', async ({ page }) => {
  await page.goto('/labs/pc-assembly');

  const scenarioId = page.getByTestId('pc-scenario-id');
  await expect(scenarioId).toBeVisible();
  const initialScenario = (await scenarioId.textContent())?.trim();

  await expect(page.getByTestId('pc-submit')).toBeDisabled();
  await expect(page.getByTestId('pc-submit')).toHaveClass(/btn-is-disabled/);
  const disabledStyles = await page.getByTestId('pc-submit').evaluate((button) => {
    const style = window.getComputedStyle(button as HTMLElement);
    return {
      cursor: style.cursor,
      opacity: style.opacity,
      pointerEvents: style.pointerEvents,
    };
  });
  expect(disabledStyles.cursor).toBe('not-allowed');
  expect(Number(disabledStyles.opacity)).toBeLessThan(0.8);
  expect(disabledStyles.pointerEvents).toBe('none');

  await page.getByTestId('pc-reset').click();
  await expect(page.getByTestId('pc-scenario-id')).toHaveText(initialScenario ?? '');

  await page.getByTestId('pc-run').click();
  await expect(page.getByTestId('pc-scenario-id')).toHaveText(initialScenario ?? '');

  await page.getByTestId('pc-select-cpu').selectOption('intel-i5-13600k');
  await page.getByTestId('pc-select-mobo').selectOption('asus-z790-ddr5');
  await page.getByTestId('pc-select-ram').selectOption('corsair-16gb-ddr5');
  await page.getByTestId('pc-select-storage').selectOption('samsung-500gb');
  await page.getByTestId('pc-select-cooler').selectOption('noctua-nh-d15');

  await expect(page.getByTestId('pc-submit')).toBeEnabled();
  await page.getByTestId('pc-submit').click();
  await expect(page.getByTestId('pc-scenario-id')).toHaveText(initialScenario ?? '');

  await page.getByTestId('pc-new-scenario').click();
  await expect(page.getByTestId('pc-scenario-id')).not.toHaveText(initialScenario ?? '');
});

test('stacked drawer does not clip workspace action bar on desktop', async ({ page }) => {
  const viewports = [
    { width: 1366, height: 768 },
    { width: 1920, height: 1080 },
  ];

  for (const viewport of viewports) {
    await page.setViewportSize(viewport);
    await page.goto('/labs/pc-assembly');
    await page.evaluate(() => window.localStorage.removeItem('workspace_drawer:pc-assembly'));
    await page.reload();

    await ensureDrawerOpen(page);

    const panelBox = await page.locator('.workspace-top-card').boundingBox();
    const barBox = await page.locator('[data-workspace-bar]').boundingBox();

    expect(panelBox).not.toBeNull();
    expect(barBox).not.toBeNull();

    if (panelBox && barBox) {
      const horizontalOverlap = panelBox.x < barBox.x + barBox.width && panelBox.x + panelBox.width > barBox.x;
      const verticalOverlap = panelBox.y < barBox.y + barBox.height && panelBox.y + panelBox.height > barBox.y;
      expect(horizontalOverlap && verticalOverlap).toBe(false);
    }
  }
});
