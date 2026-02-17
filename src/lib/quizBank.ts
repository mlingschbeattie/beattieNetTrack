export type QuizQuestion = {
  id: string;
  stem: string;
  options: string[];
  correctIndex: number;
  topicTag?: string;
  difficulty?: string;
  type?: string;
};

export type QuizCatalogEntry = {
  slug: string;
  title: string;
  questionCount: number;
};

type QuizModule = Record<string, unknown>;

type QuizBank = {
  slug: string;
  title: string;
  questions: QuizQuestion[];
};

let cachedBanks: QuizBank[] | null = null;

const toTitle = (slug: string) =>
  slug
    .replace(/-questions$/, '')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase())
    .replace(/\bA Plus\b/g, 'A+')
    .replace(/\bA\+\b/g, 'A+')
    .replace(/\bMs\b/g, 'MS')
    .replace(/\bOs\b/g, 'OS');

const isQuestionArray = (value: unknown): value is QuizQuestion[] =>
  Array.isArray(value) &&
  value.length > 0 &&
  typeof value[0] === 'object' &&
  value[0] !== null &&
  'stem' in (value[0] as Record<string, unknown>) &&
  'options' in (value[0] as Record<string, unknown>) &&
  'correctIndex' in (value[0] as Record<string, unknown>);

const extractQuestions = (mod: QuizModule): QuizQuestion[] => {
  for (const value of Object.values(mod)) {
    if (isQuestionArray(value)) return value;
  }
  return [];
};

const loadBanks = async () => {
  if (cachedBanks) return cachedBanks;
  const modules = import.meta.glob('../../../data/*-questions.js');
  const entries = Object.entries(modules);

  const banks = await Promise.all(
    entries.map(async ([filePath, loader]) => {
      const slug = filePath.split('/').pop()?.replace('-questions.js', '') ?? filePath;
      const mod = (await loader()) as QuizModule;
      const questions = extractQuestions(mod);
      return questions.length
        ? { slug, title: toTitle(slug), questions }
        : null;
    })
  );

  cachedBanks = banks
    .filter((bank): bank is QuizBank => Boolean(bank))
    .sort((a, b) => a.title.localeCompare(b.title));
  return cachedBanks;
};

export const getQuizCatalog = async (): Promise<QuizCatalogEntry[]> => {
  const banks = await loadBanks();
  return banks.map((bank) => ({
    slug: bank.slug,
    title: bank.title,
    questionCount: bank.questions.length,
  }));
};

export const getQuizQuestions = async (slug: string): Promise<QuizQuestion[]> => {
  const banks = await loadBanks();
  const bank = banks.find((entry) => entry.slug === slug);
  return bank?.questions ?? [];
};

export const getQuizTitle = async (slug: string): Promise<string> => {
  const banks = await loadBanks();
  return banks.find((entry) => entry.slug === slug)?.title ?? slug;
};
