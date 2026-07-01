import type { Diet } from "@/types/paleo";

/**
 * Maps a diet to its swatch color. Defined as a plain lookup object outside the
 * component so it isn't re-created on every render — a small but real habit:
 * keep static data out of the render path.
 *
 * Echoes the diet color-coding on the landing page's specimen cards: a small
 * square swatch beside a mono, uppercase label rather than a filled pill.
 */
const DIET_SWATCH: Record<string, string> = {
  Carnivore: "bg-paleo-carnivore",
  Herbivore: "bg-paleo-herbivore",
  Omnivore: "bg-paleo-jurassic",
};

export function DietBadge({ diet }: { diet: Diet }) {
  const swatch = DIET_SWATCH[diet] ?? "bg-paleo-dim";
  return (
    <span className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-widest text-paleo-dim">
      <span className={`inline-block h-1.5 w-1.5 ${swatch}`} />
      {diet}
    </span>
  );
}
