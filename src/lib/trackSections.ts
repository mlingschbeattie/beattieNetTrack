import type { CollectionEntry } from 'astro:content';

type RawSectionItem = string | { type: 'lesson' | 'lab' | 'quiz'; slug: string };

export type TrackSectionItem = {
  type: 'lesson' | 'lab' | 'quiz';
  slug: string;
};

export const normalizeSectionItem = (item: RawSectionItem): TrackSectionItem => {
  if (typeof item === 'string') {
    return { type: 'lesson', slug: item };
  }
  return item;
};

export const getTrackSectionItems = (track: CollectionEntry<'tracks'>): TrackSectionItem[] =>
  (track.data.sections ?? []).flatMap((section) =>
    (section.lessons ?? []).map((item) => normalizeSectionItem(item as RawSectionItem))
  );

export const getTrackSectionLessonSlugs = (track: CollectionEntry<'tracks'>): string[] =>
  getTrackSectionItems(track)
    .filter((item) => item.type === 'lesson')
    .map((item) => item.slug);

export const getTrackSectionItemCount = (track: CollectionEntry<'tracks'>): number =>
  (track.data.sections ?? []).reduce((total, section) => total + (section.lessons?.length ?? 0), 0);
