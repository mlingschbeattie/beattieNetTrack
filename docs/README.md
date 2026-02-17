# Visual regression snapshots

## Update baseline images

1. Start from the site directory.
2. Run:
   - `npx playwright install`
   - `npm run test:visual -- --update-snapshots`

This regenerates screenshots for the three baseline routes: home, track, lesson.

## Review workflow

- Use `npm run test:visual` in CI to catch UI regressions.
- If intentional UI changes are made, update snapshots and commit them with the change.
