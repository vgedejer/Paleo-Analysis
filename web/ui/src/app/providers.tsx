import { type ReactNode } from "react";
import { BrowserRouter } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { queryClient } from "./queryClient";

/**
 * App-wide context providers, composed in one place.
 *
 * Backend-dev analogy: this is your dependency-injection container / app
 * composition root. `QueryClientProvider` makes the single shared query cache
 * available to every component below it via React Context — the same idea as a
 * request-scoped service registered once and injected wherever it's needed.
 *
 * Keeping providers here (rather than inline in main.tsx) means adding a router,
 * a theme provider, or an auth provider later is a one-line change in a file
 * whose only job is wiring.
 */
export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {/* BrowserRouter provides the History API context that makes URLs like
          /genera real, deep-linkable, and refresh-safe. */}
      <BrowserRouter>{children}</BrowserRouter>
      {/* Devtools render only in dev builds; Vite strips them from production.
          Open the floating panel to watch the cache, query states, and
          refetches in real time — invaluable for understanding React Query. */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
