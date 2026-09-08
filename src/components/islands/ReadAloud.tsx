import { useEffect, useRef, useState } from 'react';
import { getGuidedPreferences, setGuidedPreferences } from '../../lib/progressStore';

/**
 * Read-aloud control for Reading mode.
 *
 * This is the one genuinely useful piece of the retired Guided mode. Guided was
 * a 968-line auto-advancing carousel built around speechSynthesis that never
 * rendered the section check questions it was handed. Text-to-speech itself is
 * real accessibility value — for ESL students and anyone who reads slowly — so
 * it survives here as a single control rather than a whole mode with its own
 * settings panel.
 *
 * Reads the rendered lesson prose, so it stays in sync with what is on screen
 * and needs no separate narration script to maintain.
 */

type Props = {
  /** Selector for the element whose text should be read. */
  contentSelector?: string;
};

const RATES = [
  { value: 0.8, label: 'Slower' },
  { value: 1, label: 'Normal' },
  { value: 1.25, label: 'Faster' },
];

export default function ReadAloud({ contentSelector = '[data-reading-content]' }: Props) {
  const [supported, setSupported] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [rate, setRate] = useState(1);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  useEffect(() => {
    setSupported(typeof window !== 'undefined' && 'speechSynthesis' in window);
    // Reuse the existing narrationRate preference so a student's chosen speed
    // persists. The other guided.* fields are legacy — see progressStore.
    try {
      const saved = getGuidedPreferences().narrationRate;
      if (typeof saved === 'number' && Number.isFinite(saved)) setRate(saved);
    } catch {}
    // Speech continues across client-side navigation unless explicitly stopped.
    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const stop = () => {
    if (!supported) return;
    window.speechSynthesis.cancel();
    setSpeaking(false);
  };

  const start = () => {
    if (!supported) return;
    const el = document.querySelector<HTMLElement>(contentSelector);
    const text = (el?.innerText ?? '').trim();
    if (!text) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = rate;
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
    setSpeaking(true);
  };

  // Changing speed mid-playback restarts at the new rate; the Web Speech API
  // cannot retune an utterance that is already being spoken.
  const changeRate = (next: number) => {
    setRate(next);
    try {
      setGuidedPreferences({ narrationRate: next });
    } catch {}
    if (speaking) {
      window.speechSynthesis.cancel();
      const el = document.querySelector<HTMLElement>(contentSelector);
      const text = (el?.innerText ?? '').trim();
      if (!text) return;
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = next;
      utterance.onend = () => setSpeaking(false);
      utterance.onerror = () => setSpeaking(false);
      utteranceRef.current = utterance;
      window.speechSynthesis.speak(utterance);
    }
  };

  if (!supported) return null;

  return (
    <div className="read-aloud" data-testid="read-aloud">
      <button
        type="button"
        className={speaking ? 'btn-secondary' : 'btn-ghost'}
        onClick={speaking ? stop : start}
        aria-pressed={speaking}
      >
        <span aria-hidden="true">{speaking ? '■' : '▶'}</span>{' '}
        {speaking ? 'Stop reading' : 'Read aloud'}
      </button>

      <label className="read-aloud__rate">
        <span className="sr-only">Reading speed</span>
        <select
          value={rate}
          onChange={(e) => changeRate(Number(e.target.value))}
          aria-label="Reading speed"
        >
          {RATES.map((r) => (
            <option key={r.value} value={r.value}>
              {r.label}
            </option>
          ))}
        </select>
      </label>

      <span className="read-aloud__status" role="status" aria-live="polite">
        {speaking ? 'Reading this lesson aloud.' : ''}
      </span>
    </div>
  );
}
