import { Link, NavLink, Outlet, useLocation } from "react-router-dom";
import { EXPLORER_ROUTES } from "@/app/explorerRoutes";

/**
 * The explorer shell shared by every data page (Dashboard, Genera, Fossils).
 *
 * It renders once as a React Router *layout route* — the sticky top bar and the
 * per-page header live here, and the active page is swapped into <Outlet/> as
 * the URL changes. Both the nav and the page header are derived from
 * EXPLORER_ROUTES, so this component never needs editing when a page is added.
 *
 * Mirrors the landing page's TopNav: ◆ accent brand (a real link back to `/`),
 * mono-uppercase nav with an amber active-underline driven by the URL.
 */
export function AppLayout() {
  const { pathname } = useLocation();
  const active = EXPLORER_ROUTES.find((route) => pathname === `/${route.path}`);

  return (
    <div className="min-h-screen bg-paleo-bg font-crimson text-paleo-cream">
      <header className="sticky top-0 z-40 border-b border-paleo-line bg-paleo-bg/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link
            to="/"
            className="flex items-center gap-2 font-mono text-sm uppercase tracking-[0.35em] text-paleo-cream transition-colors hover:text-paleo-accent"
            title="Back to landing page"
          >
            <span className="text-paleo-accent">◆</span> Paleonix
          </Link>
          <nav className="flex items-center gap-6 font-mono text-xs uppercase tracking-[0.25em]">
            {EXPLORER_ROUTES.map((route) => (
              <NavLink
                key={route.path}
                to={`/${route.path}`}
                className={({ isActive }) =>
                  `border-b-2 pb-1 transition-colors ${
                    isActive
                      ? "border-paleo-accent text-paleo-accent"
                      : "border-transparent text-paleo-dim hover:text-paleo-cream"
                  }`
                }
              >
                {route.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <div className="mx-auto max-w-6xl px-6 py-12">
        {active && (
          <div className="mb-10">
            <p className="font-mono text-xs uppercase tracking-[0.3em] text-paleo-dim">
              {active.eyebrow}
            </p>
            <h1 className="mt-4 font-cinzel text-5xl uppercase tracking-tight text-paleo-cream md:text-6xl">
              {active.title}
            </h1>
            <p className="mt-2 max-w-xl font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim">
              {active.subtitle}
            </p>
          </div>
        )}

        <main>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
