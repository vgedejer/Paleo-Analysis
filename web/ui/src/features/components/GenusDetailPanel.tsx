import { type UseQueryResult } from "@tanstack/react-query";
import type { GenusDetail } from "@/types/paleo";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/ui/ErrorState";
import { DietBadge } from "@/components/ui/DietBadge";
import { DetailPanel } from "@/components/ui/DetailPanel";

interface Props {
  /** The whole query object is passed in so this panel renders any state. */
  query: UseQueryResult<GenusDetail>;
  isOpen: boolean;
  onClose: () => void;
}

/** A labeled stat row — tiny local helper component, co-located for clarity. */
function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex justify-between gap-4 border-b border-paleo-line py-2 font-mono text-xs last:border-0">
      <span className="uppercase tracking-widest text-paleo-dim">{label}</span>
      <span className="text-right text-paleo-cream">{value}</span>
    </div>
  );
}

/**
 * Shows the full detail for the selected genus.
 *
 * Teaching point: this panel takes the query RESULT as a prop rather than
 * calling the hook itself. That keeps "which genus is selected" (parent's
 * concern) separate from "how to display a genus" (this component's concern),
 * and makes the panel easy to render in isolation (e.g. Storybook/tests) by
 * handing it a fake query object.
 */
export function GenusDetailPanel({ query, isOpen, onClose }: Props) {
  const { data, isPending, isError, error, refetch } = query;

  return (
    <DetailPanel isOpen={isOpen} onClose={onClose} placeholder="Select a genus to see details.">
      {isPending ? (
        <Spinner label="Loading detail…" />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : (
        <div>
          <div className="mb-4">
            <h3 className="font-cinzel text-2xl uppercase tracking-wide text-paleo-accent [overflow-wrap:anywhere]">
              {data.Genus}
            </h3>
            <div className="mt-2">
              <DietBadge diet={data.Diet} />
            </div>
          </div>
          <Stat label="Family" value={data.Family} />
          <Stat label="Suborder" value={data.Suborder} />
          <Stat label="Infraorder" value={data.Infraorder} />
          <Stat label="Order" value={data.Order} />
          <Stat label="Taxon size" value={data.TaxonSize} />
          <Stat label="Lifespan (MYA)" value={data.LifespanMYA.toFixed(1)} />
          <Stat label="Range (MYA)" value={`${data.MaxMYA} – ${data.MinMYA}`} />
          <Stat label="Early age" value={data.EarlyAge} />
          <Stat label="Late age" value={data.LateAge} />
        </div>
      )}
    </DetailPanel>
  );
}
