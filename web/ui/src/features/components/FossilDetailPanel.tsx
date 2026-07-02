import { type UseQueryResult } from "@tanstack/react-query";
import type { FossilDetail } from "@/types/paleo";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/ui/ErrorState";
import { DetailPanel } from "@/components/ui/DetailPanel";
import { FindMap } from "@/components/ui/FindMap";

interface Props {
  /** The whole query object is passed in so this panel renders any state. */
  query: UseQueryResult<FossilDetail>;
  isOpen: boolean;
  onClose: () => void;
}

/** A labeled stat row — mirrors the one in GenusDetailPanel for visual parity. */
function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex justify-between gap-4 border-b border-paleo-line py-2 font-mono text-xs last:border-0">
      <span className="uppercase tracking-widest text-paleo-dim">{label}</span>
      <span className="text-right text-paleo-cream">{value}</span>
    </div>
  );
}

/**
 * Shows the full detail for the selected fossil, including a map of its find
 * site. Like GenusDetailPanel, it takes the query RESULT as a prop so the panel
 * stays presentational and easy to render in isolation.
 */
export function FossilDetailPanel({ query, isOpen, onClose }: Props) {
  const { data, isPending, isError, error, refetch } = query;

  return (
    <DetailPanel isOpen={isOpen} onClose={onClose} placeholder="Select a fossil to see details.">
      {isPending ? (
        <Spinner label="Loading detail…" />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : (
        <div>
          <h3 className="mb-4 font-cinzel text-2xl uppercase tracking-wide text-paleo-accent [overflow-wrap:anywhere]">
            {data.Fossil}
          </h3>
          <Stat label="Formation" value={data.Formation} />
          <Stat label="Member" value={data.Member} />
          <Stat label="Geological group" value={data.GeoGroup} />
          <Stat label="Location" value={`${data.State}, ${data.Country}`} />
          <Stat label="County" value={data.County} />
          <Stat label="Coordinates" value={`${data.Latitude.toFixed(3)}, ${data.Longitude.toFixed(3)}`} />
          <Stat
            label="Paleo-coordinates"
            value={`${data.PaleoLatitude.toFixed(3)}, ${data.PaleoLongitude.toFixed(3)}`}
          />

          <FindMap lat={data.Latitude} lon={data.Longitude} label={data.Fossil} />

          {data.GeoComments && (
            <p className="mt-4 font-crimson text-sm italic leading-relaxed text-paleo-dim">
              {data.GeoComments}
            </p>
          )}
        </div>
      )}
    </DetailPanel>
  );
}
