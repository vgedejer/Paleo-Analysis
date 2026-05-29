import { QueryClient } from "@tanstack/react-query";

/**
 * ============================================================================
 *  THE QUERY CLIENT  —  your in-browser server-state cache.
 * ============================================================================
 *
 *  This is the most important concept shift for a backend dev, so it's worth
 *  internalizing: there are TWO kinds of state in a frontend app.
 *
 *    1. SERVER STATE  — data that lives in your database and is fetched over
 *       the network. It's a *cached copy* you don't truly own; it can go stale.
 *       (genera, fossils, species). → managed by React Query.
 *
 *    2. CLIENT STATE  — UI-only state that never leaves the browser
 *       (which tab is open, a search box's text, a modal's open/closed flag).
 *       → managed by useState / Zustand.
 *
 *  Conflating the two is the #1 architectural mistake in React apps. People dump
 *  server data into a global store (Redux/Zustand) and then hand-write all the
 *  caching, loading flags, deduping, and refetching that React Query gives for
 *  free. React Query exists precisely because server state has rules of its own:
 *  it's asynchronous, shared, and can be changed by other clients at any time.
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // How long fetched data is considered "fresh". While fresh, React Query
      // serves the cache instantly and does NOT refetch. After this it's
      // "stale" and eligible for a background refetch on the next trigger.
      // Paleo data barely changes, so a generous 5 minutes is reasonable.
      staleTime: 5 * 60 * 1000,

      // Retry failed requests twice before surfacing an error — but never retry
      // a 4xx, since a 404 won't magically become a 200. This is where our
      // typed ApiError pays off.
      retry: (failureCount, error) => {
        const status = (error as { status?: number })?.status;
        if (status && status >= 400 && status < 500) return false;
        return failureCount < 2;
      },

      // Refetch when the user re-focuses the tab — keeps data fresh after they
      // come back from another window. Turn off if it feels too chatty.
      refetchOnWindowFocus: true,
    },
  },
});
