import { useQuery } from "@tanstack/react-query";
import { ApiError } from "@/lib/apiClient";
import { fetchFossils, fetchFossilById, type FossilFilter } from "../api/fossilsApi";

export const fossilKeys = {
  all: ["fossils"] as const,
  list: (filter: FossilFilter) => [...fossilKeys.all, "list", filter ?? "none"] as const,
  detail: (id: number) => [...fossilKeys.all, "detail", id] as const,
  // Kept distinct from `list` so the genus-detail panel's 404-tolerant fetch
  // never collides with the Fossils page's own genus filter in the cache.
  forGenus: (genus: string) => [...fossilKeys.all, "byGenus", genus] as const,
};

/**
 * Fetch fossils, optionally filtered by genus or species.
 *
 * Note how the `filter` flows INTO the query key. Because the key changes when
 * the filter changes, React Query automatically treats each filter as its own
 * cached entry: switch from genus=Tyrannosaurus to genus=Triceratops and it
 * fetches + caches the new set, while the previous one stays cached for instant
 * back-navigation. You wrote zero caching code to get that — that's the payoff
 * of keying queries by their inputs.
 */
export function useFossils(filter: FossilFilter) {
  return useQuery({
    queryKey: fossilKeys.list(filter),
    queryFn: ({ signal }) => fetchFossils(filter, signal),
  });
}

/**
 * Fetch the fossil specimens for a single genus (by name), for the genus detail
 * panel. Stays idle until a genus is provided. The backend returns 404 when a
 * genus has no fossils; we normalize that to an empty list so the panel shows a
 * clean "no specimens" state instead of an error.
 */
export function useGenusFossils(genus: string | null) {
  return useQuery({
    queryKey: fossilKeys.forGenus(genus ?? ""),
    queryFn: async ({ signal }) => {
      try {
        return await fetchFossils({ by: "genus", value: genus as string }, signal);
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) return [];
        throw err;
      }
    },
    enabled: Boolean(genus),
  });
}

/**
 * Fetch one fossil's full detail by id. Mirrors `useGenusDetail`: the query
 * stays idle until a row is selected (`enabled`), then fetches + caches it.
 */
export function useFossilDetail(id: number | null) {
  return useQuery({
    queryKey: fossilKeys.detail(id ?? -1),
    queryFn: ({ signal }) => fetchFossilById(id as number, signal),
    enabled: id !== null,
  });
}
