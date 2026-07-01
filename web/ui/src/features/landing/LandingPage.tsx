import { SpecimenCard } from "@/features/landing/SpecimenCard";
import {
  SPECIMENS,
  STATS,
  ERA_DETAILS,
  ERA_COLOR,
} from "@/features/landing/data";

/** Which explorer view the landing page can hand off to. */
export type AppTarget = "genera" | "fossils";

interface LandingPageProps {
  /** Enter the data-driven explorer, optionally on a specific tab. */
  onEnter: (target?: AppTarget) => void;
}

/** Smooth-scroll to an in-page section by id. */
function scrollToSection(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
}

/**
 * The Paleonix landing page — a faithful adaptation of the Figma mockup
 * ("Paleobiology Landing Page"), rebranded to Paleonix. Dark natural-history
 * archive theme: deep shale ground, fossil-cream text, amber accents, Cinzel
 * inscription headings, and Space Mono for taxonomic data.
 *
 * Five sections: hero → specimen repository → stats → three eras → CTA/footer.
 * The nav and the closing CTA are the seams that hand visitors off to the live
 * explorer via `onEnter`.
 */
export function LandingPage({ onEnter }: LandingPageProps) {
  return (
    <div className="relative min-h-screen bg-paleo-bg font-crimson text-paleo-cream">
      <GrainOverlay />
      <TopNav onEnter={onEnter} />
      <Hero />
      <Repository onEnter={onEnter} />
      <Stats />
      <Eras />
      <CtaFooter />
    </div>
  );
}

/** Fixed fractal-noise grain over the whole viewport (mockup: ~4% overlay). */
function GrainOverlay() {
  return (
    <div
      aria-hidden
      className="pointer-events-none fixed inset-0 z-50 opacity-[0.04] mix-blend-overlay"
      style={{
        backgroundImage:
          "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")",
      }}
    />
  );
}

const NAV_LINKS = [
  { label: "Repository", section: "repository" },
  { label: "Eras", section: "eras" },
  { label: "About", section: "about" },
];

function TopNav({ onEnter }: { onEnter: (target?: AppTarget) => void }) {
  return (
    <header className="sticky top-0 z-40 border-b border-paleo-line bg-paleo-bg/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <button
          type="button"
          onClick={() => scrollToSection("top")}
          className="flex items-center gap-2 font-mono text-sm uppercase tracking-[0.35em] text-paleo-cream"
        >
          <span className="text-paleo-accent">◆</span> Paleonix
        </button>
        <nav className="hidden items-center gap-8 font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim md:flex">
          {NAV_LINKS.map((link) => (
            <button
              key={link.section}
              type="button"
              onClick={() => scrollToSection(link.section)}
              className="transition-colors hover:text-paleo-cream"
            >
              {link.label}
            </button>
          ))}
        </nav>
        <span className="font-mono text-xs tracking-[0.25em] text-paleo-dim">
          252–66 MYA
        </span>
      </div>
    </header>
  );
}

function SectionEyebrow({ children }: { children: string }) {
  return (
    <p className="font-mono text-xs uppercase tracking-[0.3em] text-paleo-dim">
      {children}
    </p>
  );
}

const HERO_ERAS = [
  { era: "Triassic", range: "252–201 MYA" },
  { era: "Jurassic", range: "201–145 MYA" },
  { era: "Cretaceous", range: "145–66 MYA" },
] as const;

function Hero() {
  return (
    <section
      id="top"
      className="relative overflow-hidden border-b border-paleo-line"
    >
      {/* Layered dark ground standing in for the full-bleed fossil photo. */}
      <div
        aria-hidden
        className="absolute inset-0 bg-gradient-to-b from-black via-paleo-bg to-paleo-bg"
      />
      <div
        aria-hidden
        className="absolute inset-0 bg-[radial-gradient(circle_at_70%_30%,rgba(193,127,58,0.12),transparent_55%)]"
      />
      <div className="relative mx-auto flex min-h-[88vh] max-w-6xl flex-col justify-center px-6 py-24">
        <SectionEyebrow>01 — Mesozoic Repository</SectionEyebrow>
        <h1 className="mt-6 font-cinzel text-6xl font-black uppercase leading-[0.95] tracking-tight sm:text-7xl md:text-8xl">
          <span className="block text-paleo-cream">The</span>
          <span className="block text-paleo-accent">Fossil</span>
          <span className="block text-paleo-cream">Record</span>
        </h1>
        <p className="mt-8 max-w-2xl font-crimson text-xl italic leading-relaxed text-paleo-dim md:text-2xl">
          A systematic record of dinosaurian life across the Triassic, Jurassic,
          and Cretaceous — 186 million years of evolutionary history, preserved
          in stone.
        </p>
        <button
          type="button"
          onClick={() => scrollToSection("repository")}
          className="mt-12 w-fit font-mono text-xs uppercase tracking-[0.3em] text-paleo-dim transition-colors hover:text-paleo-accent"
        >
          ▼ Scroll to explore
        </button>
      </div>

      {/* Era timeline bar pinned to the bottom of the hero. */}
      <div className="relative mx-auto grid max-w-6xl grid-cols-1 border-t border-paleo-line sm:grid-cols-3">
        {HERO_ERAS.map(({ era, range }) => (
          <div
            key={era}
            className="border-t-2 border-current px-6 py-5 sm:border-l sm:border-l-paleo-line sm:first:border-l-0"
          >
            <span className={ERA_COLOR[era]}>
              <span className="font-mono text-sm uppercase tracking-[0.25em]">
                {era}
              </span>
            </span>
            <p className="mt-1 font-mono text-xs tracking-widest text-paleo-dim">
              {range}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

function Repository({ onEnter }: { onEnter: (target?: AppTarget) => void }) {
  return (
    <section id="repository" className="border-b border-paleo-line">
      <div className="mx-auto max-w-6xl px-6 py-24">
        <SectionEyebrow>02 — Specimen Catalogue</SectionEyebrow>
        <div className="mt-4">
          <h2 className="font-cinzel text-5xl uppercase tracking-tight text-paleo-cream md:text-6xl">
            Repository
          </h2>
          <p className="mt-2 max-w-xl font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim">
            Nine of the most iconic dinosaurs — a sample from the archive
          </p>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-px bg-paleo-line sm:grid-cols-2 lg:grid-cols-3">
          {SPECIMENS.map((specimen) => (
            <SpecimenCard
              key={specimen.name}
              specimen={specimen}
              onOpen={() => onEnter("fossils")}
            />
          ))}
        </div>

        {/* Compact hand-off into the full data-driven repository. */}
        <div className="mt-12 flex justify-center">
          <button
            type="button"
            onClick={() => onEnter("fossils")}
            className="border border-paleo-accent px-8 py-4 font-mono text-xs uppercase tracking-[0.3em] text-paleo-accent transition-colors hover:bg-paleo-accent hover:text-paleo-bg"
          >
            Browse the full repository →
          </button>
        </div>
      </div>
    </section>
  );
}

function Stats() {
  return (
    <section className="border-b border-paleo-line">
      <div className="mx-auto max-w-6xl px-6 py-24">
        <SectionEyebrow>03 — By the Numbers</SectionEyebrow>
        <div className="mt-12 grid grid-cols-2 gap-y-12 md:grid-cols-4">
          {STATS.map((stat) => (
            <div key={stat.label}>
              <p className="font-cinzel text-5xl text-paleo-accent md:text-6xl">
                {stat.value}
              </p>
              <p className="mt-2 font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim">
                {stat.label}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Eras() {
  return (
    <section id="eras" className="border-b border-paleo-line">
      <div className="mx-auto max-w-6xl px-6 py-24">
        <SectionEyebrow>04 — Geological Periods</SectionEyebrow>
        <h2 className="mt-4 font-cinzel text-5xl uppercase tracking-tight text-paleo-cream md:text-6xl">
          Three Eras
        </h2>
        <div className="mt-14 grid grid-cols-1 gap-px bg-paleo-line md:grid-cols-3">
          {ERA_DETAILS.map((detail) => (
            <div key={detail.era} className="bg-paleo-bg p-8">
              <div className={`h-0.5 w-12 ${ERA_COLOR[detail.era]} bg-current`} />
              <h3
                className={`mt-6 font-cinzel text-3xl uppercase tracking-wide ${ERA_COLOR[detail.era]}`}
              >
                {detail.era}
              </h3>
              <p className="mt-1 font-mono text-xs tracking-widest text-paleo-dim">
                {detail.range}
              </p>
              <p className="mt-6 font-crimson text-base italic leading-relaxed text-paleo-dim">
                {detail.blurb}
              </p>
              <dl className="mt-8 space-y-2 font-mono text-xs">
                <div className="flex gap-2 text-paleo-dim">
                  <dt className="whitespace-nowrap text-paleo-accent">
                  ▸ Climate —
                </dt>
                  <dd>{detail.climate}</dd>
                </div>
                <div className="flex gap-2 text-paleo-dim">
                  <dt className="whitespace-nowrap text-paleo-accent">
                  ▸ Diversity —
                </dt>
                  <dd>{detail.diversity}</dd>
                </div>
              </dl>
              <p className="mt-8 font-mono text-[10px] uppercase tracking-[0.25em] text-paleo-dim">
                Notable Genera
              </p>
              <ul className="mt-3 space-y-1 font-crimson italic text-paleo-cream">
                {detail.genera.map((genus) => (
                  <li key={genus}>{genus}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CtaFooter() {
  return (
      <footer className="mx-auto max-w-6xl px-6 py-10">
        <div className="flex flex-col items-center gap-4 text-center font-mono text-xs uppercase tracking-[0.25em] text-paleo-dim md:flex-row md:justify-between md:text-left">
          <span>
            <span className="text-paleo-accent">◆</span> Paleonix — Mesozoic
            Dinosauria Archive
          </span>
          <span className="font-crimson normal-case italic tracking-normal">
            “The stone remembers what the ages forgot.”
          </span>
          <span>©2026</span>
        </div>
      </footer>
  );
}
