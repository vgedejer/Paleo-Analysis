import type { Diet } from "@/types/paleo";

/**
 * ============================================================================
 *  DIET LOGIC  —  one source of truth for the diet filter + badges.
 * ============================================================================
 *
 *  The `Diet` column is free text. Across the whole `dino_genera` table it takes
 *  exactly these shapes (verified against the DB):
 *
 *    Herbivore · Carnivore · Omnivore · Piscivore        (single diets)
 *    Carnivore, omnivore · Herbivore, omnivore           (combined)
 *    Piscivore, insectivore · Carnivore, insectivore     (combined)
 *    "NOT SPECIFIED"                                       (73 rows, unknown)
 *
 *  There are two SEPARATE concerns, and they use two different relationships:
 *
 *  1. DISPLAY — the single diet we *infer* and show. A combined diet is
 *     collapsed by dropping any category that a broader one already implies:
 *       "Carnivore, omnivore"  → Omnivore   (an omnivore already eats meat)
 *       "Herbivore, omnivore"  → Omnivore   (…and plants)
 *       "Carnivore, insectivore" → Carnivore (insectivory is a kind of carnivory)
 *       "Piscivore, insectivore" → Piscivore, Insectivore
 *                                  (neither implies the other — both kept)
 *
 *  2. FILTERING — a genus shows under every filter its diet *includes*. Because
 *     an omnivore eats both meat and plants, it appears under Carnivore AND
 *     Herbivore (while its label still reads "Omnivore"). A piscivore/insectivore
 *     eats animals, so it also appears under Carnivore. The reverse never holds:
 *     a plain Carnivore is not an Omnivore, Piscivore, or Insectivore.
 *
 *  Only the DB's known category tokens participate; an unrecognised value (e.g.
 *  "NOT SPECIFIED") is "Misc" and displays its actual text.
 */

/** The recognised single-diet categories, in the order they appear as filters. */
export const DIET_CATEGORIES = [
  "Carnivore",
  "Herbivore",
  "Omnivore",
  "Piscivore",
  "Insectivore",
] as const;

export type KnownDiet = (typeof DIET_CATEGORIES)[number];
/** A bucket a genus can belong to: a known diet, or the catch-all "Misc". */
export type DietCategory = KnownDiet | "Misc";
/** A selectable filter value: any category, or "All" (no filter). */
export type DietFilter = "All" | DietCategory;

/** The filter buttons rendered in the Genera toolbar, in order. */
export const DIET_FILTER_OPTIONS: DietFilter[] = ["All", ...DIET_CATEGORIES, "Misc"];

/**
 * DISPLAY relation: each diet → the narrower diets it makes redundant. When a
 * combined value lists both a diet and one it subsumes, the narrower one is
 * dropped so a single, most-informative label remains.
 */
const SUBSUMES: Record<KnownDiet, readonly KnownDiet[]> = {
  Omnivore: ["Carnivore", "Herbivore", "Piscivore", "Insectivore"],
  Carnivore: [],
  Herbivore: [],
  Piscivore: [],
  Insectivore: [],
};

/**
 * FILTER relation: each diet → the filters a genus with that diet belongs under.
 * An omnivore eats meat and plants (Carnivore + Herbivore); a piscivore /
 * insectivore eats animals (Carnivore). A diet always matches its own filter.
 */
const MATCHES_FILTERS: Record<KnownDiet, readonly KnownDiet[]> = {
  Carnivore: ["Carnivore"],
  Herbivore: ["Herbivore"],
  Omnivore: ["Omnivore", "Carnivore", "Herbivore"],
  Piscivore: ["Piscivore"],
  Insectivore: ["Insectivore"],
};

const KNOWN_BY_TOKEN = new Map<string, KnownDiet>(
  DIET_CATEGORIES.map((d) => [d.toLowerCase(), d]),
);

/** The recognised category tokens present in a raw diet value, de-duplicated. */
function knownTokens(diet: Diet | null | undefined): KnownDiet[] {
  const found = (diet ?? "")
    .split(",")
    .map((t) => KNOWN_BY_TOKEN.get(t.trim().toLowerCase()))
    .filter((d): d is KnownDiet => Boolean(d));
  return [...new Set(found)];
}

/**
 * The inferred, collapsed diet(s) for display — the "maximal" categories, with
 * any category a co-listed broader one already implies removed. Returns [] when
 * no recognised diet is present (→ Misc / unknown).
 */
export function canonicalDiets(diet: Diet | null | undefined): KnownDiet[] {
  const present = knownTokens(diet);
  return present.filter(
    (t) => !present.some((other) => other !== t && SUBSUMES[other].includes(t)),
  );
}

/**
 * The human-readable diet shown on cards — the inferred single diet
 * ("Carnivore, omnivore" → "Omnivore"). A genuinely dual diet keeps both parts
 * ("Piscivore, Insectivore"). An unrecognised value shows its actual DB text;
 * a truly empty one shows "Unknown".
 */
export function dietLabel(diet: Diet | null | undefined): string {
  const canon = canonicalDiets(diet);
  if (canon.length > 0) return canon.join(", ");
  const raw = (diet ?? "").trim();
  return raw === "" ? "Unknown" : raw;
}

/** Whether a genus's diet matches the selected filter. "All" matches everything. */
export function matchesDietFilter(
  diet: Diet | null | undefined,
  filter: DietFilter,
): boolean {
  if (filter === "All") return true;
  const canon = canonicalDiets(diet);
  if (canon.length === 0) return filter === "Misc";
  return canon.some((d) => MATCHES_FILTERS[d].includes(filter as KnownDiet));
}

/**
 * Tailwind swatch color for a diet, keyed off its PRIMARY (first inferred)
 * category. Full literal class strings so Tailwind's content scan keeps them.
 */
const SWATCH: Record<DietCategory, string> = {
  Carnivore: "bg-paleo-carnivore",
  Herbivore: "bg-paleo-herbivore",
  Omnivore: "bg-paleo-jurassic",
  Piscivore: "bg-paleo-piscivore",
  Insectivore: "bg-paleo-cretaceous",
  Misc: "bg-paleo-dim",
};

export function dietSwatchClass(diet: Diet | null | undefined): string {
  const primary = canonicalDiets(diet)[0] ?? "Misc";
  return SWATCH[primary];
}
