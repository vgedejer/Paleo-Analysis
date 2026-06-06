import { type UseQueryResult } from "@tanstack/react-query";
import type { GenusDetail } from "@/types/paleo";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/ui/ErrorState";
import { DietBadge } from "@/components/ui/DietBadge";

interface Props {
  /** The whole query object is passed in so this panel renders any state. */
  query: UseQueryResult<GenusDetail>;
  isOpen: boolean;
  onClose: () => void;
}

/** A labeled stat row — tiny local helper component, co-located for clarity. */
function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex justify-between border-b border-fossil-100 py-1.5 text-sm last:border-0">
      <span className="text-fossil-700/60">{label}</span>
      <span className="font-medium text-fossil-900">{value}</span>
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
  if (!isOpen) {
    return (
      <aside className="hidden rounded-xl border border-dashed border-fossil-100 p-6 text-center text-sm text-fossil-700/50 lg:block">
        Select a genus to see details.
      </aside>
    );
  }

  const { data, isPending, isError, error, refetch } = query;

  return (
    <aside className="rounded-xl border border-fossil-100 bg-white p-5 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-fossil-900">Detail</h2>
        <button onClick={onClose} className="text-sm text-fossil-700/60 hover:text-fossil-900">
          Close ✕
        </button>
      </div>

      {isPending ? (
        <Spinner label="Loading detail…" />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : (
        <div>
          <div className="mb-3 flex items-center gap-2">
            <h3 className="text-xl font-bold italic text-fossil-900">{data.Genus}</h3>
            <DietBadge diet={data.Diet} />
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
    </aside>
  );
}
