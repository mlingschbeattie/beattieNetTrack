import { useEffect, useState } from 'react';
import { getProgress } from '../../lib/progressStore';
import type { TrackModuleSummary, TrackActivitySummary } from '../../lib/content';

interface TrackModuleListProps {
  modules: TrackModuleSummary[];
}

export function isActivityCompleted(
  activity: TrackActivitySummary,
  state: ReturnType<typeof getProgress>
): boolean {
  if (!state) return false;
  const slug = activity.slug;

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

  const isUnlockedList: boolean[] = [];
  for (let i = 0; i < modules.length; i++) {
    if (i === 0) {
      isUnlockedList.push(true);
    } else {
      const prevStats = moduleStats[i - 1];
      isUnlockedList.push(Boolean(prevStats && prevStats.isPassing));
    }
  }

  return (
    <>
      {modules.map((module, index) => {
        const isUnlocked = isUnlockedList[index];
        const stats = moduleStats[index];
        const prevModule = index > 0 ? modules[index - 1] : null;
        const prevStats = index > 0 ? moduleStats[index - 1] : null;

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

            <div className="card-grid card-grid--two">
              {module.activities.map((activity) => {
                const isComplete = Boolean(completedMap[`${activity.type}:${activity.slug}`]);

                return (
                  <article
                    key={`${activity.type}-${activity.slug}`}
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
                      {isComplete && (
                        <span className="badge badge--completed" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                          ✓ Completed
                        </span>
                      )}
                    </div>

                    <h3>{activity.title}</h3>
                    <p>{activity.description || 'Complete this learning activity to progress your certification track.'}</p>

                    <div className="card__footer">
                      {isUnlocked ? (
                        <a className="btn-link" href={activity.href}>
                          <span>Open Activity</span>
                          <span className="icon-directional">→</span>
                        </a>
                      ) : (
                        <span
                          className="btn-link btn-is-disabled"
                          aria-disabled="true"
                          role="status"
                          aria-label={`Locked: ${activity.title} — Complete previous section to unlock`}
                          style={{ cursor: 'not-allowed', opacity: 0.6 }}
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
