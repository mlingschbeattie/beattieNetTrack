import { useState } from 'react';

type Hotspot = {
  id: string;
  label: string;
  description: string;
  x: number;
  y: number;
};

const hotspots: Hotspot[] = [
  { id: 'cpu-socket', label: 'CPU Socket', description: 'Seats the processor. Socket compatibility is mandatory.', x: 41, y: 33 },
  { id: 'dimm-slots', label: 'DIMM Slots', description: 'Holds system memory modules. Match DDR generation and capacity.', x: 64, y: 30 },
  { id: 'pcie-x16', label: 'PCIe x16', description: 'Primary graphics card slot. Bandwidth affects GPU performance.', x: 45, y: 58 },
  { id: 'sata', label: 'SATA Ports', description: 'Connects SATA SSD/HDD drives for additional storage.', x: 72, y: 69 },
  { id: 'm2', label: 'M.2 Slot', description: 'High-speed NVMe SSD connector for fast boot and load times.', x: 58, y: 52 },
  { id: 'atx-24', label: '24-pin ATX', description: 'Main motherboard power connector from the PSU.', x: 84, y: 40 },
  { id: 'cpu-8', label: '8-pin CPU', description: 'Dedicated CPU power connector near VRMs and socket.', x: 18, y: 18 },
  { id: 'front-panel', label: 'Front Panel Header', description: 'Wires case power/reset/LED controls to the board.', x: 20, y: 78 },
];

export default function MotherboardDiagram() {
  const [activeHotspotId, setActiveHotspotId] = useState<string | null>(null);

  return (
    <figure className="mb-diagram" data-testid="mb-diagram" aria-label="Motherboard map with interactive hotspots">
      <figcaption className="mb-diagram__caption">Motherboard Map</figcaption>
      <div className="mb-diagram__frame">
        <svg
          className="mb-diagram__svg"
          viewBox="0 0 960 540"
          role="img"
          aria-label="Motherboard schematic showing major connectors and slots"
        >
          <rect x="40" y="30" width="880" height="480" rx="14" className="mb-board" />
          <rect x="300" y="120" width="220" height="180" rx="10" className="mb-chip" />
          <rect x="560" y="110" width="50" height="220" rx="6" className="mb-slot" />
          <rect x="620" y="110" width="50" height="220" rx="6" className="mb-slot" />
          <rect x="680" y="110" width="50" height="220" rx="6" className="mb-slot" />
          <rect x="740" y="110" width="50" height="220" rx="6" className="mb-slot" />
          <rect x="350" y="300" width="360" height="42" rx="6" className="mb-slot-wide" />
          <rect x="520" y="250" width="180" height="28" rx="4" className="mb-slot-wide" />
          <rect x="730" y="355" width="130" height="24" rx="4" className="mb-port" />
          <rect x="730" y="388" width="130" height="24" rx="4" className="mb-port" />
          <rect x="775" y="170" width="95" height="120" rx="8" className="mb-port" />
          <rect x="120" y="70" width="110" height="36" rx="6" className="mb-port" />
          <rect x="130" y="410" width="170" height="20" rx="4" className="mb-port" />
        </svg>

        {hotspots.map((hotspot) => {
          const tooltipId = `mb-tip-${hotspot.id}`;
          const isPinned = activeHotspotId === hotspot.id;
          return (
            <button
              key={hotspot.id}
              type="button"
              className="mb-diagram__hotspot"
              style={{ left: `${hotspot.x}%`, top: `${hotspot.y}%` }}
              aria-label={hotspot.label}
              aria-describedby={tooltipId}
              data-active={isPinned ? 'true' : 'false'}
              onClick={() => setActiveHotspotId((prev) => (prev === hotspot.id ? null : hotspot.id))}
            >
              <span className="mb-diagram__dot" aria-hidden="true" />
              <span className="mb-diagram__tooltip" role="tooltip" id={tooltipId}>
                <strong>{hotspot.label}</strong>
                <span>{hotspot.description}</span>
              </span>
            </button>
          );
        })}
      </div>

      <style>{`
        .mb-diagram { margin: 0; }
        .mb-diagram__caption {
          font-weight: 600;
          margin-bottom: 0.75rem;
          color: var(--color-text, #e5e7eb);
        }
        .mb-diagram__frame {
          position: relative;
          width: 100%;
          aspect-ratio: 16 / 9;
          border-radius: 12px;
          border: 1px solid rgba(148, 163, 184, 0.28);
          background: rgba(15, 23, 42, 0.45);
          overflow: hidden;
        }
        .mb-diagram__svg {
          width: 100%;
          height: 100%;
          display: block;
        }
        .mb-board { fill: rgba(30, 41, 59, 0.86); stroke: rgba(148, 163, 184, 0.45); stroke-width: 2; }
        .mb-chip { fill: rgba(51, 65, 85, 0.95); stroke: rgba(148, 163, 184, 0.5); stroke-width: 2; }
        .mb-slot { fill: rgba(71, 85, 105, 0.9); }
        .mb-slot-wide { fill: rgba(51, 65, 85, 0.9); }
        .mb-port { fill: rgba(100, 116, 139, 0.82); }

        .mb-diagram__hotspot {
          position: absolute;
          transform: translate(-50%, -50%);
          width: 1.35rem;
          height: 1.35rem;
          border: 0;
          border-radius: 999px;
          background: transparent;
          padding: 0;
          cursor: pointer;
        }
        .mb-diagram__dot {
          display: block;
          width: 100%;
          height: 100%;
          border-radius: 999px;
          border: 2px solid rgba(248, 250, 252, 0.9);
          background: rgba(59, 130, 246, 0.85);
          box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.25);
        }
        .mb-diagram__hotspot:focus-visible {
          outline: 2px solid rgba(248, 250, 252, 0.9);
          outline-offset: 2px;
        }
        .mb-diagram__tooltip {
          position: absolute;
          left: 50%;
          bottom: calc(100% + 10px);
          transform: translateX(-50%);
          width: 220px;
          max-width: min(220px, 72vw);
          background: rgba(15, 23, 42, 0.95);
          border: 1px solid rgba(148, 163, 184, 0.35);
          color: #e2e8f0;
          border-radius: 8px;
          padding: 0.5rem 0.625rem;
          display: grid;
          gap: 0.25rem;
          font-size: 0.78rem;
          line-height: 1.35;
          opacity: 0;
          pointer-events: none;
          visibility: hidden;
          z-index: 2;
        }
        .mb-diagram__tooltip strong {
          font-size: 0.8rem;
          font-weight: 600;
        }
        .mb-diagram__hotspot:hover .mb-diagram__tooltip,
        .mb-diagram__hotspot:focus-visible .mb-diagram__tooltip,
        .mb-diagram__hotspot[data-active='true'] .mb-diagram__tooltip {
          opacity: 1;
          visibility: visible;
        }
      `}</style>
    </figure>
  );
}
