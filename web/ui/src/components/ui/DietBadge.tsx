import type { Diet } from "@/types/paleo";
import { dietLabel, dietSwatchClass } from "@/lib/diet";

/**
 * Shows a genus's diet: a small square swatch (colored by the primary diet
 * category) beside the ACTUAL diet text from the DB. Combined diets render their
 * full label ("Carnivore, Omnivore"); an unspecified diet shows as "Unknown".
 *
 * Echoes the diet color-coding on the landing page's specimen cards. All diet
 * logic — categories, labels, colors — lives in `@/lib/diet` so the filter and
 * every badge stay in lockstep.
 */
export function DietBadge({ diet }: { diet: Diet | null | undefined }) {
  return (
    <span className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-widest text-paleo-dim">
      <span className={`inline-block h-1.5 w-1.5 shrink-0 ${dietSwatchClass(diet)}`} />
      {dietLabel(diet)}
    </span>
  );
}
