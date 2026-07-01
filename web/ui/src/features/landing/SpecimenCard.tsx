import { memo } from "react";
import { type Specimen, ERA_COLOR, DIET_COLOR } from "@/features/landing/data";

interface SpecimenCardProps {
  specimen: Specimen;
  /** Fired when the card is activated — hands the visitor to the explorer. */
  onOpen: () => void;
}

/**
 * A single specimen card in the repository grid.
 *
 * The mockup used a full-bleed fossil photo per card; we render a self-contained
 * era-tinted "plate" instead so the landing page ships with no external image
 * dependencies. Everything below the plate — taxonomic name, the four data
 * fields, region and discovery year — mirrors the mockup one-to-one.
 *
 * `memo` because the parent re-renders on every era-filter change; the visible
 * cards' props are stable so unaffected ones bail out of re-rendering.
 */
export const SpecimenCard = memo(function SpecimenCard({
  specimen,
  onOpen,
}: SpecimenCardProps) {
  const {
    name,
    species,
    era,
    stage,
    period,
    length,
    clade,
    diet,
    region,
    discovered,
  } = specimen;

  return (
    <button
      type="button"
      onClick={onOpen}
      className="group flex flex-col border border-paleo-line bg-paleo-panel text-left transition-colors hover:bg-paleo-panel2 focus:outline-none focus-visible:ring-1 focus-visible:ring-paleo-accent"
    >
      {/* Era-tinted plate — stands in for the fossil photograph. */}
      <div className="relative h-40 overflow-hidden border-b border-paleo-line bg-gradient-to-br from-paleo-panel2 via-paleo-bg to-black">
        <div
          aria-hidden
          className={`pointer-events-none absolute inset-0 opacity-30 bg-gradient-to-tr from-transparent via-transparent ${
            era === "Triassic"
              ? "to-paleo-triassic/40"
              : era === "Jurassic"
                ? "to-paleo-jurassic/40"
                : "to-paleo-cretaceous/40"
          }`}
        />
        {/* Faint fossil-vertebra motif for texture. */}
        <svg
          aria-hidden
          viewBox="0 0 200 100"
          className="absolute inset-0 h-full w-full opacity-[0.08]"
          preserveAspectRatio="xMidYMid slice"
        >
          <path
            d="M-5 100 Q 30 10 45 55 T 120 50 T 210 40"
            fill="none"
            stroke="currentColor"
            strokeWidth="5"
            className="text-paleo-cream"
          />
        </svg>
        <span
          className={`absolute right-0 top-0 border-l border-b border-paleo-line px-2 py-1 font-mono text-[10px] uppercase tracking-widest ${ERA_COLOR[era]}`}
        >
          {era}
        </span>
        <span className="absolute bottom-0 left-0 px-3 py-2 font-mono text-[11px] uppercase tracking-widest text-paleo-dim">
          {stage}
        </span>
      </div>

      {/* Taxonomic identity. */}
      <div className="px-5 pt-4">
        <h3 className="font-cinzel text-xl uppercase tracking-wide text-paleo-cream transition-colors group-hover:text-paleo-accent">
          {name}
        </h3>
        <p className="font-crimson text-sm italic text-paleo-dim">{species}</p>
      </div>

      {/* Four data fields, mirroring the mockup grid. */}
      <dl className="grid grid-cols-2 gap-x-4 gap-y-3 px-5 py-4 font-mono text-xs">
        <Field label="Period" value={period} />
        <Field label="Length" value={length} />
        <Field label="Clade" value={clade} />
        <div>
          <dt className="text-[10px] uppercase tracking-widest text-paleo-dim">
            Diet
          </dt>
          <dd className="mt-1 flex items-center gap-2 text-paleo-cream">
            <span className={`inline-block h-1.5 w-1.5 ${DIET_COLOR[diet]}`} />
            {diet}
          </dd>
        </div>
      </dl>

      {/* Provenance footer. */}
      <div className="mt-auto flex items-center justify-between border-t border-paleo-line px-5 py-3 font-mono text-[11px] uppercase tracking-widest text-paleo-dim">
        <span>{region}</span>
        <span className="transition-colors group-hover:text-paleo-accent">
          Disc. {discovered} →
        </span>
      </div>
    </button>
  );
});

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-[10px] uppercase tracking-widest text-paleo-dim">
        {label}
      </dt>
      <dd className="mt-1 text-paleo-cream">{value}</dd>
    </div>
  );
}
