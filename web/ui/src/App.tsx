import { useState } from "react";
import { DinosaurDashboard } from "@/features/genera/components/DinosaurDashboard";
import { FossilList } from "@/features/fossils/components/FossilList";

type Tab = "genera" | "fossils";

/**
 * App shell + a tiny local tab switcher.
 *
 * We use `useState` for the active tab rather than pulling in a router, to keep
 * the boilerplate focused on the data/state story. In a real app this is the
 * natural seam to introduce React Router: each tab becomes a route (/genera,
 * /fossils), giving you URL-addressable views, deep links, and back-button
 * support for free. That's called out as a next step in the README.
 */
export default function App() {
  const [tab, setTab] = useState<Tab>("genera");

  const tabs: { id: Tab; label: string }[] = [
    { id: "genera", label: "🦕 Genera" },
    { id: "fossils", label: "🦴 Fossils" },
  ];

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-fossil-900">Paleonix</h1>
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

      <main>{tab === "genera" ? <DinosaurDashboard /> : <FossilList />}</main>
    </div>
  );
}
