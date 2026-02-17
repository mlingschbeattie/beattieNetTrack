# Beattie Tech Astro Site

This is the new frontend architecture built with Astro + MDX + Content Collections. It lives alongside the legacy static site.

## Project structure

```text
site/
├── src/
│   ├── components/
│   ├── content/
│   │   ├── lessons/
│   │   └── tracks/
│   ├── layouts/
│   ├── pages/
│   └── styles/
├── scripts/
├── tests/
└── playwright.config.ts
```

## Dev commands

All commands run from the site folder:

| Command | Action |
| --- | --- |
| `npm install` | Install dependencies |
| `npm run dev` | Start the dev server at `localhost:4321` |
| `npm run build` | Build production output to `dist/` |
| `npm run preview` | Preview the production build |
| `npm run test:visual` | Run Playwright visual tests |
| `npm run lint` | Run Astro checks |
| `npm run format` | Format files with Prettier |
| `npm run format:check` | Check formatting without changes |

## Content authoring

Lessons live in `src/content/lessons/*.mdx` and are validated by Content Collections. Required frontmatter:

- `title`
- `description`
- `slug`
- `track`
- `order`
- `difficulty`
- `estMinutes`
- `tags`
- `legacyUrl` (optional for URL mapping)

Tracks live in `src/content/tracks/*.mdx` and define the lesson order via `lessons: [slug, ...]`.

## Add a lesson

1. Create a new MDX file under `src/content/lessons/`.
2. Fill out the frontmatter.
3. Add the lesson slug to the track file in `src/content/tracks/`.

## Legacy migration helper

Use the script to generate a stub MDX file with a TODO and embedded legacy HTML for reference:

```
node scripts/legacy-html-to-mdx.mjs --input ../a-plus-networking.html --output src/content/lessons/a-plus-networking.mdx
```

## URL strategy (legacy compatibility)

- Use `legacyUrl` in lesson frontmatter to preserve the original route.
- During migration, add redirects from legacy routes to `/lessons/[slug]` or `/tracks/[slug]`.
- Keep the legacy static site at the repo root until all routes are migrated.

## Visual regression tests

See docs in `docs/README.md` for snapshot updates.

## Workspace layout modes

`WorkspaceLayout.astro` supports two modes:

- `layoutMode="stacked"` → sticky top drawer with `Instructions | Checks | Notes`, large activity region (default for labs/quizzes).
- `layoutMode="split"` → two-column instructions/activity layout for reading-heavy pages.

You can override per page by passing the `layoutMode` prop.
