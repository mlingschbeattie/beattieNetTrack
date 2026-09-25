import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  emitQuizCompleted,
  emitLessonStarted,
  emitLessonCompleted,
  emitLabStarted,
  emitLabCompleted,
  type CISDomainTag,
} from './events';

describe('CIS Events Bus', () => {
  it('exports all LMS event emission helpers', () => {
    assert.equal(typeof emitQuizCompleted, 'function');
    assert.equal(typeof emitLessonStarted, 'function');
    assert.equal(typeof emitLessonCompleted, 'function');
    assert.equal(typeof emitLabStarted, 'function');
    assert.equal(typeof emitLabCompleted, 'function');
  });

  it('safely handles non-browser and empty apiUrl gracefully without throwing', () => {
    const domains: CISDomainTag[] = [{ domainId: 'netplus.networking', weight: 1.0 }];
    assert.doesNotThrow(() => {
      emitQuizCompleted('quiz-1', 95, 100, domains, '');
      emitLessonStarted('lesson-1', 'OSI Model', domains, '');
      emitLessonCompleted('lesson-1', domains, '');
      emitLabStarted('lab-1', 'Terminal Lab', domains, '');
      emitLabCompleted('lab-1', 5, domains, '');
    });
  });

  it('reports untagged content: empty domains still send, with an event type the hub accepts', () => {
    // The LMS event types the hub API guarantees are registered (cluster ensureSchema.ts);
    // anything else is rejected with 400 and silently lost.
    const REGISTERED = new Set([
      'lms.lesson_viewed',
      'lms.lesson_started',
      'lms.assignment_submitted',
      'lms.lab_started',
      'lms.lab_completed',
      'lms.lab_beacon',
      'lms.quiz_completed',
      'lms.lesson_completed',
    ]);
    const sent: Array<{ url: string; body: { eventType: string; payload: Record<string, unknown> } }> = [];
    const store = new Map<string, string>();
    const g = globalThis as Record<string, unknown>;
    const saved = { window: g.window, document: g.document, fetch: g.fetch };
    g.window = {
      localStorage: {
        getItem: (k: string) => store.get(k) ?? null,
        setItem: (k: string, v: string) => void store.set(k, v),
      },
    };
    g.document = { querySelector: () => null };
    g.fetch = (url: string, init: { body: string }) => {
      sent.push({ url, body: JSON.parse(init.body) });
      return Promise.resolve(new Response(null));
    };

    try {
      const slug = 'tech-plus-1-1-1-basics-of-computing';
      emitQuizCompleted(slug, 80, 100, [], 'https://api.test');
      emitLessonStarted(slug, 'Basics of Computing', [], 'https://api.test');
      emitLessonCompleted(slug, [], 'https://api.test');
      emitLabStarted('lab-untagged', 'Untagged Lab', [], 'https://api.test');
      emitLabCompleted('lab-untagged', 3, [], 'https://api.test');

      assert.equal(sent.length, 5, 'every emitter sends even without CIS domain tags');
      for (const { url, body } of sent) {
        assert.equal(url, 'https://api.test/api/events');
        assert.ok(REGISTERED.has(body.eventType), `${body.eventType} is not registered for app lms`);
        assert.deepEqual(body.payload.domains, []);
      }
    } finally {
      Object.assign(g, saved);
    }
  });
});
