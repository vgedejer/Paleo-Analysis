/**
 * ============================================================================
 *  DOMAIN TYPES  —  the frontend's contract with the FastAPI backend.
 * ============================================================================
 *
 *  Mental model for a backend dev:
 *  These interfaces are the TypeScript equivalent of your Pydantic response
 *  schemas (schemas/genus.py, schemas/fossil.py, schemas/species.py). They are
 *  the single source of truth for "what shape does the API hand me?".
 *
 *  The crucial difference from Pydantic:
 *  Pydantic *validates at runtime* — if the JSON is malformed, Pydantic throws.
 *  TypeScript interfaces are *erased at compile time* — they are pure
 *  documentation for the compiler and your editor. At runtime, `as Genus` is a
 *  promise to the compiler, not a guarantee from the network. (We discuss how
 *  to close that gap with a runtime validator like Zod in the README.)
 *
 *  NOTE ON CASING:
 *  Your API returns PascalCase keys (`Genus`, `MaxMYA`, `EarlyPeriod`) because
 *  the Pydantic models expose the original column names. JS/TS convention is
 *  camelCase. We deliberately keep these types PascalCase so they match the
 *  wire format 1:1 — no silent drift between backend and frontend. (The
 *  trade-off, and where you'd add a mapping layer, is covered in the README's
 *  interview-talking-points section.)
 */

/**
 * `Diet` is stored as a free-text string in the DB, but in practice only takes
 * a few values. This pattern — a union of known literals plus `(string & {})`
 * — gives you autocomplete for the common cases while still accepting any
 * string the backend might return. You get the ergonomics of an enum without
 * lying to the compiler about the data being closed.
 */
export type Diet = "Herbivore" | "Carnivore" | "Omnivore" | (string & {});

/** Shared identity field. Mirrors `model_config = from_attributes` + `id`. */
export interface Entity {
  id: number;
}

/* --------------------------------- Genus --------------------------------- */

/** Mirrors `GenusRead` (schemas/genus.py): the lightweight list/card shape. */
export interface Genus extends Entity {
  Genus: string;
  Family: string;
  Infraorder: string;
  Suborder: string;
  Order: string;
  Diet: Diet;
  EarlyPeriod: string;
  LatePeriod: string;
}

/**
 * Mirrors `GenusDetail`: the full record returned for a single genus.
 * `extends Genus` expresses the same inheritance your Pydantic models use
 * (`GenusDetailBase(GenusBase)`), so the relationship is explicit in the types.
 */
export interface GenusDetail extends Genus {
  Informal: boolean;
  TaxonSize: number;
  MaxMYA: number;
  MinMYA: number;
  LifespanMYA: number;
  EarlyAge: string;
  LateAge: string;
}

/* -------------------------------- Species -------------------------------- */

/** Mirrors `SpeciesRead`. */
export interface Species extends Entity {
  Species: string;
  Genus: string;
  Diet: Diet;
  EarlyPeriod: string;
  LatePeriod: string;
}

/* -------------------------------- Fossils -------------------------------- */

/** Mirrors `FossilRead`: the lightweight shape. */
export interface Fossil extends Entity {
  Fossil: string;
  Longitude: number;
  Latitude: number;
  Formation: string;
  Country: string;
  State: string;
}

/** Mirrors `FossilDetail`: full geolocation + collection metadata. */
export interface FossilDetail extends Fossil {
  County: string;
  PaleoLongitude: number;
  PaleoLatitude: number;
  Collection: number;
  GeoComments: string;
  GeoPlate: string;
  GeoGroup: string;
  Member: string;
  PaleoModel: string;
}
