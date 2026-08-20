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
    const domains: CISDomainTag[] = [{ domainId: 'netplus.networking_concepts', weight: 1.0 }];
    assert.doesNotThrow(() => {
      emitQuizCompleted('quiz-1', 95, 100, domains, '');
      emitLessonStarted('lesson-1', 'OSI Model', domains, '');
      emitLessonCompleted('lesson-1', domains, '');
      emitLabStarted('lab-1', 'Terminal Lab', domains, '');
      emitLabCompleted('lab-1', 5, domains, '');
    });
  });
});
