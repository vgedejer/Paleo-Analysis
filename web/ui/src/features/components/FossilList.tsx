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
          className="w-full border border-paleo-line bg-paleo-panel px-3 py-2 font-mono text-sm text-paleo-cream outline-none transition-colors placeholder:text-paleo-dim focus:border-paleo-accent"
        />
        </form>

        {showSuggestions && suggestions.length > 0 && (
          // `onMouseDown` fires before the input's `blur`, so preventing its
          // default keeps focus on the input long enough for the click below to
          // register (otherwise blur would unmount this list first).
          <ul
            onMouseDown={(e) => e.preventDefault()}
            className="absolute z-10 mt-1 w-full overflow-hidden border border-paleo-line bg-paleo-panel"
          >
            {suggestions.map((name, i) => (
              <li key={name}>
                <button
                  type="button"
                  onClick={() => selectSuggestion(name)}
                  onMouseEnter={() => setActiveIndex(i)}
                  className={`block w-full px-3 py-2 text-left font-mono text-sm transition-colors ${
                    i === activeIndex
                      ? "bg-paleo-panel2 text-paleo-accent"
                      : "text-paleo-cream hover:bg-paleo-panel2"
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
      {isFetching && !isPending && (
        <p className="font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim">Updating…</p>
      )}

      {isPending ? (
        <Spinner label="Sifting sediment…" />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : fossils.length === 0 ? (
        <p className="border border-dashed border-paleo-line p-8 text-center font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim">
          No fossils found.
        </p>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="overflow-hidden border border-paleo-line">
            <table className="w-full text-sm">
              <thead className="border-b border-paleo-line bg-paleo-panel2 text-left font-mono text-[10px] uppercase tracking-[0.2em] text-paleo-dim">
                <tr>
                  <th className="px-4 py-3 font-normal">Fossil</th>
                  <th className="px-4 py-3 font-normal">Formation</th>
                  <th className="px-4 py-3 font-normal">Location</th>
                  <th className="px-4 py-3 text-right font-normal">Lat / Lon</th>
                </tr>
              </thead>
              <tbody>
                {fossils.map((f) => (
                  <tr
                    key={f.id}
                    onClick={() => setSelectedId(f.id)}
                    className={`cursor-pointer border-t border-paleo-line transition-colors ${
                      f.id === selectedId ? "bg-paleo-panel2" : "hover:bg-paleo-panel"
                    }`}
                  >
                    <td className="px-4 py-2.5 font-crimson italic text-paleo-cream">{f.Fossil}</td>
                    <td className="px-4 py-2.5 text-paleo-dim">{f.Formation}</td>
                    <td className="px-4 py-2.5 text-paleo-dim">
                      {f.State}, {f.Country}
                    </td>
                    <td className="px-4 py-2.5 text-right font-mono text-xs text-paleo-dim">
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
