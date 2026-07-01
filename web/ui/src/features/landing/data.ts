/**
 * Curated content for the landing page, transcribed from the Figma mockup
 * ("Paleobiology Landing Page"). This is intentionally static, hand-picked
 * marketing content — the landing page showcases a fixed set of nine flagship
 * specimens rather than querying the live API. The "Browse full repository" CTA
 * is what hands the visitor off to the data-driven explorer.
 */

export type Era = "Triassic" | "Jurassic" | "Cretaceous";
export type Diet = "Carnivore" | "Herbivore" | "Piscivore";

export interface Specimen {
  name: string;
  species: string;
  era: Era;
  /** Fine-grained stage label shown on the plate, e.g. "Late Cretaceous". */
  stage: string;
  period: string;
  length: string;
  clade: string;
  diet: Diet;
  region: string;
  discovered: string;
}

/** The nine flagship specimens, in the mockup's grid order. */
export const SPECIMENS: Specimen[] = [
  {
    name: "Tyrannosaurus",
    species: "rex",
    era: "Cretaceous",
    stage: "Late Cretaceous",
    period: "68–66 MYA",
    length: "12–13 m",
    clade: "Theropoda",
    diet: "Carnivore",
    region: "Western North America",
    discovered: "1902",
  },
  {
    name: "Brachiosaurus",
    species: "altithorax",
    era: "Jurassic",
    stage: "Late Jurassic",
    period: "154–153 MYA",
    length: "20–26 m",
    clade: "Sauropoda",
    diet: "Herbivore",
    region: "North America",
    discovered: "1900",
  },
  {
    name: "Triceratops",
    species: "horridus",
    era: "Cretaceous",
    stage: "Late Cretaceous",
    period: "68–66 MYA",
    length: "7.9–9 m",
    clade: "Ceratopsia",
    diet: "Herbivore",
    region: "Western North America",
    discovered: "1887",
  },
  {
    name: "Stegosaurus",
    species: "stenops",
    era: "Jurassic",
    stage: "Late Jurassic",
    period: "155–150 MYA",
    length: "6–9 m",
    clade: "Thyreophora",
    diet: "Herbivore",
    region: "North America",
    discovered: "1877",
  },
  {
    name: "Velociraptor",
    species: "mongoliensis",
    era: "Cretaceous",
    stage: "Late Cretaceous",
    period: "75–71 MYA",
    length: "1.5–2 m",
    clade: "Dromaeosauridae",
    diet: "Carnivore",
    region: "Central Asia",
    discovered: "1923",
  },
  {
    name: "Spinosaurus",
    species: "aegyptiacus",
    era: "Cretaceous",
    stage: "Mid Cretaceous",
    period: "99–93 MYA",
    length: "14–18 m",
    clade: "Spinosauridae",
    diet: "Piscivore",
    region: "North Africa",
    discovered: "1912",
  },
  {
    name: "Coelophysis",
    species: "bauri",
    era: "Triassic",
    stage: "Late Triassic",
    period: "210–200 MYA",
    length: "2–3 m",
    clade: "Theropoda",
    diet: "Carnivore",
    region: "North America",
    discovered: "1881",
  },
  {
    name: "Allosaurus",
    species: "fragilis",
    era: "Jurassic",
    stage: "Late Jurassic",
    period: "155–145 MYA",
    length: "8.5–9.7 m",
    clade: "Theropoda",
    diet: "Carnivore",
    region: "North America, Europe",
    discovered: "1869",
  },
  {
    name: "Ankylosaurus",
    species: "magniventris",
    era: "Cretaceous",
    stage: "Late Cretaceous",
    period: "68–66 MYA",
    length: "6–8 m",
    clade: "Ankylosauria",
    diet: "Herbivore",
    region: "Western North America",
    discovered: "1906",
  },
];

/** The "By the Numbers" stat block. */
export const STATS = [
  { value: "1,468", label: "Classified Species" },
  { value: "186M", label: "Years of Evolution" },
  { value: "7", label: "Continents Surveyed" },
  { value: "3", label: "Geological Periods" },
];

export interface EraDetail {
  era: Era;
  range: string;
  blurb: string;
  climate: string;
  diversity: string;
  genera: string[];
}

/** The three deep-dive era columns. */
export const ERA_DETAILS: EraDetail[] = [
  {
    era: "Triassic",
    range: "252–201 MYA",
    blurb:
      "The dawn of the dinosaurs. Following the Permian mass extinction, the first dinosaurs emerged in the late Triassic alongside pterosaurs and early mammals. A world of vast Pangean deserts and dense equatorial forests.",
    climate: "Arid, seasonally hot",
    diversity: "~50 known genera",
    genera: ["Coelophysis", "Eoraptor", "Plateosaurus", "Herrerasaurus"],
  },
  {
    era: "Jurassic",
    range: "201–145 MYA",
    blurb:
      "The age of giants. Sauropods achieved their greatest diversity and size. Pangea fragmented, creating shallow seaways and lush forests. Archaeopteryx bridged theropod dinosaurs and modern birds.",
    climate: "Warm, humid, greenhouse",
    diversity: "~330 known genera",
    genera: ["Brachiosaurus", "Stegosaurus", "Allosaurus", "Diplodocus"],
  },
  {
    era: "Cretaceous",
    range: "145–66 MYA",
    blurb:
      "The most diverse chapter of dinosaur evolution. Flowering plants revolutionized ecosystems. Ceratopsians, hadrosaurs, and ankylosaurs flourished. Ended 66 MYA in the Chicxulub impact event.",
    climate: "Warm, high sea levels",
    diversity: "~1,100 known genera",
    genera: ["Tyrannosaurus", "Triceratops", "Velociraptor", "Spinosaurus"],
  },
];

/** Era → accent color token (drives era tags, underlines, timeline bar). */
export const ERA_COLOR: Record<Era, string> = {
  Triassic: "text-paleo-triassic",
  Jurassic: "text-paleo-jurassic",
  Cretaceous: "text-paleo-cretaceous",
};

/** Diet → dot color token for the color-coded diet marker. */
export const DIET_COLOR: Record<Diet, string> = {
  Carnivore: "bg-paleo-carnivore",
  Herbivore: "bg-paleo-herbivore",
  Piscivore: "bg-paleo-piscivore",
};
