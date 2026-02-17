import { test as base, expect } from '@playwright/test';

type InvalidHookMessage = {
  kind: 'console' | 'pageerror';
  text: string;
};

export const test = base.extend({
  page: async ({ page }, use, testInfo) => {
    const invalidHookMessages: InvalidHookMessage[] = [];
    const pattern = /invalid hook call/i;

    page.on('console', (message) => {
      const text = message.text();
      if (pattern.test(text)) {
        invalidHookMessages.push({ kind: 'console', text });
      }
    });

    page.on('pageerror', (error) => {
      if (pattern.test(error.message)) {
        invalidHookMessages.push({ kind: 'pageerror', text: error.message });
      }
    });

    await use(page);

    if (invalidHookMessages.length > 0) {
      const details = invalidHookMessages
        .map((entry, index) => `${index + 1}. [${entry.kind}] ${entry.text}`)
        .join('\n');
      throw new Error(`Invalid hook call detected in browser context during ${testInfo.title}:\n${details}`);
    }
  },
});

export { expect };