import { useGenusFossils } from "../hooks/useFossils";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/ui/ErrorState";

/**
 * The fossil specimens excavated for a genus, rendered as its own section at the
 * bottom of the genus detail panel. It fetches its own data (keyed by genus
 * name) so the presentational GenusDetailPanel stays focused on the genus record
 * itself. Each specimen shows its fossil name, formation, and location.
 *
 * The list is capped in height and scrolls — a genus can have dozens of finds
 * (up to ~90), which would otherwise make the sticky panel unwieldy.
 */
export function GenusFossils({ genus }: { genus: string }) {
  const { data, isPending, isError, error, refetch } = useGenusFossils(genus);

  return (
    <section className="mt-6">
      <div className="flex items-baseline justify-between gap-2">
        <h4 className="font-cinzel text-sm uppercase tracking-wide text-paleo-cream">
          Fossil Specimens
        </h4>
        {data && (
          <span className="font-mono text-[10px] uppercase tracking-widest text-paleo-dim">
            {data.length} {data.length === 1 ? "find" : "finds"}
          </span>
        )}
      </div>

      <div className="mt-2">
        {isPending ? (
          <Spinner label="Locating specimens…" />
        ) : isError ? (
          <ErrorState message={error.message} onRetry={() => refetch()} />
        ) : data.length === 0 ? (
          <p className="border border-dashed border-paleo-line p-4 text-center font-mono text-[10px] uppercase tracking-[0.25em] text-paleo-dim">
            No fossil specimens recorded.
          </p>
        ) : (
          <ul className="max-h-72 overflow-y-auto pr-1">
            {data.map((f) => (
              <li key={f.id} className="border-b border-paleo-line py-3 last:border-0">
                <p className="font-crimson text-sm italic text-paleo-cream">{f.Fossil}</p>
                <div className="mt-1.5 space-y-1 font-mono text-[10px] uppercase tracking-wider">
                  <div className="flex justify-between gap-3">
                    <span className="text-paleo-dim">Formation</span>
                    <span className="text-right text-paleo-cream/80">{f.Formation}</span>
                  </div>
                  <div className="flex justify-between gap-3">
                    <span className="text-paleo-dim">Location</span>
                    <span className="text-right text-paleo-cream/80">
                      {f.State}, {f.Country}
                    </span>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
