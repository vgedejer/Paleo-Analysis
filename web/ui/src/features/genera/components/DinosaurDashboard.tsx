import { useCallback, useMemo, useState } from "react";
import { useGenera, useGenusDetail } from "../hooks/useGenera";
import { useUiStore, type DietFilter } from "@/app/store";
import { GenusCard } from "./GenusCard";
import { GenusDetailPanel } from "./GenusDetailPanel";
import { Spinner } from "@/components/ui/Spinner";
import { ErrorState } from "@/components/ui/ErrorState";

const DIET_OPTIONS: DietFilter[] = ["All", "Herbivore", "Carnivore", "Omnivore"];

/**
 * ============================================================================
 *  DinosaurDashboard — the feature's container/"smart" component.
 * ============================================================================
 *
 *  This component orchestrates: it pulls server data (useGenera), reads shared
 *  UI state (useUiStore), derives the filtered view, and composes presentational
 *  children (GenusCard, GenusDetailPanel). The children stay dumb; the smarts
 *  live here. That container/presentational split keeps the dumb parts trivially
 *  reusable and testable.
 *
 *  ---------------------------------------------------------------------------
 *  THE RE-RENDER MENTAL MODEL  (the big shift from backend request/response)
 *  ---------------------------------------------------------------------------
 *  A backend handler runs once per request, top to bottom, then dies. A React
 *  component function runs AGAIN every time its state or props change. So this
 *  function body re-executes on every keystroke in the search box, on every
 *  fetch state change, on every selection. "Rendering" = calling this function
 *  to produce a description of the UI; React then reconciles that against the
 *  DOM. Internalize this and hooks stop being mysterious: they're how a function
 *  that re-runs constantly can still "remember" things between runs.
 */
export function DinosaurDashboard() {
  // --- SERVER STATE: fetched, cached, and kept fresh by React Query. ---
  // `isPending` = first load, no data yet. `isFetching` = any in-flight request
  // (including background refetches while showing stale data).
  const { data: genera, isPending, isError, error, refetch } = useGenera();

  // --- GLOBAL CLIENT STATE: shared filter values from the Zustand store. ---
  // We subscribe to individual slices so this component only re-renders when
  // these specific values change, not on every unrelated store update.
  const search = useUiStore((s) => s.search);
  const dietFilter = useUiStore((s) => s.dietFilter);
  const setSearch = useUiStore((s) => s.setSearch);
  const setDietFilter = useUiStore((s) => s.setDietFilter);

  // --- LOCAL COMPONENT STATE: which genus is selected for the detail panel. ---
  // It's local because nothing outside this subtree needs it — the right default
  // until proven otherwise. `useState` returns [value, setter]; calling the
  // setter schedules a re-render with the new value.
  const [selectedId, setSelectedId] = useState<number | null>(null);

  // This dependent query stays idle until `selectedId` is set (see the hook's
  // `enabled` flag), then fetches that genus's full detail and caches it.
  const detailQuery = useGenusDetail(selectedId);

  /**
   * DERIVED STATE via `useMemo`.
   *
   * Filtering is pure computation from existing state — it should NOT be stored
   * in its own useState (that would create two sources of truth that can drift).
   * Instead we compute it during render. `useMemo` caches the result and only
   * recomputes when something in the dependency array `[genera, search,
   * dietFilter]` changes — so typing elsewhere or selecting a card won't re-run
   * this filter. For a tiny list this is premature, but it's the correct shape
   * for when the dataset grows, and it demonstrates the dependency-array model.
   */
  const filteredGenera = useMemo(() => {
    if (!genera) return [];
    const needle = search.trim().toLowerCase();
    return genera.filter((g) => {
      const matchesSearch = needle === "" || g.Genus.toLowerCase().includes(needle);
      const matchesDiet = dietFilter === "All" || g.Diet === dietFilter;
      return matchesSearch && matchesDiet;
    });
  }, [genera, search, dietFilter]);

  /**
   * `useCallback` memoizes a FUNCTION's identity across renders.
   *
   * Without it, `onSelect` would be a brand-new function object on every render,
   * which would defeat the `React.memo` on every GenusCard (new prop reference =
   * "props changed" = re-render). With an empty dep array the same function
   * instance is reused, so memoized cards can correctly skip re-rendering.
   * This is the canonical memo + useCallback pairing.
   */
  const handleSelect = useCallback((id: number) => setSelectedId(id), []);

  return (
    <section className="space-y-6">
      {/* ----------------------------- Toolbar ----------------------------- */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <input
          type="search"
          // A "controlled input": React state is the single source of truth for
          // the field's value, and onChange pushes every keystroke back into
          // state. The DOM never holds value independently — React drives it.
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search genera…"
          className="w-full rounded-lg border border-fossil-100 px-3 py-2 text-sm outline-none focus:border-fossil-700/50 sm:max-w-xs"
        />
        <div className="flex gap-1.5">
          {DIET_OPTIONS.map((option) => (
            <button
              key={option}
              onClick={() => setDietFilter(option)}
              className={`rounded-full px-3 py-1 text-xs font-medium transition ${
                dietFilter === option
                  ? "bg-fossil-700 text-white"
                  : "bg-fossil-100 text-fossil-700 hover:bg-fossil-100/70"
              }`}
            >
              {option}
            </button>
          ))}
        </div>
      </div>

      {/* --------------------------- Conditional UI ------------------------ */}
      {/* Render branches off the query state machine. Note we handle loading
          and error explicitly — never assume `data` exists. The compiler enforces
          this too: `genera` is `Genus[] | undefined` until the success branch. */}
      {isPending ? (
        <Spinner label="Excavating genera…" />
      ) : isError ? (
        <ErrorState message={error.message} onRetry={() => refetch()} />
      ) : (
        <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
          {/* Results grid */}
          <div>
            <p className="mb-3 text-xs text-fossil-700/60">
              {filteredGenera.length} of {genera.length} genera
            </p>
            {filteredGenera.length === 0 ? (
              <p className="rounded-lg border border-dashed border-fossil-100 p-8 text-center text-sm text-fossil-700/60">
                No genera match your filters.
              </p>
            ) : (
              <div className="grid gap-3 sm:grid-cols-2">
                {/* Lists need a stable, unique `key` per item. React uses keys to
                    match elements across renders so it can move/update rather than
                    destroy + rebuild them. Use a real id — NEVER the array index
                    for dynamic/reorderable lists (a classic source of subtle bugs). */}
                {filteredGenera.map((genus) => (
                  <GenusCard key={genus.id} genus={genus} onSelect={handleSelect} />
                ))}
              </div>
            )}
          </div>

          {/* Detail side panel — driven by the dependent query. */}
          <GenusDetailPanel
            query={detailQuery}
            isOpen={selectedId !== null}
            onClose={() => setSelectedId(null)}
          />
        </div>
      )}
    </section>
  );
}
