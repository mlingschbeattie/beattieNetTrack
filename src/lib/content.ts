import { getCollection, type CollectionEntry } from 'astro:content';
import { normalizeLessonMeta } from './lessonMeta';

export type TrackActivityType = 'lab' | 'quiz' | 'lesson' | 'activity';

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

export interface ActivityModuleNavigation {
  trackSlug: string;
  moduleSlug: string;
  prev: PrevNextLink | null;
  next: PrevNextLink | null;
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
  return tracks.filter((t) => !t.data.hidden).map(toTrackSummary).sort(compareOrderTitleSlug);
};

export const getTrackDetailData = async (trackSlug: string): Promise<TrackDetailData | null> => {
  const [tracks, modules, labs, quizzes, lessons, activities] = await Promise.all([
    getCollection('tracks'),
    getCollection('modules'),
    getCollection('labs'),
    getCollection('quizzes'),
    getCollection('lessons'),
    getCollection('activities'),
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
    const moduleSlug = getActivityModuleSlug(entry.data);
    if (!moduleSlug) continue;
    pushActivity({
      slug: entry.slug,
      type: 'lesson',
      title: entry.data.title,
      description: entry.data.description ?? 'Lesson',
      order: entry.data.order,
      href: `/lessons/${entry.slug}`,
      module: moduleSlug,
    });
  }

  for (const entry of activities) {
    if (entry.data.track !== trackSlug) continue;
    const moduleSlug = getActivityModuleSlug(entry.data);
    if (!moduleSlug) continue;
    pushActivity({
      slug: entry.slug,
      type: 'activity',
      title: entry.data.title,
      description: entry.data.description ?? 'Workspace activity',
      order: entry.data.order ?? 0,
      href: `/workspace/activity/${entry.slug}`,
      module: moduleSlug,
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

export const getActivityModuleNavigation = async (
  activity: { slug: string; type: TrackActivityType }
): Promise<ActivityModuleNavigation | null> => {
  const tracks = await getTracksIndexData();
  const trackDetails = await Promise.all(tracks.map((track) => getTrackDetailData(track.slug)));

  for (const detail of trackDetails) {
    if (!detail) continue;
    for (const module of detail.modules) {
      const key = toActivityKey(activity);
      const links = module.prevNextByKey[key];
      if (!links) continue;
      return {
        trackSlug: detail.track.slug,
        moduleSlug: module.slug,
        prev: links.prev,
        next: links.next,
      };
    }
  }

  return null;
};

export const getModuleProgressData = async (
  trackSlug: string,
  moduleSlug: string
): Promise<{ total: number; completed: number; activities: { type: TrackActivityType; slug: string }[] } | null> => {
  const detail = await getTrackDetailData(trackSlug);
  if (!detail) return null;
  const module = detail.modules.find((m) => m.slug === moduleSlug);
  if (!module) return null;
  const activities = module.activities.map((a) => ({ type: a.type, slug: a.slug }));
  return {
    total: activities.length,
    // Server-side cannot read client progress; default to 0.
    completed: 0,
    activities,
  };
};

export interface ProgressData {
  labs?: Record<string, { completed?: boolean }>;
  lessons?: Record<string, { completed?: boolean }>;
  quizzes?: Record<string, { completed?: boolean }>;
}

export const getTrackContinueHref = async (trackSlug: string, progress: ProgressData | null = null): Promise<string> => {
  const detail = await getTrackDetailData(trackSlug);
  if (!detail) return `/tracks/${trackSlug}`;

  for (const module of detail.modules) {
    for (const activity of module.activities) {
      if (progress) {
        const collectionKey =
          activity.type === 'lab' ? 'labs' : activity.type === 'quiz' ? 'quizzes' : 'lessons';
        const completed = Boolean((progress as any)[collectionKey]?.[activity.slug]?.completed);
        if (!completed) return activity.href;
      } else {
        return activity.href;
      }
    }
  }

  return `/tracks/${trackSlug}`;
};

type LegacyTrackSlug = 'pc-technician' | 'network-engineer' | 'cybersecurity-engineer';

const legacyNetworkKeywords = ['network', 'https-demo'];
const legacyPcKeywords = [
  'a-plus-guides',
  'a-plus-hardware',
  'a-plus-motherboards',
  'a-plus-operating-systems',
  'a-plus-power-cooling',
  'a-plus-storage',
  'a-plus-troubleshooting',
  'a-plus-lab-',
  'a-plus-labs',
];

export const inferLegacyTrackSlug = (legacySlug: string): LegacyTrackSlug => {
  if (legacyNetworkKeywords.some((keyword) => legacySlug.includes(keyword))) {
    return 'network-engineer';
  }
  if (legacyPcKeywords.some((keyword) => legacySlug.startsWith(keyword) || legacySlug.includes(keyword))) {
    return 'pc-technician';
  }
  return 'cybersecurity-engineer';
};

export const toLegacyLabPath = (legacyUrl?: string) => {
  if (!legacyUrl) return undefined;
  if (legacyUrl.startsWith('/legacy/')) return legacyUrl;
  if (legacyUrl.startsWith('/')) return `/legacy${legacyUrl}`;
  return `/legacy/${legacyUrl}`;
};

const inferLegacyModuleId = (legacySlug: string, trackSlug: string) => {
  if (trackSlug === 'pc-technician') {
    return legacySlug.startsWith('a-plus-lab-') ? 'pc-tech-labs' : 'pc-tech-legacy';
  }
  if (trackSlug === 'network-engineer') {
    return 'network-legacy';
  }
  return 'cybersecurity-legacy';
};

export const mapLessonToLegacyActivity = (lesson: CollectionEntry<'lessons'>) => {
  const labPath = toLegacyLabPath(lesson.data.legacyUrl);
  if (!labPath) return undefined;
  const normalized = normalizeLessonMeta(lesson.data);
  const track = lesson.data.track ?? inferLegacyTrackSlug(lesson.slug);
  const moduleId = inferLegacyModuleId(lesson.slug, track);
  return {
    slug: lesson.slug,
    type: 'activity' as const,
    title: lesson.data.title,
    description: lesson.data.description ?? 'Legacy page activity',
    track,
    moduleId,
    order: lesson.data.order ?? 999,
    difficulty: normalized.difficulty,
    estMinutes: normalized.estMinutes,
    labPath,
  };
};
