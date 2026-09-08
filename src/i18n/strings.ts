/**
 * UI chrome translations for the Beattie learning ecosystem.
 *
 * SCOPE: interface chrome ONLY — navigation, controls, status labels.
 * Lesson and quiz CONTENT deliberately stays in English: CompTIA exams are
 * administered in English, so students must learn the English technical
 * vocabulary ("throughput", "kernel", "hypervisor"). Translating the interface
 * helps ESL students navigate; translating the technical content would train
 * them on terminology the exam will not use.
 *
 * ⚠️ REVIEW STATUS: the ar / fa / uk strings below were drafted by Claude and
 * are NOT yet verified by a fluent speaker. Have a native speaker review this
 * file before relying on it with students. English (en) is authoritative.
 *
 * Keys are grouped side by side so a reviewer can see every language for a
 * given string at once. Add a new language by adding its code to LANGUAGES in
 * ./index.ts and a key here for every entry.
 */

export type LangCode = 'en' | 'ar' | 'fa' | 'uk';

export type StringEntry = Record<LangCode, string>;

export const strings = {
  // --- Global navigation ---
  'nav.home': { en: 'Home', ar: 'الرئيسية', fa: 'خانه', uk: 'Головна' },
  'nav.tracks': { en: 'Learning Tracks', ar: 'المسارات التعليمية', fa: 'مسیرهای یادگیری', uk: 'Навчальні курси' },
  'nav.studyHub': { en: 'Study Hub', ar: 'مركز الدراسة', fa: 'مرکز مطالعه', uk: 'Навчальний центр' },
  'nav.activeTrack': { en: 'Active Track', ar: 'المسار النشط', fa: 'مسیر فعال', uk: 'Активний курс' },

  // --- Sidebar ---
  'sidebar.learningTracks': { en: 'Learning Tracks', ar: 'المسارات التعليمية', fa: 'مسیرهای یادگیری', uk: 'Навчальні курси' },
  'sidebar.lessons': { en: 'Lessons', ar: 'الدروس', fa: 'درس‌ها', uk: 'Уроки' },
  'sidebar.navigation': { en: 'Navigation', ar: 'التنقل', fa: 'ناوبری', uk: 'Навігація' },
  'sidebar.dashboard': { en: 'Dashboard', ar: 'لوحة التحكم', fa: 'داشبورد', uk: 'Панель' },
  'sidebar.done': { en: 'done', ar: 'مكتمل', fa: 'انجام‌شده', uk: 'виконано' },

  // --- Activity type labels ---
  'type.lesson': { en: 'Lesson', ar: 'درس', fa: 'درس', uk: 'Урок' },
  'type.quiz': { en: 'Quiz', ar: 'اختبار', fa: 'آزمون', uk: 'Тест' },
  'type.lab': { en: 'Lab', ar: 'مختبر', fa: 'آزمایشگاه', uk: 'Лабораторна' },

  // --- Workspace action bar ---
  'workspace.run': { en: 'Run', ar: 'تشغيل', fa: 'اجرا', uk: 'Запустити' },
  'workspace.check': { en: 'Check', ar: 'تحقق', fa: 'بررسی', uk: 'Перевірити' },
  'workspace.submit': { en: 'Submit', ar: 'إرسال', fa: 'ارسال', uk: 'Надіслати' },
  'workspace.reset': { en: 'Reset', ar: 'إعادة تعيين', fa: 'بازنشانی', uk: 'Скинути' },
  'workspace.instructions': { en: 'Instructions', ar: 'التعليمات', fa: 'دستورالعمل‌ها', uk: 'Інструкції' },
  'workspace.checks': { en: 'Checks', ar: 'الفحوصات', fa: 'بررسی‌ها', uk: 'Перевірки' },
  'workspace.notes': { en: 'Notes', ar: 'الملاحظات', fa: 'یادداشت‌ها', uk: 'Нотатки' },
  'workspace.hints': { en: 'Hints', ar: 'تلميحات', fa: 'راهنمایی‌ها', uk: 'Підказки' },
  'workspace.collapse': { en: 'Collapse', ar: 'طي', fa: 'جمع کردن', uk: 'Згорнути' },
  'workspace.expand': { en: 'Expand', ar: 'توسيع', fa: 'باز کردن', uk: 'Розгорнути' },

  // --- Lesson view toggle ---
  'lesson.learn': { en: 'Learn', ar: 'تعلم', fa: 'یادگیری', uk: 'Навчання' },
  'lesson.readAloud': { en: 'Read aloud', ar: 'قراءة بصوت عالٍ', fa: 'خواندن با صدای بلند', uk: 'Читати вголос' },
  'lesson.outline': { en: 'Outline', ar: 'المخطط', fa: 'رئوس مطالب', uk: 'Огляд' },
  'lesson.reading': { en: 'Reading', ar: 'القراءة', fa: 'خواندن', uk: 'Читання' },
  'lesson.markComplete': { en: 'Mark Complete', ar: 'وضع علامة مكتمل', fa: 'علامت‌گذاری به‌عنوان کامل', uk: 'Позначити виконаним' },
  'lesson.markIncomplete': { en: 'Mark Incomplete', ar: 'وضع علامة غير مكتمل', fa: 'علامت‌گذاری به‌عنوان ناقص', uk: 'Позначити невиконаним' },
  'lesson.checkIn': { en: 'Check-in', ar: 'تسجيل حضور', fa: 'ثبت حضور', uk: 'Відмітитися' },

  // --- Guided walkthrough ---
  'guided.walkthrough': { en: 'Guided Walkthrough', ar: 'شرح موجّه', fa: 'راهنمای گام‌به‌گام', uk: 'Покроковий огляд' },
  'guided.focusPoints': { en: 'Focus Points', ar: 'نقاط التركيز', fa: 'نکات کلیدی', uk: 'Ключові моменти' },
  'guided.quickRead': { en: 'Quick Read', ar: 'قراءة سريعة', fa: 'مطالعه سریع', uk: 'Швидке читання' },
  'guided.revealNext': { en: 'Reveal next', ar: 'إظهار التالي', fa: 'نمایش بعدی', uk: 'Показати наступне' },
  'guided.revealAll': { en: 'Reveal all', ar: 'إظهار الكل', fa: 'نمایش همه', uk: 'Показати все' },
  'guided.openInReading': { en: 'Open in reading', ar: 'فتح في وضع القراءة', fa: 'باز کردن در حالت خواندن', uk: 'Відкрити в режимі читання' },
  'guided.step': { en: 'Step', ar: 'خطوة', fa: 'گام', uk: 'Крок' },

  // --- Quiz ---
  'quiz.question': { en: 'Question', ar: 'سؤال', fa: 'سؤال', uk: 'Питання' },
  'quiz.of': { en: 'of', ar: 'من', fa: 'از', uk: 'з' },
  'quiz.pass': { en: 'Pass', ar: 'النجاح', fa: 'قبولی', uk: 'Прохідний бал' },
  'quiz.workspace': { en: 'Quiz workspace', ar: 'مساحة الاختبار', fa: 'فضای آزمون', uk: 'Робоча область тесту' },

  // --- Shared controls & status ---
  'common.back': { en: 'Back', ar: 'رجوع', fa: 'بازگشت', uk: 'Назад' },
  'common.next': { en: 'Next', ar: 'التالي', fa: 'بعدی', uk: 'Далі' },
  'common.previous': { en: 'Previous', ar: 'السابق', fa: 'قبلی', uk: 'Попереднє' },
  'common.openActivity': { en: 'Open Activity', ar: 'فتح النشاط', fa: 'باز کردن فعالیت', uk: 'Відкрити завдання' },
  'common.continueModule': { en: 'Continue Module', ar: 'متابعة الوحدة', fa: 'ادامه ماژول', uk: 'Продовжити модуль' },
  'common.inProgress': { en: 'In progress', ar: 'قيد التقدم', fa: 'در حال انجام', uk: 'У процесі' },
  'common.completed': { en: 'Completed', ar: 'مكتمل', fa: 'تکمیل‌شده', uk: 'Завершено' },
  'common.locked': { en: 'Locked', ar: 'مقفل', fa: 'قفل‌شده', uk: 'Заблоковано' },
  'common.moduleProgress': { en: 'Module Progress', ar: 'تقدم الوحدة', fa: 'پیشرفت ماژول', uk: 'Прогрес модуля' },

  // --- Theme & language controls ---
  'theme.light': { en: 'Light', ar: 'فاتح', fa: 'روشن', uk: 'Світла' },
  'theme.dark': { en: 'Dark', ar: 'داكن', fa: 'تیره', uk: 'Темна' },
  'theme.switchToLight': { en: 'Switch to light mode', ar: 'التبديل إلى الوضع الفاتح', fa: 'تغییر به حالت روشن', uk: 'Перемкнути на світлу тему' },
  'theme.switchToDark': { en: 'Switch to dark mode', ar: 'التبديل إلى الوضع الداكن', fa: 'تغییر به حالت تیره', uk: 'Перемкнути на темну тему' },
  'lang.label': { en: 'Language', ar: 'اللغة', fa: 'زبان', uk: 'Мова' },
} satisfies Record<string, StringEntry>;

export type StringKey = keyof typeof strings;
