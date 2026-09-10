import { useEffect, useState } from 'react';
import {
  getProgress,
  isContentWaived,
  getWaivedReason,
  fetchWaivedContent,
} from '../../lib/progressStore';
import type { TrackModuleSummary, TrackActivitySummary } from '../../lib/content';

interface TrackModuleListProps {
  modules: Array<Omit<TrackModuleSummary, 'prevNextByKey'> & { prevNextByKey?: TrackModuleSummary['prevNextByKey'] }>;
}

export function isActivityCompleted(
  activity: TrackActivitySummary,
  state: ReturnType<typeof getProgress>
): boolean {
  if (!state) return false;
  const slug = activity.slug;

  if (isContentWaived(slug)) {
    return true;
  }

  if (activity.type === 'lab') {
    return Boolean(state.labs?.[slug]?.completed);
  }

  if (activity.type === 'quiz') {
    return (state.quizzes?.[slug]?.bestScore ?? 0) >= 70;
  }

  if (activity.type === 'lesson') {
    const lessonEntry = state.lessons?.[slug];
    if (!lessonEntry?.completed) return false;

    // If lesson has section checks recorded, ensure they are completed
    const sectionChecks = state.lessonSections?.[slug];
    if (sectionChecks && Object.keys(sectionChecks).length > 0) {
      const allPassed = Object.values(sectionChecks).every(Boolean);
      if (!allPassed) return false;
    }
    return true;
  }

  // Generic activity: check labs or lessons
  return Boolean(state.labs?.[slug]?.completed || state.lessons?.[slug]?.completed);
}

export interface ConceptUnit {
  id: string;
  order: number;
  title: string;
  lesson?: TrackActivitySummary;
  quiz?: TrackActivitySummary;
  standalone?: TrackActivitySummary;
}

export function getCoreConceptSlug(slug: string): string {
  return slug
    .toLowerCase()
    .replace(/^(?:tech-plus|net|pct|cfs)-/, '')
    .replace(/^\d+-\d+(?:-\d+)?-/, '')
    .replace(/-vs-|-and-|-or-/g, '-')
    .trim();
}

export function doActivitiesMatchConcept(
  lesson: TrackActivitySummary,
  quiz: TrackActivitySummary
): boolean {
  if (lesson.slug === quiz.slug) return true;

  const coreLesson = getCoreConceptSlug(lesson.slug);
  const coreQuiz = getCoreConceptSlug(quiz.slug);

  if (coreLesson && coreQuiz && coreLesson === coreQuiz) return true;

  if (coreLesson.length > 5 && coreQuiz.length > 5) {
    if (coreLesson.includes(coreQuiz) || coreQuiz.includes(coreLesson)) {
      return true;
    }
  }

  return false;
}

export function groupActivitiesIntoConceptUnits(activities: TrackActivitySummary[]): ConceptUnit[] {
  const units: ConceptUnit[] = [];
  const used = new Set<string>();

  for (let i = 0; i < activities.length; i++) {
    const act = activities[i];
    const key = `${act.type}:${act.slug}`;
    if (used.has(key)) continue;

    if (act.type === 'lesson') {
      // Find matching checkpoint quiz by semantic concept match within the module.
      // We deliberately avoid naive order === order matching to prevent cross-topic hijacking
      // when content authors share order values or module checkpoints exist.
      const matchingQuizIndex = activities.findIndex(
        (other) =>
          other.type === 'quiz' &&
          !used.has(`${other.type}:${other.slug}`) &&
          doActivitiesMatchConcept(act, other)
      );

      if (matchingQuizIndex !== -1) {
        const matchingQuiz = activities[matchingQuizIndex];
        used.add(key);
        used.add(`${matchingQuiz.type}:${matchingQuiz.slug}`);

        // Derive concept title cleanly (e.g. "Storage Units — From Bits to Petabytes" -> "Storage Units")
        const conceptTitle = act.title.split('—')[0]?.trim() || act.title;

        units.push({
          id: `concept-${act.slug}`,
          order: act.order,
          title: conceptTitle,
          lesson: act,
          quiz: matchingQuiz,
        });
        continue;
      }
    }

    // Standalone activity (e.g. lab, standalone quiz, or standalone lesson)
    used.add(key);
    units.push({
      id: `standalone-${act.type}-${act.slug}`,
      order: act.order,
      title: act.title,
      standalone: act,
    });
  }

  return units;
}

export default function TrackModuleList({ modules }: TrackModuleListProps) {
  const [completedMap, setCompletedMap] = useState<Record<string, boolean>>({});

  useEffect(() => {
    const update = () => {
      const state = getProgress();
      const map: Record<string, boolean> = {};

      for (const mod of modules) {
        for (const act of mod.activities) {
          map[`${act.type}:${act.slug}`] = isActivityCompleted(act, state);
        }
      }
      setCompletedMap(map);
    };

    update();
    fetchWaivedContent().then(() => {
      update();
    });
    window.addEventListener('progress-updated', update);
    return () => window.removeEventListener('progress-updated', update);
  }, [modules]);

  if (!modules || modules.length === 0) {
    return (
      <section className="track-section">
        <div className="section-head">
          <h2>Modules</h2>
          <div className="section-head-line"></div>
        </div>
        <article className="card">
          <h3>No modules published yet</h3>
          <p>This track is configured, but no module activities are available right now.</p>
        </article>
      </section>
    );
  }

  // Calculate unlocking sequentially:
  // Section 0 is always unlocked.
  // Section N (N >= 1) is unlocked if Section N-1 has >= 80% completion.
  const moduleStats = modules.map((mod) => {
    const total = mod.activities.length;
    const completed = mod.activities.filter(
      (act) => completedMap[`${act.type}:${act.slug}`]
    ).length;
    const percent = total > 0 ? Math.round((completed / total) * 100) : 100;
    const isPassing = total === 0 || (completed / total) >= 0.8;
    const requiredToUnlock = Math.ceil(total * 0.8);
    return { total, completed, percent, isPassing, requiredToUnlock };
  });

  return (
    <>
      {modules.map((module, sectionIndex) => {
        const stats = moduleStats[sectionIndex];
        const isUnlocked = sectionIndex === 0 || moduleStats[sectionIndex - 1].isPassing;
        const prevModule = sectionIndex > 0 ? modules[sectionIndex - 1] : null;
        const prevStats = sectionIndex > 0 ? moduleStats[sectionIndex - 1] : null;
        const conceptUnits = groupActivitiesIntoConceptUnits(module.activities);

        return (
          <section
            key={module.slug}
            className={`track-section ${!isUnlocked ? 'track-section--locked' : ''}`}
            aria-label={`${module.title} ${!isUnlocked ? '(Locked)' : ''}`}
          >
            <div className="section-head">
              <div className="section-head__title-row" style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
                <h2>{module.title}</h2>
                {!isUnlocked ? (
                  <span className="track-section__lock-badge" title="Complete 80% of previous section to unlock">
                    🔒 Locked
                  </span>
                ) : stats.total > 0 ? (
                  <span className="pill pill--muted" style={{ fontSize: '12px' }}>
                    {stats.completed}/{stats.total} completed ({stats.percent}%)
                  </span>
                ) : null}
              </div>
              <div className="section-head-line"></div>
            </div>

            {module.description && <p className="track-section__subtitle">{module.description}</p>}

            {!isUnlocked && prevModule && prevStats && (
              <div
                className="callout callout--info"
                style={{ marginBottom: '16px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}
              >
                <span>🔒</span>
                <span>
                  <strong>Locked:</strong> Complete at least 80% ({prevStats.requiredToUnlock} of {prevStats.total} activities) of{' '}
                  <em>{prevModule.title}</em> to unlock this section. Currently {prevStats.completed}/{prevStats.total} complete.
                </span>
              </div>
            )}

            <div className="concept-units-list">
              {conceptUnits.map((unit) => {
                if (unit.lesson || unit.quiz) {
                  const isLessonWaived = unit.lesson ? isContentWaived(unit.lesson.slug) : false;
                  const lessonWaivedReason = unit.lesson ? getWaivedReason(unit.lesson.slug) : null;
                  const isLessonComplete = unit.lesson
                    ? Boolean(completedMap[`${unit.lesson.type}:${unit.lesson.slug}`])
                    : false;

                  const isQuizWaived = unit.quiz ? isContentWaived(unit.quiz.slug) : false;
                  const quizWaivedReason = unit.quiz ? getWaivedReason(unit.quiz.slug) : null;
                  const isQuizComplete = unit.quiz
                    ? Boolean(completedMap[`${unit.quiz.type}:${unit.quiz.slug}`])
                    : false;

                  const unitMastered = isLessonComplete && isQuizComplete;

                  return (
                    <article
                      key={unit.id}
                      className={`card concept-unit-card ${!isUnlocked ? 'card--locked' : ''}`}
                    >
                      <div className="concept-unit-header">
                        <div className="concept-unit-header__badge-row">
                          <span className="concept-unit-pill">Concept Unit {unit.order}</span>
                          {unitMastered ? (
                            <span
                              className="badge badge--completed"
                              style={isLessonWaived || isQuizWaived ? { background: 'rgba(16, 185, 129, 0.15)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.35)' } : undefined}
                            >
                              ✓ Unit Mastered {isLessonWaived || isQuizWaived ? '(Credit)' : ''}
                            </span>
                          ) : isLessonComplete ? (
                            <span
                              className="badge badge--in-progress"
                              style={{
                                background: 'rgba(59, 130, 246, 0.12)',
                                color: '#60a5fa',
                                border: '1px solid rgba(59, 130, 246, 0.25)',
                              }}
                            >
                              Quiz Ready
                            </span>
                          ) : null}
                        </div>
                        <h3 className="concept-unit-title">{unit.title}</h3>
                      </div>

                      <div className="concept-step-flow">
                        {unit.lesson && (
                          <div
                            className={`concept-step-item concept-step-item--lesson ${
                              isLessonComplete ? 'concept-step-item--complete' : ''
                            }`}
                          >
                            <div className="concept-step-indicator">
                              <span className="concept-step-number">1</span>
                              <span className="concept-step-type-label">Core Lesson</span>
                            </div>
                            <div className="concept-step-content">
                              <div className="concept-step-header">
                                <h4 className="concept-step-title">{unit.lesson.title}</h4>
                                {isLessonWaived ? (
                                  <span
                                    className="badge"
                                    style={{
                                      background: 'rgba(16, 185, 129, 0.15)',
                                      color: '#10b981',
                                      border: '1px solid rgba(16, 185, 129, 0.35)',
                                      fontSize: '11px',
                                      padding: '2px 8px',
                                    }}
                                    title={lessonWaivedReason || 'Satisfied via Certification'}
                                  >
                                    ✓ Satisfied via Certification
                                  </span>
                                ) : isLessonComplete ? (
                                  <span className="badge badge--completed">
                                    ✓ Completed
                                  </span>
                                ) : null}
                              </div>
                            </div>
                            <div className="concept-step-action">
                              {isUnlocked ? (
                                <a className="btn-link" href={unit.lesson.href}>
                                  <span>{isLessonWaived ? 'Review Lesson' : 'Read Lesson'}</span>
                                  <span className="icon-directional">→</span>
                                </a>
                              ) : (
                                <span
                                  className="btn-link btn-is-disabled"
                                  aria-disabled="true"
                                  role="status"
                                  aria-label={`Locked: ${unit.lesson.title} — Complete previous section to unlock`}
                                >
                                  <span>🔒 Locked</span>
                                </span>
                              )}
                            </div>
                          </div>
                        )}

                        {unit.quiz && (
                          <div
                            className={`concept-step-item concept-step-item--quiz ${
                              isQuizComplete ? 'concept-step-item--complete' : ''
                            }`}
                          >
                            <div className="concept-step-indicator">
                              <span className="concept-step-number">2</span>
                              <span className="concept-step-type-label">Checkpoint Quiz</span>
                            </div>
                            <div className="concept-step-content">
                              <div className="concept-step-header">
                                <h4 className="concept-step-title">{unit.quiz.title}</h4>
                                {isQuizWaived ? (
                                  <span
                                    className="badge"
                                    style={{
                                      background: 'rgba(16, 185, 129, 0.15)',
                                      color: '#10b981',
                                      border: '1px solid rgba(16, 185, 129, 0.35)',
                                      fontSize: '11px',
                                      padding: '2px 8px',
                                    }}
                                    title={quizWaivedReason || 'Satisfied via Certification'}
                                  >
                                    ✓ Satisfied via Certification
                                  </span>
                                ) : isQuizComplete ? (
                                  <span className="badge badge--completed">
                                    ✓ Passed
                                  </span>
                                ) : isLessonComplete ? (
                                  <span
                                    className="badge"
                                    style={{
                                      background: 'rgba(59, 130, 246, 0.12)',
                                      color: '#60a5fa',
                                      border: '1px solid rgba(59, 130, 246, 0.25)',
                                      fontSize: '11px',
                                      padding: '2px 8px',
                                    }}
                                  >
                                    Ready to Test
                                  </span>
                                ) : null}
                              </div>
                            </div>
                            <div className="concept-step-action">
                              {isUnlocked ? (
                                <a className="btn-link" href={unit.quiz.href}>
                                  <span>{isQuizWaived ? 'Review Quiz' : 'Take Checkpoint Quiz'}</span>
                                  <span className="icon-directional">→</span>
                                </a>
                              ) : (
                                <span
                                  className="btn-link btn-is-disabled"
                                  aria-disabled="true"
                                  role="status"
                                  aria-label={`Locked: ${unit.quiz.title} — Complete previous section to unlock`}
                                >
                                  <span>🔒 Locked</span>
                                </span>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    </article>
                  );
                }

                // Standalone activity (e.g. lab sandbox, standalone assessment)
                const activity = unit.standalone!;
                const isActWaived = isContentWaived(activity.slug);
                const actWaivedReason = getWaivedReason(activity.slug);
                const isComplete = Boolean(completedMap[`${activity.type}:${activity.slug}`]);

                return (
                  <article
                    key={unit.id}
                    className={`card card--activity-${activity.type ?? 'lesson'} ${!isUnlocked ? 'card--locked' : ''}`}
                  >
                    <div className="card__header-row">
                      <span className={`badge badge--activity-${activity.type ?? 'lesson'}`}>
                        {activity.type === 'lab'
                          ? 'Lab Sandbox'
                          : activity.type === 'quiz'
                            ? 'Checkpoint Quiz'
                            : activity.type === 'activity'
                              ? 'Hands-on Activity'
                              : 'Core Lesson'}
                      </span>
                      {isActWaived ? (
                        <span
                          className="badge"
                          style={{
                            background: 'rgba(16, 185, 129, 0.15)',
                            color: '#10b981',
                            border: '1px solid rgba(16, 185, 129, 0.35)',
                            fontSize: '11px',
                            padding: '2px 8px',
                          }}
                          title={actWaivedReason || 'Satisfied via Certification'}
                        >
                          ✓ Satisfied via Certification
                        </span>
                      ) : isComplete ? (
                        <span className="badge badge--completed">
                          ✓ Completed
                        </span>
                      ) : null}
                    </div>

                    <h3>{activity.title}</h3>
                    <p>{activity.description || 'Complete this learning activity to progress your certification track.'}</p>
                    {isActWaived && actWaivedReason && (
                      <p style={{ fontSize: '12px', color: '#10b981', marginTop: '4px' }}>
                        Exempt: {actWaivedReason}
                      </p>
                    )}

                    <div className="card__footer">
                      {isUnlocked ? (
                        <a className="btn-link" href={activity.href}>
                          <span>{isActWaived ? 'Review Activity (Optional)' : 'Open Activity'}</span>
                          <span className="icon-directional">→</span>
                        </a>
                      ) : (
                        <span
                          className="btn-link btn-is-disabled"
                          aria-disabled="true"
                          role="status"
                          aria-label={`Locked: ${activity.title} — Complete previous section to unlock`}
                        >
                          <span>🔒 Locked</span>
                        </span>
                      )}
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        );
      })}
    </>
  );
}
