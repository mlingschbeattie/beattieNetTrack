/**
 * Server-only: builds a quiz's full definition, answers included. Pages send students
 * toPublicQuiz(...) instead; the answers go only to the hub, which grades submissions
 * (see src/pages/internal/quiz-key/[slug].ts).
 */
import { getCollection, type CollectionEntry } from 'astro:content';
import fs from 'node:fs/promises';
import path from 'node:path';
import type { QuizDefinition, QuizQuestion } from './quizEngine';

async function questionsFromJson(quizJsonPath: string): Promise<QuizQuestion[]> {
  const diskPath = path.join(process.cwd(), 'public', quizJsonPath.replace(/^\//, ''));
  try {
    const parsed = JSON.parse(await fs.readFile(diskPath, 'utf8')) as {
      questions?: Array<{ prompt?: string; choices?: string[]; answerIndex?: number; explanation?: string }>;
    };
    return Array.isArray(parsed.questions)
      ? parsed.questions
          .filter((item) => typeof item.prompt === 'string' && Array.isArray(item.choices) && typeof item.answerIndex === 'number')
          .map((item, index) => ({
            id: `q${index + 1}`,
            type: 'single' as const,
            prompt: item.prompt as string,
            options: item.choices as string[],
            correctIndex: item.answerIndex as number,
            explanation: item.explanation,
          }))
      : [];
  } catch {
    return [];
  }
}

export async function quizDefinitionFromEntry(quiz: CollectionEntry<'quizzes'>): Promise<QuizDefinition> {
  let questions: QuizQuestion[] = quiz.data.questions ?? [];
  if (questions.length === 0 && quiz.data.quizJsonPath) {
    questions = await questionsFromJson(quiz.data.quizJsonPath);
  }
  return {
    slug: quiz.slug,
    title: quiz.data.title,
    description: quiz.data.description,
    passThreshold: quiz.data.passThreshold,
    questions,
  };
}

export async function loadQuizDefinition(slug: string): Promise<QuizDefinition | null> {
  const quizzes = await getCollection('quizzes');
  const quiz = quizzes.find((item) => item.slug === slug);
  return quiz ? quizDefinitionFromEntry(quiz) : null;
}
