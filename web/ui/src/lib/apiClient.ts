/**
 * ============================================================================
 *  API CLIENT  —  the single choke point for talking to the backend.
 * ============================================================================
 *
 *  Backend-dev analogy:
 *  Think of this as the frontend's equivalent of a typed HTTP client / repository
 *  base class. Every request in the app flows through `apiGet`. That means
 *  cross-cutting concerns — base URL, JSON parsing, error normalization, and
 *  later auth headers or tracing — live in exactly ONE place. Feature code never
 *  touches `fetch` directly, the same way your routers never open a raw DB
 *  connection.
 *
 *  Why a custom error class instead of letting `fetch` reject?
 *  `fetch` only rejects on network failure — a 404 or 500 still RESOLVES.
 *  That trips up almost every newcomer. We normalize that here so the rest of
 *  the app can rely on a simple rule: "if apiGet didn't throw, you have data."
 */

// import.meta.env is Vite's compile-time env injection (see .env.example).
// We fall back to the relative prefix so the app runs even without a .env file.
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

/**
 * A typed error carrying the HTTP status, so callers (and React Query) can
 * branch on it — e.g. show a "Not found" UI for 404 vs. a retry for 503.
 */
export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
    public readonly url: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Build a URL with query params, dropping any param that is `undefined`/`null`.
 * Keeps call sites clean: pass an object, get a correct query string, with no
 * dangling `?genus=undefined` bugs.
 */
function buildUrl(path: string, params?: Record<string, string | number | boolean | undefined>): string {
  const url = new URL(`${BASE_URL}${path}`, window.location.origin);
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null) {
        url.searchParams.set(key, String(value));
      }
    }
  }
  // Return path + search only; the origin was just needed to satisfy the URL API.
  return url.pathname + url.search;
}

/**
 * The generic GET helper. `<T>` is the expected response shape — the caller
 * states it (`apiGet<Genus[]>(...)`) and TypeScript propagates it outward so
 * the data is typed all the way to the component.
 *
 * `signal` lets React Query abort in-flight requests when a query is no longer
 * needed (component unmounts, query key changes). This is the frontend analog
 * of cancelling an orphaned async DB call — it prevents wasted work and races.
 */
export async function apiGet<T>(
  path: string,
  options: {
    params?: Record<string, string | number | boolean | undefined>;
    signal?: AbortSignal;
  } = {},
): Promise<T> {
  const url = buildUrl(path, options.params);

  const response = await fetch(url, {
    method: "GET",
    headers: { Accept: "application/json" },
    signal: options.signal,
  });

  // Normalize HTTP errors into thrown ApiErrors (see class comment above).
  if (!response.ok) {
    // FastAPI's exception handlers return `{ "detail": "..." }`; try to surface it.
    let detail = response.statusText;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body?.detail) detail = body.detail;
    } catch {
      // Body wasn't JSON — keep the status text. Swallowing here is intentional.
    }
    throw new ApiError(response.status, detail, url);
  }

  return (await response.json()) as T;
}
