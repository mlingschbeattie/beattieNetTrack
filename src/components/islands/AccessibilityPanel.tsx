import { useEffect, useRef, useState } from 'react';
import {
  A11Y_DEFAULTS,
  readA11y,
  setA11y,
  applyA11yToDocument,
  type A11yState,
  type MotionPref,
  type TextSize,
} from '../../lib/a11yStore';

/**
 * Student-facing accessibility controls.
 *
 * Opened from the top nav. Every change applies immediately and persists, so a
 * student can adjust and see the effect without hunting for a Save button.
 */
export default function AccessibilityPanel() {
  const [open, setOpen] = useState(false);
  const [state, setState] = useState<A11yState>(A11Y_DEFAULTS);
  const dialogRef = useRef<HTMLDivElement>(null);
  const openerRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const initial = readA11y();
    setState(initial);
    applyA11yToDocument(initial);
  }, []);

  // Close on Escape and keep focus inside the dialog while it is open.
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.stopPropagation();
        setOpen(false);
        openerRef.current?.focus();
        return;
      }
      if (event.key !== 'Tab' || !dialogRef.current) return;
      const focusable = dialogRef.current.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    document.addEventListener('keydown', onKey);
    const firstControl = dialogRef.current?.querySelector<HTMLElement>('button, input, select');
    firstControl?.focus();
    return () => document.removeEventListener('keydown', onKey);
  }, [open]);

  const update = (patch: Partial<A11yState>) => setState(setA11y(patch));

  const reset = () => {
    setState(setA11y(A11Y_DEFAULTS));
  };

  const Toggle = ({
    id,
    label,
    hint,
    checked,
    onChange,
  }: {
    id: string;
    label: string;
    hint: string;
    checked: boolean;
    onChange: (next: boolean) => void;
  }) => (
    <div className="a11y-row">
      <input
        type="checkbox"
        id={id}
        className="a11y-checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        aria-describedby={`${id}-hint`}
      />
      <div className="a11y-row__text">
        <label htmlFor={id} className="a11y-row__label">{label}</label>
        <p id={`${id}-hint`} className="a11y-row__hint">{hint}</p>
      </div>
    </div>
  );

  return (
    <>
      <button
        ref={openerRef}
        type="button"
        className="a11y-trigger"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-haspopup="dialog"
        aria-label="Accessibility and display settings"
        title="Accessibility settings"
      >
        <span aria-hidden="true">☰</span>
        <span className="a11y-trigger__text">Accessibility</span>
      </button>

      {open && (
        <>
          <div className="a11y-backdrop" onClick={() => setOpen(false)} aria-hidden="true" />
          <div
            ref={dialogRef}
            className="a11y-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="a11y-dialog-title"
          >
            <div className="a11y-dialog__head">
              <h2 id="a11y-dialog-title">Accessibility &amp; Display</h2>
              <button
                type="button"
                className="a11y-close"
                onClick={() => {
                  setOpen(false);
                  openerRef.current?.focus();
                }}
                aria-label="Close accessibility settings"
              >
                ✕
              </button>
            </div>

            <p className="a11y-dialog__intro">
              These settings are saved on this device and apply everywhere in the app.
            </p>

            <fieldset className="a11y-group">
              <legend>Motion</legend>
              <div className="a11y-segmented" role="radiogroup" aria-label="Motion">
                {(
                  [
                    ['system', 'Match device'],
                    ['reduced', 'Reduce motion'],
                    ['full', 'Allow motion'],
                  ] as Array<[MotionPref, string]>
                ).map(([value, label]) => (
                  <button
                    key={value}
                    type="button"
                    role="radio"
                    aria-checked={state.motion === value}
                    className={`a11y-seg ${state.motion === value ? 'a11y-seg--on' : ''}`}
                    onClick={() => update({ motion: value })}
                  >
                    {label}
                  </button>
                ))}
              </div>
              <p className="a11y-row__hint">
                Stops animations and transitions. Use “Reduce motion” if the device setting is not
                available to you.
              </p>
            </fieldset>

            <fieldset className="a11y-group">
              <legend>Text size</legend>
              <div className="a11y-segmented" role="radiogroup" aria-label="Text size">
                {(
                  [
                    ['default', 'Default'],
                    ['large', 'Large'],
                    ['larger', 'Largest'],
                  ] as Array<[TextSize, string]>
                ).map(([value, label]) => (
                  <button
                    key={value}
                    type="button"
                    role="radio"
                    aria-checked={state.textSize === value}
                    className={`a11y-seg ${state.textSize === value ? 'a11y-seg--on' : ''}`}
                    onClick={() => update({ textSize: value })}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </fieldset>

            <fieldset className="a11y-group">
              <legend>Visual calm</legend>
              <Toggle
                id="a11y-calm"
                label="Calm mode"
                hint="Removes glows, gradients, and shadows. Colors and contrast stay the same."
                checked={state.calmMode}
                onChange={(v) => update({ calmMode: v })}
              />
              <Toggle
                id="a11y-collapse"
                label="Collapse long lists"
                hint="Opens catalogs grouped and closed, so a page starts small instead of showing everything at once."
                checked={state.collapseCatalogs}
                onChange={(v) => update({ collapseCatalogs: v })}
              />
            </fieldset>

            <fieldset className="a11y-group">
              <legend>Reading</legend>
              <Toggle
                id="a11y-spacing"
                label="Readable spacing"
                hint="More space between lines and words, and shorter line lengths."
                checked={state.readableSpacing}
                onChange={(v) => update({ readableSpacing: v })}
              />
              <Toggle
                id="a11y-underline"
                label="Underline links"
                hint="Marks links with an underline instead of color alone."
                checked={state.underlineLinks}
                onChange={(v) => update({ underlineLinks: v })}
              />
            </fieldset>

            <div className="a11y-dialog__foot">
              <button type="button" className="btn-ghost" onClick={reset}>
                Reset to defaults
              </button>
            </div>
          </div>
        </>
      )}
    </>
  );
}
