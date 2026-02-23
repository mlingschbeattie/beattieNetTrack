import { getCollection } from 'astro:content';

export type SearchIndexItem = {
  type: 'track' | 'lesson' | 'lab' | 'quiz';
  title: string;
  description: string;
  slug: string;
  href: string;
};

const compareSearchItems = (a: SearchIndexItem, b: SearchIndexItem) => {
  return a.type.localeCompare(b.type) || a.title.localeCompare(b.title) || a.slug.localeCompare(b.slug);
};

export const getSearchIndexData = async (): Promise<SearchIndexItem[]> => {
  const [tracks, modules, lessons, labs, quizzes] = await Promise.all([
    getCollection('tracks'),
    getCollection('modules'),
    getCollection('lessons'),
    getCollection('labs'),
    getCollection('quizzes'),
  ]);

  const trackTitleBySlug = new Map(tracks.map((track) => [track.slug, track.data.title]));

  const items: SearchIndexItem[] = [];

  for (const track of tracks) {
    items.push({
      type: 'track',
      title: track.data.title,
      description: track.data.description ?? '',
      slug: track.slug,
      href: `/tracks/${track.slug}`,
    });
  }

  // Include module content in the global index while preserving the required item shape.
  for (const module of modules) {
    const trackTitle = trackTitleBySlug.get(module.data.track) ?? module.data.track;
    items.push({
      type: 'track',
      title: module.data.title,
      description: module.data.description ? `${module.data.description} (Module in ${trackTitle})` : `Module in ${trackTitle}`,
      slug: module.slug,
      href: `/tracks/${module.data.track}`,
    });
  }

  for (const lesson of lessons) {
    items.push({
      type: 'lesson',
      title: lesson.data.title,
      description: lesson.data.description ?? '',
      slug: lesson.slug,
      href: `/lessons/${lesson.slug}`,
    });
  }

  for (const lab of labs) {
    items.push({
      type: 'lab',
      title: lab.data.title,
      description: lab.data.description ?? '',
      slug: lab.slug,
      href: `/labs/${lab.slug}`,
    });
  }

  for (const quiz of quizzes) {
    items.push({
      type: 'quiz',
      title: quiz.data.title,
      description: quiz.data.description ?? '',
      slug: quiz.slug,
      href: `/quizzes/${quiz.slug}`,
    });
  }

  return items.sort(compareSearchItems);
};
