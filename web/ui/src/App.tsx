import { useEffect, useState } from "react";
import { GenusList } from "@/features/components/GenusList";
import { FossilList } from "@/features/components/FossilList";
import { UserDashboard } from "@/features/components/UserDashboard";
import { LandingPage, type AppTarget } from "@/features/landing/LandingPage";

type Tab = "genera" | "fossils" | "dashboard";
type View = "landing" | "app";

/**
 * App shell + a tiny local view/tab switcher.
 *
 * Two top-level views: the marketing `landing` page (shown first) and the
 * data-driven `app` explorer. The landing page's nav and CTA call `onEnter` to
 * cross into the explorer; clicking the "Paleonix" brand in the app header
 * returns to the landing page.
 *
 * Within the explorer we use `useState` for the active tab rather than pulling
 * in a router, to keep the boilerplate focused on the data/state story. In a
 * real app this is the natural seam to introduce React Router: landing becomes
 * `/`, each tab a route (/genera, /fossils), giving URL-addressable views, deep
 * links, and back-button support for free. That's called out in the README.
 */
export default function App() {
  const [view, setView] = useState<View>("landing");
  const [tab, setTab] = useState<Tab>("dashboard");

  // The landing page owns the whole viewport with a dark ground; paint the
  // document background to match so overscroll doesn't reveal the light app
  // theme. Restored whenever we're in the explorer.
  useEffect(() => {
    document.body.classList.toggle("bg-paleo-bg", view === "landing");
    return () => document.body.classList.remove("bg-paleo-bg");
  }, [view]);

  if (view === "landing") {
    const enter = (target?: AppTarget) => {
      if (target) setTab(target);
      setView("app");
    };
    return <LandingPage onEnter={enter} />;
  }

  const tabs: { id: Tab; label: string }[] = [
    { id: "dashboard", label: "Dashboard" },
    { id: "genera", label: "Genera" },
    { id: "fossils", label: "Fossils" },
  ];

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <header className="mb-8">
        <button
          type="button"
          onClick={() => setView("landing")}
          className="text-left text-2xl font-bold text-fossil-900 transition-opacity hover:opacity-70"
          title="Back to landing page"
        >
          Paleonix
        </button>
        <p className="text-sm text-fossil-700/70">
          Dinosaur genera &amp; fossil explorer
        </p>
        <nav className="mt-4 flex gap-2">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
                tab === t.id
                  ? "bg-fossil-900 text-white"
                  : "bg-white text-fossil-700 hover:bg-fossil-100"
              }`}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </header>

      <main>
        {tab === "dashboard" ? (
          <UserDashboard />
        ) : tab === "genera" ? (
          <GenusList />
        ) : (
          <FossilList />
        )}
      </main>
    </div>
  );
}
