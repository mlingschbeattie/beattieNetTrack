import { test, expect } from './fixtures';
import type { Page } from '@playwright/test';

const setMockDate = async (page: Page, isoDate: string) => {
  await page.addInitScript(({ isoDate }: { isoDate: string }) => {
    const now = new Date(isoDate).getTime();
    const OriginalDate = Date;
    class MockDate extends OriginalDate {
      constructor(value?: string | number | Date) {
        if (typeof value === 'undefined') {
          super(now);
        } else {
          super(value);
        }
      }
      static now() {
        return now;
      }
    }
    window.Date = MockDate as unknown as DateConstructor;
  }, { isoDate });
};

test('completing a lesson updates XP and track progress', async ({ page }) => {
  await page.goto('/lessons/intro-to-cybersecurity');
  await page.evaluate(() => {
    window.localStorage.clear();
  });
  await page.reload();
  await page.getByTestId('mark-complete').click();

  // Wait for client islands to signal readiness via document classes
  await page.waitForFunction(() => document.documentElement.classList.contains('progress-ready'));
  await page.locator('[data-testid="status-xp"]').waitFor({ state: 'visible' });
  await expect(page.getByTestId('status-xp')).toHaveText('10');

  await page.goto('/tracks/cybersecurity-foundations');
  await page.waitForFunction(() => document.documentElement.classList.contains('sidebar-ready'));
  await page.locator('[data-testid="track-completed-count"]').waitFor({ state: 'visible' });
  await expect(page.getByTestId('track-completed-count')).toHaveText(/^1\/\d+$/);
});

test('streak increments across days via check-in', async ({ page }) => {
  await setMockDate(page, '2026-02-10T12:00:00Z');
  await page.goto('/lessons/intro-to-cybersecurity');
  await page.evaluate(() => {
    window.localStorage.clear();
  });
  await page.reload();
  await page.getByTestId('check-in').click();
  await expect(page.getByTestId('status-streak')).toHaveText('1 day');

  await setMockDate(page, '2026-02-11T12:00:00Z');
  await page.reload();
  await page.getByTestId('check-in').click();
  await expect(page.getByTestId('status-streak')).toHaveText('2 days');
});
