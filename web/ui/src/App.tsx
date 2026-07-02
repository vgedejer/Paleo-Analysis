import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { LandingPage } from "@/features/landing/LandingPage";
import { AppLayout } from "@/features/components/AppLayout";
import { EXPLORER_ROUTES, DEFAULT_EXPLORER_PATH } from "@/app/explorerRoutes";

/**
 * The app's route map.
 *
 * Every view is a real, deep-linkable URL that survives a refresh:
 *   `/`                      → the marketing landing page
 *   `/dashboard` /`/genera` /`/fossils` → the explorer, inside a shared layout
 *
 * The explorer routes are generated from EXPLORER_ROUTES (the single source of
 * truth), so adding a page means adding one entry there — not touching this
 * file. `AppLayout` is a pathless layout route: it renders the shared shell once
 * and swaps the active page through its <Outlet/>. Both views share the dark
 * archive theme; the body background is painted `paleo-bg` globally in
 * index.css so overscroll never reveals a light seam.
 *
 * Vite's dev server and `vite preview` both do SPA history fallback, so hitting
 * `/genera` directly (or reloading on it) serves index.html and the router takes
 * over — no server config needed.
 */
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingRoute />} />
      <Route element={<AppLayout />}>
        {EXPLORER_ROUTES.map((route) => (
          <Route key={route.path} path={route.path} element={route.element} />
        ))}
      </Route>
      {/* Unknown paths fall back to the landing page. */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

/**
 * Bridges the presentational LandingPage (which just reports "enter" intent via
 * `onEnter`) to the router. Keeping LandingPage router-agnostic leaves it easy
 * to render in isolation for tests/Storybook.
 */
function LandingRoute() {
  const navigate = useNavigate();
  return (
    <LandingPage
      onEnter={(target) => navigate(`/${target ?? DEFAULT_EXPLORER_PATH}`)}
    />
  );
}
