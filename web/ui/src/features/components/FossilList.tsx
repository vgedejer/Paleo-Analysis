import { useEffect, useState } from "react";
import { useFossils } from "../hooks/useFossils";
import type { FossilFilter } from "../api/fossilsApi";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/ui/ErrorState";

/**
 * ============================================================================
 *  FossilList — a second core view, demonstrating filtered/parameterized fetch.
 * ============================================================================
 *
 *  Where DinosaurDashboard filters data CLIENT-side (fetch all, then filter in
 *  memory), this view filters SERVER-side: the genus typed here becomes a query
 *  param and the backend returns only matching fossils. Knowing when to do which
 *  is a real architecture decision — see the README trade-offs section.
 */
export function FossilList() {
  // Local input text vs. the committed filter we actually query with. The list
  // auto-updates as you type: a debounce delays committing the filter until
  // typing pauses, so we don't fire a request per keystroke against the backend.
  const [genusInput, setGenusInput] = useState("");
  const [filter, setFilter] = useState<FossilFilter>(undefined);

  const { data: fossils, isPending, isFetching, isError, error, refetch } = useFossils(filter);

  // Debounce: whenever the input changes, schedule the filter update 300ms out.
  // If the user keeps typing, the cleanup cancels the pending timer and a fresh
  // one is scheduled — so the filter only commits once typing settles.
  useEffect(() => {
    const id = setTimeout(() => {
      const value = genusInput.trim();
      setFilter(value === "" ? undefined : { by: "genus", value });
    }, 300);
    return () => clearTimeout(id);
  }, [genusInput]);

  return (
    <section className="space-y-4">
      <input
        type="search"
        value={genusInput}
        onChange={(e) => setGenusInput(e.target.value)}
        placeholder="Filter fossils by genus (e.g. Tyrannosaurus)…"
        className="w-full rounded-lg border border-fossil-100 px-3 py-2 text-sm outline-none focus:border-fossil-700/50"
      />

      {/* `isFetching` (vs `isPending`) lets us show a subtle refetch indicator
          while still displaying the previous results — a smoother UX than
          blanking the list on every new query. */}
      {isFetching && !isPending && <p className="text-xs text-fossil-700/60">Updating…</p>}

      {isPending ? (
        <Spinner label="Sifting sediment…" />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : fossils.length === 0 ? (
        <p className="rounded-lg border border-dashed border-fossil-100 p-8 text-center text-sm text-fossil-700/60">
          No fossils found.
        </p>
      ) : (
        <div className="overflow-hidden rounded-xl border border-fossil-100">
          <table className="w-full text-sm">
            <thead className="bg-fossil-50 text-left text-xs uppercase tracking-wide text-fossil-700/70">
              <tr>
                <th className="px-4 py-2 font-medium">Fossil</th>
                <th className="px-4 py-2 font-medium">Formation</th>
                <th className="px-4 py-2 font-medium">Location</th>
                <th className="px-4 py-2 text-right font-medium">Lat / Lon</th>
              </tr>
            </thead>
            <tbody>
              {fossils.map((f) => (
                <tr key={f.id} className="border-t border-fossil-100 hover:bg-fossil-50/50">
                  <td className="px-4 py-2 font-medium text-fossil-900">{f.Fossil}</td>
                  <td className="px-4 py-2 text-fossil-700">{f.Formation}</td>
                  <td className="px-4 py-2 text-fossil-700">
                    {f.State}, {f.Country}
                  </td>
                  <td className="px-4 py-2 text-right font-mono text-xs text-fossil-700/70">
                    {f.Latitude.toFixed(2)}, {f.Longitude.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
