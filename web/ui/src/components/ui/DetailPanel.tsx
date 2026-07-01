import type { ReactNode } from "react";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  /** Placeholder text shown (on large screens) when nothing is selected. */
  placeholder: string;
  /** Header title; defaults to "Detail". */
  title?: string;
  children: ReactNode;
}

/**
 * ============================================================================
 *  DetailPanel — the shared shell for every side detail panel.
 * ============================================================================
 *
 *  Both GenusDetailPanel and FossilDetailPanel (and any future one) wrap their
 *  body in this so the chrome lives in exactly one place: the card styling, the
 *  "Detail / Close" header, the empty-state placeholder, and — the reason this
 *  exists — the scroll behavior.
 *
 *  `sticky top-24` makes the panel follow the page as you scroll a long list:
 *  it scrolls normally until it reaches 6rem from the top — clearing the sticky
 *  app header — then pins there. `self-start` is what makes that possible inside
 *  the parent CSS grid — without it the panel would stretch to the full row
 *  height and have no room to travel.
 */
export function DetailPanel({ isOpen, onClose, placeholder, title = "Detail", children }: Props) {
  if (!isOpen) {
    return (
      <aside className="sticky top-24 hidden self-start border border-dashed border-paleo-line p-6 text-center font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim lg:block">
        {placeholder}
      </aside>
    );
  }

  return (
    <aside className="sticky top-24 self-start border border-paleo-line bg-paleo-panel p-5">
      <div className="mb-4 flex items-center justify-between border-b border-paleo-line pb-3">
        <h2 className="font-cinzel text-lg uppercase tracking-wide text-paleo-cream">{title}</h2>
        <button
          onClick={onClose}
          className="font-mono text-xs uppercase tracking-[0.2em] text-paleo-dim transition-colors hover:text-paleo-accent"
        >
          Close ✕
        </button>
      </div>
      {children}
    </aside>
  );
}
