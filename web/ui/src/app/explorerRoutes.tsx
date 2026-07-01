import type { ReactElement } from "react";
import { UserDashboard } from "@/features/components/UserDashboard";
import { GenusList } from "@/features/components/GenusList";
import { FossilList } from "@/features/components/FossilList";

/**
 * ============================================================================
 *  Explorer route table — the single source of truth for the app's pages.
 * ============================================================================
 *
 *  Each entry drives three things at once, so they can never drift apart:
 *    1. the URL          — `/${path}` (deep-linkable, survives a refresh)
 *    2. the header nav    — `label`
 *    3. the page header    — `eyebrow` / `title` / `subtitle`
 *  …plus the `element` React Router renders into the layout's <Outlet/>.
 *
 *  Adding a page is therefore a one-line change here: append an entry and it
 *  shows up in the nav, gets a titled header, and becomes a real URL — no edits
 *  to App.tsx or AppLayout needed. `title` is kept distinct from `label` because
 *  the "Fossils" tab presents itself as the "Repository" (matching the landing
 *  page's section 02), so the nav word and the page heading differ.
 */
export interface ExplorerRoute {
  /** URL segment under the site root, e.g. "genera" → /genera. */
  path: string;
  /** Nav link text. */
  label: string;
  /** Small mono eyebrow above the page title. */
  eyebrow: string;
  /** Cinzel page heading (may differ from the nav `label`). */
  title: string;
  /** Mono subtitle under the heading. */
  subtitle: string;
  /** The view rendered into the layout outlet for this route. */
  element: ReactElement;
}

export const EXPLORER_ROUTES: ExplorerRoute[] = [
  {
    path: "dashboard",
    label: "Dashboard",
    eyebrow: "00 — Overview",
    title: "Dashboard",
    subtitle: "Counts, timelines & diet breakdowns",
    element: <UserDashboard />,
  },
  {
    path: "genera",
    label: "Genera",
    eyebrow: "05 — Taxonomy",
    title: "Genera",
    subtitle: "Dinosaurian genera across the Mesozoic",
    element: <GenusList />,
  },
  {
    path: "fossils",
    label: "Fossils",
    eyebrow: "02 — Specimen Catalogue",
    title: "Repository",
    subtitle: "The full catalogue of excavated specimens",
    element: <FossilList />,
  },
];

/** Where the landing page's "enter" actions land when no tab is specified. */
export const DEFAULT_EXPLORER_PATH = "dashboard";
