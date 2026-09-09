import type { APIRoute } from 'astro';
import { getSearchIndexData } from '../lib/searchIndex';

/**
 * The search index used to be inlined into every page as a JSON script tag,
 * which put ~51 KB on every request whether or not anyone opened search.
 * Serving it here instead means the cost is paid once, on first search-open,
 * by the people who actually search — and it lifts the size ceiling enough to
 * index tags and Key Terms rather than titles alone.
 */
export const prerender = true;

export const GET: APIRoute = async () => {
  const data = await getSearchIndexData();
  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
};
