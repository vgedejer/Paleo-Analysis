import { create } from "zustand";
import type { DietFilter } from "@/lib/diet";

/**
 * ============================================================================
 *  GLOBAL CLIENT STATE  —  Zustand store for cross-component UI state.
 * ============================================================================
 *
 *  Read queryClient.ts first for the server-state vs. client-state distinction.
 *  THIS file is the *client-state* half: UI concerns that several unrelated
 *  components need to read/write, but which never get persisted to the backend.
 *
 *  Why Zustand and not Redux?
 *  Redux is powerful but ceremony-heavy (actions, reducers, dispatch, selectors,
 *  middleware). Zustand is "a hook around a single object + setter functions" —
 *  far less boilerplate for small apps. The store below is the entire pattern:
 *  define state + the functions that mutate it, and components subscribe to
 *  exactly the slices they read.
 *
 *  Why not just useState? Because this filter is shared between the dashboard
 *  toolbar and the list/grid that reacts to it. Lifting it to a global store
 *  avoids "prop drilling" the value and its setter through every layer between.
 *
 *  Rule of thumb: reach for a global store only when state is genuinely shared
 *  across distant components. Local component state (useState) should remain
 *  your default — global state you don't need is just hidden coupling.
 */

/**
 * The diet filter value. Its type — the recognised diet categories plus "Misc"
 * and "All" — lives with the rest of the diet logic in `@/lib/diet`; re-exported
 * here so existing importers of the store keep working.
 */
export type { DietFilter };

interface UiState {
  /** Free-text search bound to the dashboard's search input. */
  search: string;
  /** Which diet the user is filtering genera by. */
  dietFilter: DietFilter;

  setSearch: (value: string) => void;
  setDietFilter: (value: DietFilter) => void;
  resetFilters: () => void;
}

export const useUiStore = create<UiState>((set) => ({
  search: "",
  dietFilter: "All",

  // Each setter calls `set` with a partial state object. Zustand shallow-merges
  // it and notifies only the components subscribed to the changed slice — the
  // same render-minimization goal Redux selectors chase, with less code.
  setSearch: (value) => set({ search: value }),
  setDietFilter: (value) => set({ dietFilter: value }),
  resetFilters: () => set({ search: "", dietFilter: "All" }),
}));
