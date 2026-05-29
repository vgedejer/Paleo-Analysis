import { useQuery } from "@tanstack/react-query";
import { fetchGenera, fetchGenusById } from "../api/generaApi";

/**
 * ============================================================================
 *  GENERA — DATA-FETCHING HOOKS  (the React Query layer)
 * ============================================================================
 *
 *  A "custom hook" is just a function whose name starts with `use` and which
 *  calls other hooks. It's React's unit of reusable, stateful logic. By wrapping
 *  React Query here, every component gets the same cached query with one import
 *  — and if the endpoint changes, there's exactly one place to fix it.
 *
 *  ---------------------------------------------------------------------------
 *  QUERY KEYS — the concept that makes the cache work.
 *  ---------------------------------------------------------------------------
 *  The first argument, `queryKey`, is a serializable array that uniquely
 *  identifies this data in the cache. Think of it as a cache key / primary key:
 *
 *    - Two components using the SAME key share ONE network request and ONE
 *      cached result (automatic request deduplication).
 *    - When any value INSIDE the key changes, React Query treats it as a
 *      different query and refetches — this is how you make data react to
 *      inputs (an id, a filter) declaratively, without manually calling fetch.
 *
 *  We centralize keys in `generaKeys` so they're consistent and so cache
 *  invalidation elsewhere (`queryClient.invalidateQueries`) can target them.
 */
export const generaKeys = {
  all: ["genera"] as const,
  lists: () => [...generaKeys.all, "list"] as const,
  detail: (id: number) => [...generaKeys.all, "detail", id] as const,
};

/**
 * Fetch the full list of genera.
 *
 * What you get back is NOT just data — it's a state machine. `useQuery` returns
 * `{ data, isPending, isError, error, isFetching, ... }`. There is no
 * `setData`; you never imperatively assign the result. Instead the component
 * RE-RENDERS automatically whenever any of these fields change (request starts,
 * succeeds, fails, refetches). That declarative loop — "describe what data you
 * need, render from whatever state it's in" — is the heart of React.
 */
export function useGenera() {
  return useQuery({
    queryKey: generaKeys.lists(),
    // React Query passes an AbortSignal; we forward it so a refetch or unmount
    // cancels the in-flight request instead of leaking it.
    queryFn: ({ signal }) => fetchGenera(signal),
  });
}

/**
 * Fetch one genus's full detail by id.
 *
 * `enabled` is a dependent-query guard: when `id` is null (nothing selected),
 * the query stays idle and never fires. This is the React Query way to express
 * "don't run until the input exists" — instead of an `if` around a fetch call.
 */
export function useGenusDetail(id: number | null) {
  return useQuery({
    queryKey: generaKeys.detail(id ?? -1),
    queryFn: ({ signal }) => fetchGenusById(id as number, signal),
    enabled: id !== null,
  });
}
