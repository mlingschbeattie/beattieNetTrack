# ADD_A_LAB

MVP process to add a new lab primitive in this platform.

## 1) Pick primitive type

- Terminal: use `TerminalSimulator`
- Code: use `CodeRunner`
- Quiz: use quiz content in `src/content/quizzes`
- Iframe simulation: use `LabFrame` + `public/labs/<slug>/index.html`

## 2) Add lab metadata

Create `src/content/labs/<slug>.mdx` with frontmatter:

- `title`, `description`, `slug`
- `track`, `module`, `order`
- `difficulty`, `estMinutes`
- Optional `labPath` for iframe labs

## 3) Add route page

Create `src/pages/labs/<slug>.astro` and wrap with `WorkspaceLayout`.

Set:

- `itemSlug` to lab slug
- `itemType="lab"`
- `checkLabel` / `submitLabel`
- `activity-main` slot with your primitive component

## 4) Hook actions to Workspace

Your island should listen for `workspace:action` and dispatch `workspace:result`:

```ts
window.addEventListener('workspace:action', (event) => {
  // handle run/check/submit/reset
});
window.dispatchEvent(new CustomEvent('workspace:result', {
  detail: { slug: '<lab-slug>', action: 'check', passed: true, progress: 100, message: 'OK' }
}));
```

## 5) Progress model

Use only `src/lib/progressStore.ts` (`markLabComplete`, `markLabIncomplete`, etc).

## 6) Styling

Use existing classes/tokens in `src/styles/global.css`.
Do not introduce a separate design system.

## 7) Verify

- `npm run lint`
- `npm run build`
- Add/update Playwright behavior test for the lab
