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
      className="group flex w-full min-w-0 flex-col items-start gap-3 border border-paleo-line bg-paleo-panel p-5 text-left transition-colors hover:bg-paleo-panel2 focus:outline-none focus-visible:ring-1 focus-visible:ring-paleo-accent"
    >
      <div className="w-full">
        <h3 className="font-cinzel text-lg uppercase tracking-wide text-paleo-cream transition-colors [overflow-wrap:anywhere] group-hover:text-paleo-accent">
          {genus.Genus}
        </h3>
        <div className="mt-1.5">
          <DietBadge diet={genus.Diet} />
        </div>
      </div>
      <dl className="grid w-full grid-cols-2 gap-x-3 gap-y-2 font-mono text-xs">
        <dt className="text-[10px] uppercase tracking-widest text-paleo-dim">Family</dt>
        <dd className="text-right text-paleo-cream">{genus.Family}</dd>
        <dt className="text-[10px] uppercase tracking-widest text-paleo-dim">Order</dt>
        <dd className="text-right text-paleo-cream">{genus.Order}</dd>
        <dt className="text-[10px] uppercase tracking-widest text-paleo-dim">Period</dt>
        <dd className="text-right text-paleo-cream">
          {genus.EarlyPeriod == genus.LatePeriod ? genus.EarlyPeriod : `${genus.EarlyPeriod} – ${genus.LatePeriod}`}
        </dd>
      </dl>
    </button>
  );
});
