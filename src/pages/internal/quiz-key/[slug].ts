import type { APIRoute } from 'astro';
import { timingSafeEqual } from 'node:crypto';
import { loadQuizDefinition } from '../../../lib/quizKey';

// Answer keys for the hub's quiz grader, never for browsers. The hub proves itself with this
// app's shared key (HUB_APP_KEY, the lms entry in the hub's HUB_APP_KEYS). Anyone else gets
// the same 404 as a quiz that does not exist.
export const prerender = false;

function keyMatches(presented: string | null): boolean {
  const expected = process.env.HUB_APP_KEY ?? '';
  if (!presented || expected.length < 32) return false;
  const a = Buffer.from(presented);
  const b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}

const notFound = () =>
  new Response(JSON.stringify({ error: 'NOT_FOUND' }), { status: 404, headers: { 'content-type': 'application/json' } });

export const GET: APIRoute = async ({ params, request }) => {
  if (!keyMatches(request.headers.get('x-hub-app-key'))) return notFound();
  const quiz = await loadQuizDefinition(params.slug ?? '');
  if (!quiz || quiz.questions.length === 0) return notFound();
  return new Response(JSON.stringify(quiz), {
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });
};
