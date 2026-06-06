import type { Diet } from "@/types/paleo";

/**
 * Maps a diet to Tailwind classes. Defined as a plain lookup object outside the
 * component so it isn't re-created on every render — a small but real habit:
 * keep static data out of the render path.
 */
const DIET_STYLES: Record<string, string> = {
  Carnivore: "bg-red-100 text-red-800",
  Herbivore: "bg-green-100 text-green-800",
  Omnivore: "bg-amber-100 text-amber-800",
};

export function DietBadge({ diet }: { diet: Diet }) {
  const styles = DIET_STYLES[diet] ?? "bg-fossil-100 text-fossil-700";
  return (
    <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${styles}`}>
      {diet}
    </span>
  );
}
