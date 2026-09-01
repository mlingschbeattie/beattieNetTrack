import { useState } from 'react';

/**
 * Interactive ATX motherboard map for A+ / Tech+ component identification.
 *
 * Design notes:
 * - Geometry and hotspots come from ONE data source. The previous version kept
 *   the SVG rectangles and the hotspot dots in two separate hardcoded lists,
 *   so markers drifted off the parts they described.
 * - Every part is labeled ON the board. Hover-only tooltips meant a student had
 *   to find and hover eight dots before learning anything, and transient
 *   tooltips are poor for touch and for students who need information to stay
 *   put. Selecting a part pins its detail in a panel below.
 * - Parts are colour-coded by function with a legend, so the board reads as a
 *   board rather than a field of identical grey blocks.
 * - All colours are design tokens, so the diagram themes with the app. The old
 *   version hardcoded slate/navy values and stayed dark on a light page.
 */

type Category = 'cpu' | 'memory' | 'expansion' | 'storage' | 'power' | 'io';

type Part = {
  id: string;
  label: string;
  /** Short label drawn on the board; falls back to `label`. */
  short?: string;
  description: string;
  category: Category;
  /** Rect geometry in viewBox units. */
  x: number;
  y: number;
  w: number;
  h: number;
  /** Where the label sits relative to the rect. */
  labelPos?: 'inside' | 'above' | 'below' | 'right' | 'left';
};

const CATEGORIES: Record<Category, { label: string; token: string }> = {
  cpu: { label: 'Processor', token: 'var(--beattie-primary)' },
  memory: { label: 'Memory', token: 'var(--beattie-ai)' },
  expansion: { label: 'Expansion', token: 'var(--beattie-cyan)' },
  storage: { label: 'Storage', token: 'var(--beattie-success)' },
  power: { label: 'Power', token: 'var(--beattie-warning)' },
  io: { label: 'I/O & headers', token: 'var(--beattie-text-muted)' },
};

// Board occupies x 90..930, y 60..700 of a 960x760 viewBox (ATX is ~1.25:1).
const PARTS: Part[] = [
  {
    id: 'rear-io',
    label: 'Rear I/O Panel',
    short: 'REAR I/O',
    description:
      'USB, Ethernet, audio and video connectors that face out the back of the case. The I/O shield must be fitted to the case before the board is mounted.',
    category: 'io',
    x: 108, y: 84, w: 96, h: 190, labelPos: 'inside',
  },
  {
    id: 'cpu-8',
    label: '8-pin CPU Power (EPS)',
    short: '8-PIN CPU',
    description:
      'Dedicated 12V power for the processor, routed from the PSU to the top-left corner beside the VRM heatsinks. A build will not POST if this is left unplugged — a very common first-build mistake.',
    category: 'power',
    x: 300, y: 84, w: 120, h: 40, labelPos: 'below',
  },
  {
    id: 'vrm',
    label: 'VRM Heatsinks',
    short: 'VRM',
    description:
      'Voltage regulator modules step 12V down to the ~1.2V the CPU needs. They sit next to the socket and get hot under sustained load.',
    category: 'power',
    // 'below', not 'left': a left-anchored label collides with the Rear I/O block.
    x: 240, y: 150, w: 52, h: 150, labelPos: 'below',
  },
  {
    id: 'cpu-socket',
    label: 'CPU Socket',
    short: 'CPU SOCKET',
    description:
      'Seats the processor. Socket type (LGA1700, AM5, …) must match the CPU exactly — this is the single hardest compatibility rule in a build.',
    category: 'cpu',
    x: 320, y: 150, w: 190, h: 175, labelPos: 'inside',
  },
  {
    id: 'dimm-slots',
    label: 'DIMM Slots (RAM)',
    short: 'DIMM',
    description:
      'Holds memory modules. DDR generation must match the board and CPU — DDR4 will not fit a DDR5 slot. Populate matching colours first to enable dual-channel.',
    category: 'memory',
    x: 560, y: 140, w: 170, h: 200, labelPos: 'above',
  },
  {
    id: 'atx-24',
    label: '24-pin ATX Power',
    short: '24-PIN',
    description:
      'Main board power from the PSU. Runs down the right edge so the cable can be routed behind the motherboard tray.',
    category: 'power',
    x: 800, y: 150, w: 62, h: 170, labelPos: 'left',
  },
  {
    id: 'chipset',
    label: 'Chipset Heatsink',
    short: 'CHIPSET',
    description:
      'Covers the chipset, which handles communication between the CPU, storage, and expansion devices. Determines how many PCIe lanes and USB ports the board supports.',
    category: 'io',
    x: 620, y: 470, w: 130, h: 120, labelPos: 'inside',
  },
  {
    id: 'pcie-x16',
    label: 'PCIe x16 Slot',
    short: 'PCIe x16',
    description:
      'Primary graphics card slot — the long one closest to the CPU. Provides the most bandwidth; always seat the GPU here first.',
    category: 'expansion',
    x: 200, y: 420, w: 380, h: 34, labelPos: 'above',
  },
  {
    id: 'pcie-x1',
    label: 'PCIe x1 Slot',
    short: 'PCIe x1',
    description:
      'Short expansion slot for low-bandwidth cards such as capture, sound, or add-in network adapters.',
    category: 'expansion',
    x: 200, y: 600, w: 150, h: 30, labelPos: 'below',
  },
  {
    id: 'm2',
    label: 'M.2 / NVMe Slot',
    short: 'M.2',
    description:
      'Seats an NVMe SSD flat against the board. Far faster than SATA because it runs over PCIe lanes rather than the SATA bus.',
    category: 'storage',
    x: 200, y: 500, w: 330, h: 26, labelPos: 'below',
  },
  {
    id: 'sata',
    label: 'SATA Ports',
    short: 'SATA',
    description:
      'Right-angle connectors for SATA SSDs and hard drives. Each port carries one drive; data and power are separate cables.',
    category: 'storage',
    x: 820, y: 420, w: 60, h: 120, labelPos: 'left',
  },
  {
    id: 'front-panel',
    label: 'Front Panel Header',
    short: 'F_PANEL',
    description:
      'Tiny pins for the case power button, reset, and activity LEDs. Polarity matters for the LEDs, and the layout is printed in the board manual — the fiddliest connection in any build.',
    category: 'io',
    x: 700, y: 640, w: 150, h: 26, labelPos: 'above',
  },
];

const MOUNTING_HOLES = [
  [140, 120], [140, 400], [140, 660],
  [520, 120], [520, 400], [520, 660],
  [890, 120], [890, 400], [890, 660],
];

export default function MotherboardDiagram() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selected = PARTS.find((p) => p.id === selectedId) ?? null;

  const labelFor = (part: Part) => {
    const cx = part.x + part.w / 2;
    const cy = part.y + part.h / 2;
    switch (part.labelPos) {
      case 'above':
        return { x: cx, y: part.y - 10, anchor: 'middle' as const };
      case 'below':
        return { x: cx, y: part.y + part.h + 20, anchor: 'middle' as const };
      case 'left':
        return { x: part.x - 10, y: cy + 4, anchor: 'end' as const };
      case 'right':
        return { x: part.x + part.w + 10, y: cy + 4, anchor: 'start' as const };
      default:
        return { x: cx, y: cy + 4, anchor: 'middle' as const };
    }
  };

  return (
    <figure className="mb-diagram" data-testid="mb-diagram">
      <figcaption className="mb-diagram__caption">
        <span className="mb-diagram__title">Motherboard Map</span>
        <span className="mb-diagram__help">
          Select a part to read what it does. Use Tab and Enter to move through them.
        </span>
      </figcaption>

      <ul className="mb-legend" aria-label="Component categories">
        {Object.entries(CATEGORIES).map(([key, cat]) => (
          <li key={key} className="mb-legend__item">
            <span className="mb-legend__swatch" style={{ background: cat.token }} aria-hidden="true" />
            {cat.label}
          </li>
        ))}
      </ul>

      <div className="mb-diagram__frame">
        <svg
          className="mb-diagram__svg"
          viewBox="0 0 960 760"
          role="group"
          aria-label="ATX motherboard schematic. Rear I/O panel on the left, CPU socket upper centre, memory slots to its right, expansion slots along the lower half."
        >
          {/* PCB */}
          <rect x="90" y="60" width="840" height="640" rx="18" className="mb-board" />
          <rect x="106" y="76" width="808" height="608" rx="12" className="mb-board__inner" />

          {MOUNTING_HOLES.map(([cx, cy]) => (
            <circle key={`${cx}-${cy}`} cx={cx} cy={cy} r="9" className="mb-hole" />
          ))}

          {/* DIMM slot fins, drawn inside the DIMM group for realism */}
          {[0, 1, 2, 3].map((i) => (
            <rect
              key={`dimm-${i}`}
              x={566 + i * 42}
              y={146}
              width={26}
              height={188}
              rx="4"
              className="mb-detail"
            />
          ))}
          {/* SATA port stack */}
          {[0, 1, 2, 3].map((i) => (
            <rect
              key={`sata-${i}`}
              x={826}
              y={428 + i * 28}
              width={48}
              height={20}
              rx="3"
              className="mb-detail"
            />
          ))}

          {PARTS.map((part) => {
            const isSelected = part.id === selectedId;
            const tint = CATEGORIES[part.category].token;
            const lbl = labelFor(part);
            return (
              <g
                key={part.id}
                className={`mb-part ${isSelected ? 'mb-part--selected' : ''}`}
                role="button"
                tabIndex={0}
                aria-pressed={isSelected}
                aria-label={`${part.label}. ${CATEGORIES[part.category].label}.`}
                onClick={() => setSelectedId(isSelected ? null : part.id)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    setSelectedId(isSelected ? null : part.id);
                  }
                }}
              >
                <rect
                  x={part.x}
                  y={part.y}
                  width={part.w}
                  height={part.h}
                  rx="6"
                  className="mb-part__rect"
                  style={{ stroke: tint, fill: tint }}
                />
                <text x={lbl.x} y={lbl.y} textAnchor={lbl.anchor} className="mb-part__label">
                  {part.short ?? part.label}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="mb-detail-panel" aria-live="polite">
        {selected ? (
          <>
            <div className="mb-detail-panel__head">
              <span
                className="mb-legend__swatch"
                style={{ background: CATEGORIES[selected.category].token }}
                aria-hidden="true"
              />
              <strong>{selected.label}</strong>
              <span className="mb-detail-panel__cat">{CATEGORIES[selected.category].label}</span>
            </div>
            <p className="mb-detail-panel__body">{selected.description}</p>
          </>
        ) : (
          <p className="mb-detail-panel__empty">
            No part selected. Choose a component on the board to see what it does and why it matters
            in a build.
          </p>
        )}
      </div>

      <style>{`
        .mb-diagram { margin: 0; display: grid; gap: var(--space-4); }

        .mb-diagram__caption { display: grid; gap: 2px; }
        .mb-diagram__title { font-weight: 600; color: var(--beattie-text); }
        .mb-diagram__help { font-size: var(--text-xs); color: var(--beattie-text-muted); }

        .mb-legend {
          display: flex; flex-wrap: wrap; gap: var(--space-3);
          margin: 0; padding: 0; list-style: none;
        }
        .mb-legend__item {
          display: inline-flex; align-items: center; gap: var(--space-2);
          font-size: var(--text-xs); color: var(--beattie-text-muted);
        }
        .mb-legend__swatch {
          width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0;
        }

        .mb-diagram__frame {
          width: 100%;
          border-radius: var(--radius-md);
          border: 1px solid var(--beattie-border);
          background: var(--beattie-surface-elevated);
          padding: var(--space-3);
          overflow-x: auto;
        }
        .mb-diagram__svg { width: 100%; min-width: 420px; height: auto; display: block; }

        .mb-board { fill: var(--beattie-surface-subtle); stroke: var(--beattie-border); stroke-width: 2; }
        .mb-board__inner { fill: none; stroke: var(--beattie-border-subtle); stroke-width: 1; stroke-dasharray: 4 6; }
        .mb-hole { fill: var(--beattie-surface-elevated); stroke: var(--beattie-border); stroke-width: 2; }
        .mb-detail { fill: var(--beattie-surface-elevated); opacity: 0.75; }

        .mb-part { cursor: pointer; }
        .mb-part__rect {
          fill-opacity: 0.18;
          stroke-width: 2;
          transition: fill-opacity var(--transition-fast);
        }
        .mb-part:hover .mb-part__rect { fill-opacity: 0.34; }
        .mb-part--selected .mb-part__rect { fill-opacity: 0.45; stroke-width: 3.5; }

        .mb-part__label {
          fill: var(--beattie-text);
          font-family: var(--font-mono);
          font-size: 15px;
          font-weight: 700;
          letter-spacing: 0.04em;
          pointer-events: none;
        }

        .mb-part:focus-visible { outline: none; }
        .mb-part:focus-visible .mb-part__rect {
          stroke: var(--beattie-border-active);
          stroke-width: 4;
        }

        .mb-detail-panel {
          min-height: 5.5rem;
          padding: var(--space-4);
          border: 1px solid var(--beattie-border);
          border-radius: var(--radius-md);
          background: var(--beattie-surface);
        }
        .mb-detail-panel__head {
          display: flex; align-items: center; gap: var(--space-2);
          margin-bottom: var(--space-2); color: var(--beattie-text);
        }
        .mb-detail-panel__cat {
          font-size: var(--text-xs); color: var(--beattie-text-muted);
          border: 1px solid var(--beattie-border);
          border-radius: var(--radius-pill);
          padding: 1px var(--space-2);
        }
        .mb-detail-panel__body {
          margin: 0; color: var(--beattie-text-muted);
          font-size: var(--text-sm); line-height: var(--leading-normal);
        }
        .mb-detail-panel__empty {
          margin: 0; color: var(--beattie-text-dim);
          font-size: var(--text-sm);
        }
      `}</style>
    </figure>
  );
}
