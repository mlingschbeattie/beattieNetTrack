import { getCollection, type CollectionEntry } from 'astro:content';

export type TrackActivityType = 'lab' | 'quiz' | 'lesson';

export interface TrackSummary {
  slug: string;
  title: string;
  description: string;
  order: number;
  icon?: string;
}

export interface TrackActivitySummary {
  slug: string;
  type: TrackActivityType;
  title: string;
  description: string;
  order: number;
  href: string;
  module: string;
}

export interface PrevNextLink {
  slug: string;
  type: TrackActivityType;
  title: string;
  href: string;
}

export interface TrackModuleSummary {
  slug: string;
  title: string;
  description: string;
  order: number;
  activities: TrackActivitySummary[];
  prevNextByKey: Record<string, { prev: PrevNextLink | null; next: PrevNextLink | null }>;
}

export interface TrackDetailData {
  track: TrackSummary;
  modules: TrackModuleSummary[];
}

const toTrackSummary = (track: CollectionEntry<'tracks'>): TrackSummary => ({
  slug: track.slug,
  title: track.data.title,
  description: track.data.description ?? '',
  order: track.data.order ?? 0,
  icon: track.data.icon,
});

const compareOrderTitleSlug = <T extends { order: number; title: string; slug: string }>(a: T, b: T) => {
  return a.order - b.order || a.title.localeCompare(b.title) || a.slug.localeCompare(b.slug);
};

const toActivityKey = (activity: { type: TrackActivityType; slug: string }) => `${activity.type}:${activity.slug}`;

const buildPrevNextByKey = (
  activities: TrackActivitySummary[]
): Record<string, { prev: PrevNextLink | null; next: PrevNextLink | null }> => {
  const map: Record<string, { prev: PrevNextLink | null; next: PrevNextLink | null }> = {};
  for (let index = 0; index < activities.length; index += 1) {
    const current = activities[index];
    if (!current) continue;
    const prev = activities[index - 1];
    const next = activities[index + 1];
    map[toActivityKey(current)] = {
      prev: prev
        ? {
            slug: prev.slug,
            type: prev.type,
            title: prev.title,
            href: prev.href,
          }
        : null,
      next: next
        ? {
            slug: next.slug,
            type: next.type,
            title: next.title,
            href: next.href,
          }
        : null,
    };
  }
  return map;
};

const getActivityModuleSlug = (data: { module?: string; moduleId?: string }) => data.module ?? data.moduleId ?? null;

export const getTracksIndexData = async (): Promise<TrackSummary[]> => {
  const tracks = await getCollection('tracks');
  return tracks.map(toTrackSummary).sort(compareOrderTitleSlug);
};

export const getTrackDetailData = async (trackSlug: string): Promise<TrackDetailData | null> => {
  const [tracks, modules, labs, quizzes, lessons] = await Promise.all([
    getCollection('tracks'),
    getCollection('modules'),
    getCollection('labs'),
    getCollection('quizzes'),
    getCollection('lessons'),
  ]);

  const trackEntry = tracks.find((entry) => entry.slug === trackSlug);
  if (!trackEntry) return null;

  const moduleMap = new Map<string, { slug: string; title: string; description: string; order: number }>();
  for (const moduleEntry of modules) {
    if (moduleEntry.data.track !== trackSlug) continue;
    const moduleSlug = moduleEntry.slug;
    moduleMap.set(moduleSlug, {
      slug: moduleSlug,
      title: moduleEntry.data.title,
      description: moduleEntry.data.description ?? '',
      order: moduleEntry.data.order ?? 0,
    });
  }

  const moduleActivityMap = new Map<string, TrackActivitySummary[]>();
  const pushActivity = (activity: TrackActivitySummary) => {
    const existing = moduleActivityMap.get(activity.module) ?? [];
    existing.push(activity);
    moduleActivityMap.set(activity.module, existing);
  };

  for (const entry of labs) {
    if (entry.data.track !== trackSlug) continue;
    const moduleSlug = getActivityModuleSlug(entry.data);
    if (!moduleSlug) continue;
    pushActivity({
      slug: entry.slug,
      type: 'lab',
      title: entry.data.title,
      description: entry.data.description,
      order: entry.data.order ?? 0,
      href: `/labs/${entry.slug}`,
      module: moduleSlug,
    });
  }

  for (const entry of quizzes) {
    if (entry.data.track !== trackSlug) continue;
    const moduleSlug = getActivityModuleSlug(entry.data);
    if (!moduleSlug) continue;
    pushActivity({
      slug: entry.slug,
      type: 'quiz',
      title: entry.data.title,
      description: entry.data.description ?? 'Quiz workspace',
      order: entry.data.order ?? 0,
      href: `/quizzes/${entry.slug}`,
      module: moduleSlug,
    });
  }

  for (const entry of lessons) {
    if (entry.data.track !== trackSlug) continue;
    if (typeof entry.data.order !== 'number') continue;
    if (!entry.data.module) continue;
    pushActivity({
      slug: entry.slug,
      type: 'lesson',
      title: entry.data.title,
      description: entry.data.description ?? 'Lesson',
      order: entry.data.order,
      href: `/lessons/${entry.slug}`,
      module: entry.data.module,
    });
  }

  const modulesWithActivities: TrackModuleSummary[] = [];
  for (const [moduleSlug, activities] of moduleActivityMap.entries()) {
    const sortedActivities = activities.sort(compareOrderTitleSlug);
    const moduleData = moduleMap.get(moduleSlug);
    modulesWithActivities.push({
      slug: moduleSlug,
      title: moduleData?.title ?? moduleSlug,
      description: moduleData?.description ?? '',
      order: moduleData?.order ?? 999,
      activities: sortedActivities,
      prevNextByKey: buildPrevNextByKey(sortedActivities),
    });
  }

  modulesWithActivities.sort(compareOrderTitleSlug);

  return {
    track: toTrackSummary(trackEntry),
    modules: modulesWithActivities,
  };
};

export const getPrevNextInModule = (
  module: TrackModuleSummary,
  activity: { slug: string; type: TrackActivityType }
): { prev: PrevNextLink | null; next: PrevNextLink | null } => {
  return module.prevNextByKey[toActivityKey(activity)] ?? { prev: null, next: null };
};
