import { strings, type LangCode, type StringKey } from './strings';

export { strings };
export type { LangCode, StringKey };

export type LanguageDef = {
  code: LangCode;
  /** Name shown in the switcher, written in that language. */
  nativeName: string;
  /** Short label for the compact switcher button. */
  short: string;
  dir: 'ltr' | 'rtl';
  /** English name, for aria-labels and admin surfaces. */
  englishName: string;
};

/**
 * The language registry. Adding a language means adding an entry here and a
 * value for every key in ./strings.ts — nothing else is wired by hand.
 */
export const LANGUAGES: LanguageDef[] = [
  { code: 'en', nativeName: 'English', short: 'EN', dir: 'ltr', englishName: 'English' },
  { code: 'ar', nativeName: 'العربية', short: 'ع', dir: 'rtl', englishName: 'Arabic' },
  { code: 'fa', nativeName: 'فارسی', short: 'فا', dir: 'rtl', englishName: 'Persian' },
  { code: 'uk', nativeName: 'Українська', short: 'УК', dir: 'ltr', englishName: 'Ukrainian' },
];

export const DEFAULT_LANG: LangCode = 'en';

export const LANG_CODES = LANGUAGES.map((l) => l.code);

export const isLangCode = (value: unknown): value is LangCode =>
  typeof value === 'string' && (LANG_CODES as string[]).includes(value);

export const getLanguage = (code: string): LanguageDef =>
  LANGUAGES.find((l) => l.code === code) ?? LANGUAGES[0];

export const dirFor = (code: string): 'ltr' | 'rtl' => getLanguage(code).dir;

/**
 * Look up a UI string. Falls back to English, then to the key itself, so a
 * missing translation degrades to readable English rather than blank UI.
 */
export const t = (key: StringKey, lang: string = DEFAULT_LANG): string => {
  const entry = strings[key];
  if (!entry) return key;
  return entry[lang as LangCode] || entry.en || key;
};

/** Serializable dictionary for one language, for the client-side applier. */
export const dictionaryFor = (lang: string): Record<string, string> => {
  const code = (isLangCode(lang) ? lang : DEFAULT_LANG) as LangCode;
  const out: Record<string, string> = {};
  for (const [key, entry] of Object.entries(strings)) {
    out[key] = (entry as Record<LangCode, string>)[code] || (entry as Record<LangCode, string>).en;
  }
  return out;
};

/** Every dictionary, for embedding once so switching needs no round trip. */
export const allDictionaries = (): Record<string, Record<string, string>> => {
  const out: Record<string, Record<string, string>> = {};
  for (const lang of LANG_CODES) out[lang] = dictionaryFor(lang);
  return out;
};
