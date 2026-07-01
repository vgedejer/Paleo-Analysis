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
 *  `sticky top-6` makes the panel follow the page as you scroll a long list:
 *  it scrolls normally until it reaches 1.5rem from the top, then pins there.
 *  `self-start` is what makes that possible inside the parent CSS grid — without
 *  it the panel would stretch to the full row height and have no room to travel.
 */
export function DetailPanel({ isOpen, onClose, placeholder, title = "Detail", children }: Props) {
  if (!isOpen) {
    return (
      <aside className="sticky top-6 hidden self-start rounded-xl border border-dashed border-fossil-100 p-6 text-center text-sm text-fossil-700/50 lg:block">
        {placeholder}
      </aside>
    );
  }

  return (
    <aside className="sticky top-6 self-start rounded-xl border border-fossil-100 bg-white p-5 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-fossil-900">{title}</h2>
        <button onClick={onClose} className="text-sm text-fossil-700/60 hover:text-fossil-900">
          Close ✕
        </button>
      </div>
      {children}
    </aside>
  );
}
