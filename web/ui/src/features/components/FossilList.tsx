import { useMemo, useState } from "react";
import { useFossils, useFossilDetail } from "../hooks/useFossils";
import { useGenera } from "../hooks/useGenera";
import type { FossilFilter } from "../api/fossilsApi";
import { FossilDetailPanel } from "./FossilDetailPanel";
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
  // Local, uncommitted input text vs. the committed filter we actually query
  // with. Separating them means we fetch on submit, not on every keystroke —
  // avoiding a request per character against the backend.
  const [genusInput, setGenusInput] = useState("");
  const [filter, setFilter] = useState<FossilFilter>(undefined);
  const [showSuggestions, setShowSuggestions] = useState(false);
  // Which suggestion the arrow keys have highlighted; -1 = none highlighted.
  const [activeIndex, setActiveIndex] = useState(-1);
  // Which fossil row is selected for the detail panel (local, like GenusList).
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const { data: fossils, isPending, isFetching, isError, error, refetch } = useFossils(filter);

  // Dependent query: idle until a row is selected, then fetches that fossil.
  const detailQuery = useFossilDetail(selectedId);

  // Autocomplete source: the full genus list, fetched (and cached) once. We
  // derive prefix-matched suggestions from it rather than hitting the backend
  // for every keystroke.
  const { data: genera } = useGenera();

  const suggestions = useMemo(() => {
    const needle = genusInput.trim().toLowerCase();
    if (needle === "" || !genera) return [];
    const matches = genera
      .map((g) => g.Genus)
      .filter((name) => name.toLowerCase().startsWith(needle))
      .slice(0, 8);
    // Nothing useful to suggest if the sole match is exactly what's typed.
    if (matches.length === 1 && matches[0]?.toLowerCase() === needle) return [];
    return matches;
  }, [genera, genusInput]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFilter(genusInput.trim() === "" ? undefined : { by: "genus", value: genusInput.trim() });
  }

  // Selecting a suggestion both fills the input and commits the filter — same
  // effect as submitting the form. Used by both click and keyboard (Enter).
  function selectSuggestion(name: string) {
    setGenusInput(name);
    setFilter({ by: "genus", value: name });
    setShowSuggestions(false);
    setActiveIndex(-1);
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (!showSuggestions || suggestions.length === 0) return;
    if (e.key === "ArrowDown") {
      e.preventDefault(); // keep the cursor from jumping to the input's end
      setActiveIndex((i) => (i + 1) % suggestions.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActiveIndex((i) => (i - 1 + suggestions.length) % suggestions.length);
    } else if (e.key === "Enter" && activeIndex >= 0) {
      // A suggestion is highlighted — pick it instead of submitting raw input.
      e.preventDefault();
      const name = suggestions[activeIndex];
      if (name) selectSuggestion(name);
    } else if (e.key === "Escape") {
      setShowSuggestions(false);
      setActiveIndex(-1);
    }
  }

  return (
    <section className="space-y-4">
      <div className="relative">
        <form onSubmit={handleSubmit}>
        <input
          type="search"
          value={genusInput}
          onChange={(e) => {
            setGenusInput(e.target.value);
            setShowSuggestions(true);
            setActiveIndex(-1); // typing invalidates the highlighted row
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setShowSuggestions(false)}
          placeholder="Filter fossils by genus (e.g. Tyrannosaurus)…"
          className="w-full rounded-lg border border-fossil-100 px-3 py-2 text-sm outline-none focus:border-fossil-700/50"
        />
        </form>

        {showSuggestions && suggestions.length > 0 && (
          // `onMouseDown` fires before the input's `blur`, so preventing its
          // default keeps focus on the input long enough for the click below to
          // register (otherwise blur would unmount this list first).
          <ul
            onMouseDown={(e) => e.preventDefault()}
            className="absolute z-10 mt-1 w-full overflow-hidden rounded-lg border border-fossil-100 bg-white shadow-sm"
          >
            {suggestions.map((name, i) => (
              <li key={name}>
                <button
                  type="button"
                  onClick={() => selectSuggestion(name)}
                  onMouseEnter={() => setActiveIndex(i)}
                  className={`block w-full px-3 py-2 text-left text-sm text-fossil-900 ${
                    i === activeIndex ? "bg-fossil-100" : "hover:bg-fossil-50"
                  }`}
                >
                  {name}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

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
        <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
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
                  <tr
                    key={f.id}
                    onClick={() => setSelectedId(f.id)}
                    className={`cursor-pointer border-t border-fossil-100 ${
                      f.id === selectedId ? "bg-fossil-100" : "hover:bg-fossil-50/50"
                    }`}
                  >
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

          {/* Detail side panel — driven by the dependent query. */}
          <FossilDetailPanel
            query={detailQuery}
            isOpen={selectedId !== null}
            onClose={() => setSelectedId(null)}
          />
        </div>
      )}
    </section>
  );
}
