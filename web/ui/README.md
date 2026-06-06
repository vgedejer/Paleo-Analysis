# Paleonix UI

Frontend for the Paleo-Analysis platform — a React + TypeScript dashboard for
dinosaur genera and fossil data, talking to the FastAPI backend in `web/app`.

Stack: **React 18 (Vite) · TypeScript (strict) · Tailwind CSS · TanStack Query · Zustand**

---

## 1. Architectural Overview & Directory Structure

### Feature-based, not layer-based

```
src/
├── app/                 # App-wide wiring: providers, query client, global store
│   ├── providers.tsx    #   composition root (DI container analog)
│   ├── queryClient.ts   #   server-state cache config
│   └── store.ts         #   global CLIENT state (Zustand)
├── lib/
│   └── apiClient.ts     # The ONE HTTP choke point (base URL, errors, params)
├── types/
│   └── paleo.ts         # Domain types — mirror of your Pydantic schemas
├── components/ui/       # Generic, presentational components (Spinner, Badge…)
└── features/            # ← the app is organized by FEATURE, not by file type
    ├── genera/
    │   ├── api/         #   endpoint wrappers (mirror genus_service + router)
    │   ├── hooks/       #   React Query hooks (caching, fetching, keys)
    │   └── components/  #   DinosaurDashboard, GenusCard, GenusDetailPanel
    └── fossils/
        ├── api/  hooks/  components/   # FossilList
```

**Why feature-based?** The common beginner layout groups by *technical role* —
all components in `/components`, all hooks in `/hooks`, all api in `/api`. That
scales badly: adding one feature means touching five scattered folders, and
nothing tells you which files belong together. This is the same lesson as the
backend debate between a **layered** architecture (controllers/services/repos)
and a **modular / vertical-slice / DDD** one (a self-contained module per
bounded context). Past a certain size, organizing by *domain capability* wins
because related code changes together and stays together. Each folder under
`features/` is a vertical slice you could lift out, test, or hand to another
dev with minimal cross-cutting.

> A pragmatic note for interviews: small layer-based apps are perfectly fine,
> and feature-based has a real cost (where do truly shared bits live? → `lib/`,
> `components/ui/`, `types/`). The senior signal is *justifying the trade-off*,
> not dogmatically picking one.

### Separation of concerns (mapped to backend concepts)

| Frontend layer            | File(s)                       | Backend analog                     |
| ------------------------- | ----------------------------- | ---------------------------------- |
| Domain types              | `types/paleo.ts`              | Pydantic response schemas          |
| HTTP client               | `lib/apiClient.ts`            | Typed HTTP client / repo base      |
| Per-feature API wrappers  | `features/*/api/*.ts`         | `*_service.py` + router            |
| Server-state cache/hooks  | `features/*/hooks/*.ts`       | Query/caching layer (no DB analog) |
| Global client state       | `app/store.ts`                | (no analog — UI only)              |
| Presentational components | `components/ui`, feature UI   | Templates / serializers' output    |

The hard rule: **data flows in one direction through these layers.** A
component never calls `fetch`; it calls a hook. A hook never builds a URL; it
calls an api wrapper. An api wrapper never parses errors; `apiClient` does.
Change an endpoint → one file changes.

### The one idea worth internalizing: server state ≠ client state

- **Server state** (genera, fossils) is a *cached copy* of data you don't own.
  It's async, shared, and can go stale. → **TanStack Query** (`app/queryClient.ts`).
- **Client state** (search text, active tab, selected id) never leaves the
  browser. → `useState` for local, **Zustand** (`app/store.ts`) for shared.

Conflating them — dumping fetched data into a global store and hand-rolling
caching/loading/refetch — is the most common React architecture mistake. The
whole codebase is built around keeping them separate.

---

## Getting started

```bash
cd web/ui
cp .env.example .env        # optional; defaults work with the dev proxy
npm install
npm run dev                 # http://localhost:5173
```

Run the backend separately so the dev proxy has something to forward to:

```bash
cd web/app && uvicorn main:app --reload --port 8000
```

The Vite dev server proxies `/api/*` → `http://127.0.0.1:8000` (see
`vite.config.ts`), so the browser only ever sees one origin and there's no CORS
setup needed for local dev.

Other scripts: `npm run build` (type-check + production bundle), `npm run
typecheck`, `npm run preview`.

---

## 2. Where the core boilerplate lives

- **DinosaurDashboard** (`features/genera/components/DinosaurDashboard.tsx`) —
  the flagship container. Fetches via React Query, reads shared filter state
  from Zustand, derives a filtered list with `useMemo`, and renders memoized
  `GenusCard`s plus a dependent-query detail panel. Heavily commented with the
  re-render / hooks mental model.
- **FossilList** (`features/fossils/components/FossilList.tsx`) — the second
  view, showing **server-side** filtering (the filter becomes a query param and
  flows into the React Query key) vs. the dashboard's **client-side** filtering.

---

## 3. Educational comments

Every non-trivial file is commented for a backend engineer, calling out the
paradigm shifts that don't exist in a request/response backend: component
re-render cycles, hook dependency arrays, `useMemo`/`useCallback`/`React.memo`,
controlled inputs, list keys, query keys as cache keys, and dependent queries.
Start with `app/queryClient.ts` → `useGenera.ts` → `DinosaurDashboard.tsx`.

---

## 4. Resume & interview material

### Resume bullets (adapt freely)

- Architected a **feature-based React + TypeScript** frontend (Vite, Tailwind)
  for a paleobiology data platform, enforcing strict separation between a typed
  HTTP layer, server-state caching, and presentational components.
- Modeled **server state with TanStack Query** (query-key-driven caching,
  request deduplication, background refetch, dependent queries) and **client
  state with Zustand**, eliminating hand-rolled loading/error/caching logic.
- Authored an end-to-end **type-safe API contract** in TypeScript mirroring the
  FastAPI/Pydantic schemas, with a single normalized HTTP client (typed errors,
  request cancellation via `AbortSignal`).

### Trade-offs / pitfalls to be ready to discuss

1. **Server-state-in-a-global-store** — the canonical React anti-pattern. Be
   ready to explain *why* server state belongs in a cache like React Query
   (it's async, shared, and goes stale) rather than Redux/Zustand, and what you
   lose by conflating them (manual caching, refetch, dedupe, race conditions).

2. **Client-side vs. server-side filtering** — the dashboard filters in-memory
   (one fetch, instant interaction, but doesn't scale past what's reasonable to
   ship to the browser); FossilList filters server-side (scales, but a round
   trip per change). Knowing the cutover point — and pagination/virtualization
   as the next step — is a real senior decision.

3. **Casing mismatch at the boundary** — the API returns PascalCase
   (`Genus`, `MaxMYA`); JS convention is camelCase. We deliberately kept types
   1:1 with the wire format for zero drift, but the alternative is an
   anti-corruption / mapping layer (`mappers/`) that translates DTO → domain
   model. Trade-off: fidelity & less code now vs. insulation from backend
   changes later.

4. **Memoization is not free** — `React.memo`/`useMemo`/`useCallback` only pay
   off on real hot paths and only when prop references stay stable. Sprinkling
   them everywhere adds complexity and can *hurt*. The honest answer in an
   interview is "measure first."

### Natural next steps (good to mention as a roadmap)

- **React Router** for URL-addressable views (the tabs become routes).
- **Runtime validation (Zod)** to close the gap that TS types are erased at
  runtime — validate API responses so a backend contract change fails loudly.
- **Mutations** (`useMutation` + optimistic updates) once the API gains
  write endpoints.
- **Testing**: Vitest + React Testing Library, with MSW to mock the API.
