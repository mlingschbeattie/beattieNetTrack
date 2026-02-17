# ADD_A_TOUR_STEP

Tour steps live in `src/content/tour/*.mdx` and render via `/tour/[slug]`.

## 1) Add tour content entry

Create `src/content/tour/<slug>.mdx` with frontmatter:

- `title`, `description`, `slug`, `order`
- `kind`: `intro | terminal | quiz | code | complete`
- `next`: next step slug
- Optional by kind:
  - `terminalScenario`
  - `quizSlug`
  - `codeExercise`
  - `ctaLabel`

## 2) Reuse existing primitives

`/tour/[slug]` already maps `kind` to components:

- terminal → `TerminalSimulator`
- quiz → `QuizRunner`
- code → `CodeRunner`

No extra layout work is needed if frontmatter is correct.

## 3) Progress behavior

Tour progress is tracked separately inside the same canonical store via:

- `markTourStepComplete`
- `getTourPercent`

Tour id currently: `hands-on-tour`.

## 4) Continue flow

Set `next` so the page shows a continue CTA (`data-testid="tour-next-link"`).

## 5) Verify

- Visit `/tour`
- Complete the step interaction
- Click Continue to next slug
- Run Playwright tour behavior test
