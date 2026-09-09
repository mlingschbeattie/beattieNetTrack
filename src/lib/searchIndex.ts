import { getCollection } from 'astro:content';

export type SearchIndexItem = {
  type: 'track' | 'lesson' | 'lab' | 'quiz';
  title: string;
  description: string;
  slug: string;
  href: string;
  /** Track title, shown on a result so overlapping topics stay distinguishable. */
  track?: string;
  /**
   * Extra matchable text: frontmatter tags plus the lesson's `## Key Terms`
   * line. Both are curated topic lists, which makes them far better search
   * fodder than raw body text — a lesson that teaches binary conversion names
   * it in Key Terms even when the title says "Number Systems".
   */
  keywords?: string;
};

/** Terms only, `·` separated, per the authoring standard. Capped so one long list cannot dominate the payload. */
const KEY_TERMS_CAP = 600;

const extractKeyTerms = (body: string | undefined): string => {
  if (!body) return '';
  const match = /^##\s+Key Terms\s*$/m.exec(body);
  if (!match) return '';
  const after = body.slice(match.index + match[0].length);
  // Stop at the next heading; Key Terms is normally the final section.
  const end = after.search(/^##\s+/m);
  const block = (end === -1 ? after : after.slice(0, end)).trim();
  return block.replace(/\s+/g, ' ').slice(0, KEY_TERMS_CAP);
};

const buildKeywords = (tags: unknown, body?: string): string => {
  const tagText = Array.isArray(tags) ? tags.join(' ') : '';
  return [tagText, extractKeyTerms(body)].filter(Boolean).join(' ').toLowerCase();
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
  const titleForTrack = (slug: string | undefined) =>
    slug ? trackTitleBySlug.get(slug) ?? slug : undefined;

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

  // Modules ride in the track group so they stay findable without a group of their own.
  for (const module of modules) {
    const trackTitle = titleForTrack(module.data.track) ?? module.data.track;
    items.push({
      type: 'track',
      title: module.data.title,
      description: module.data.description ? `${module.data.description} (Module in ${trackTitle})` : `Module in ${trackTitle}`,
      slug: module.slug,
      href: `/tracks/${module.data.track}`,
      track: trackTitle,
    });
  }

  for (const lesson of lessons) {
    items.push({
      type: 'lesson',
      title: lesson.data.title,
      description: lesson.data.description ?? '',
      slug: lesson.slug,
      href: `/lessons/${lesson.slug}`,
      track: titleForTrack(lesson.data.track),
      keywords: buildKeywords(lesson.data.tags, lesson.body),
    });
  }

  for (const lab of labs) {
    items.push({
      type: 'lab',
      title: lab.data.title,
      description: lab.data.description ?? '',
      slug: lab.slug,
      href: `/labs/${lab.slug}`,
      track: titleForTrack(lab.data.track),
      keywords: buildKeywords(lab.data.tags, lab.body),
    });
  }

  for (const quiz of quizzes) {
    items.push({
      type: 'quiz',
      title: quiz.data.title,
      description: quiz.data.description ?? '',
      slug: quiz.slug,
      href: `/quizzes/${quiz.slug}`,
      track: titleForTrack(quiz.data.track),
      keywords: buildKeywords(quiz.data.tags, quiz.body),
    });
  }

  return items.sort(compareSearchItems);
};
