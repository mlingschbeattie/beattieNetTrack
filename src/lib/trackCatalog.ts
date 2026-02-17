import type { CollectionEntry } from 'astro:content';
import { normalizeLessonMeta } from './lessonMeta';

type LegacyTrackSlug = 'pc-technician' | 'network-engineer' | 'cybersecurity-engineer';

const networkKeywords = ['network', 'https-demo'];
const pcKeywords = [
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
  if (networkKeywords.some((keyword) => legacySlug.includes(keyword))) {
    return 'network-engineer';
  }
  if (pcKeywords.some((keyword) => legacySlug.startsWith(keyword) || legacySlug.includes(keyword))) {
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

export const inferLegacyModuleId = (legacySlug: string, trackSlug: string) => {
  if (trackSlug === 'pc-technician') {
    return legacySlug.startsWith('a-plus-lab-') ? 'pc-tech-labs' : 'pc-tech-legacy';
  }
  if (trackSlug === 'network-engineer') {
    return 'network-legacy';
  }
  return 'cybersecurity-legacy';
};

export const getDefaultModuleTitle = (moduleId: string) => {
  if (moduleId === 'pc-tech-labs') return 'Legacy Labs';
  if (moduleId === 'pc-tech-legacy') return 'Legacy Core Pages';
  if (moduleId === 'network-legacy') return 'Legacy Networking Pages';
  if (moduleId === 'cybersecurity-legacy') return 'Legacy Cybersecurity Pages';
  return 'Learning Module';
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
