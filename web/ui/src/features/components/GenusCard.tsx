import { memo } from "react";
import type { Genus } from "@/types/paleo";
import { DietBadge } from "@/components/ui/DietBadge";

interface GenusCardProps {
  genus: Genus;
  /** Behavior passed down from the parent — the child just reports the click. */
  onSelect: (id: number) => void;
}

/**
 * A single genus card.
 *
 * Wrapped in `React.memo`: this tells React to skip re-rendering the card when
 * its props are unchanged (compared shallowly). Why it matters here — when the
 * dashboard's search box updates on every keystroke, the PARENT re-renders, and
 * by default every child re-renders with it. `memo` lets unaffected cards bail
 * out. For this to actually help, the `onSelect` prop must be a STABLE function
 * reference across renders — which is exactly why the parent wraps it in
 * `useCallback` (see DinosaurDashboard). memo + unstable props = no benefit.
 *
 * Don't sprinkle memo everywhere preemptively, though: it has its own cost and
 * most components are cheap. Reach for it when you've identified a real hot path
 * (long lists, expensive subtrees) — a classic interview nuance.
 */
export const GenusCard = memo(function GenusCard({ genus, onSelect }: GenusCardProps) {
  return (
    <button
      onClick={() => onSelect(genus.id)}
      className="flex w-full flex-col items-start gap-2 rounded-xl border border-fossil-100 bg-white p-4 text-left shadow-sm transition hover:border-fossil-700/40 hover:shadow-md"
    >
      <div className="flex w-full items-center justify-between gap-2">
        <h3 className="font-semibold italic text-fossil-900">{genus.Genus}</h3>
        <DietBadge diet={genus.Diet} />
      </div>
      <dl className="grid w-full grid-cols-2 gap-x-3 gap-y-1 text-xs text-fossil-700">
        <dt className="text-fossil-700/60">Family</dt>
        <dd className="text-right">{genus.Family}</dd>
        <dt className="text-fossil-700/60">Order</dt>
        <dd className="text-right">{genus.Order}</dd>
        <dt className="text-fossil-700/60">Period</dt>
        <dd className="text-right">
          {genus.EarlyPeriod} – {genus.LatePeriod}
        </dd>
      </dl>
    </button>
  );
});
