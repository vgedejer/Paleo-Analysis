"""Ingest one taxonomic group from PaleoDB into the Alembic-managed database.

This is a duplicate of create_tables.py, adjusted to:
  * target the configured database (PALEO_DATABASE_URL / Supabase) through
    SQLAlchemy instead of a hardcoded local SQLite file;
  * parameterize the taxonomic group via --base-name (default "Dinosauria"), so
    adding mammals / pterosaurs / etc. later is one more run, not new tables;
  * write into the shared genera/species/fossils tables with real foreign keys,
    tagging every row with its `clade`, and refresh idempotently per clade
    (a re-run replaces only that clade's rows).

Prerequisite: the schema must already exist — run `alembic upgrade head`
against the target database first (this script does not create tables).

Examples:
    python populate_db.py                          # Dinosauria (default)
    python populate_db.py --base-name Dinosauria
    python populate_db.py --base-name Mammalia --no-wiki
"""
from __future__ import annotations

import argparse
import logging
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

import constants
import helpers

# Make the app package importable so we reuse its engine + ORM table defs
# (single source of truth for the schema). scripts/data_collection -> web/app.
APP_DIR = Path(__file__).resolve().parents[2] / "app"
sys.path.insert(0, str(APP_DIR))

from sqlalchemy import delete, insert, inspect, select  # noqa: E402
from sqlalchemy.engine import make_url  # noqa: E402
from db.session import engine  # noqa: E402
from models.fossil import Fossil  # noqa: E402
from models.genus import Genus  # noqa: E402
from models.species import Species  # noqa: E402

logger = logging.getLogger(__name__)

PALEODB_BASE = "https://paleobiodb.org/data1.2"
PALEODB_DEV = "https://dev.paleobiodb.org/data1.2"

OCC_TEMPLATE = (
    "/occs/list.csv?base_name={base}&taxon_reso=species&idqual=certain"
    "&pres=regular&max_ma={max_ma}&min_ma={min_ma}"
    "&show=class,coords,loc,strat,acconly,paleoloc"
)
TAXA_TEMPLATE = (
    "/occs/taxa.csv?base_name={base}&idreso=species&idqual=certain"
    "&pres=regular&max_ma={max_ma}&min_ma={min_ma}&show=class,size,app,ecospace,img"
)

# Column sets per table (must match the ORM models). `clade` and `genus_id` are
# added by the writer, so they're not listed here.
GENUS_COLS = [
    "Genus", "Family", "Infraorder", "Suborder", "Order", "Informal",
    "TaxonSize", "Diet", "MaxMYA", "MinMYA", "LifespanMYA",
    "EarlyAge", "LateAge", "EarlyPeriod", "LatePeriod",
]
SPECIES_COLS = [
    "Species", "Genus", "Diet", "MaxMYA", "MinMYA", "LifespanMYA",
    "EarlyAge", "LateAge", "EarlyPeriod", "LatePeriod",
]
FOSSIL_COLS = [
    "Fossil", "Longitude", "Latitude", "Formation", "Country", "State",
    "County", "Collection", "GeoComments", "PaleoLongitude", "PaleoLatitude",
    "GeoPlate", "GeoGroup", "Member", "PaleoModel",
]


def fetch_paleodb(path, label):
    """Try the main PaleoDB server, then fall back to dev."""
    try:
        return helpers.get_df(PALEODB_BASE + path)
    except Exception:
        logger.warning(f"Failed to retrieve {label} from PaleoDB! Trying dev server...")
    try:
        return helpers.get_df(PALEODB_DEV + path)
    except Exception:
        logger.error(f"ERROR !!!! Failed to retrieve {label} from PaleoDB!")
        return None


def scrape_genus_row(i, name, family):
    """Scrape Wikipedia data for a single genus. Returns (index, dict | 'informal' | None)."""
    try:
        biota = helpers.get_webpage(name)
        if biota == "Informally Named Dinosaur":
            return (i, "informal")
        return (i, helpers.wiki_scrape_genus(biota))
    except Exception:
        if family:
            try:
                biota = helpers.get_webpage(family)
                return (i, helpers.wiki_scrape_genus(biota))
            except Exception:
                pass
    return (i, None)


def build_frames(base_name, max_ma, min_ma, do_wiki, max_workers):
    """Fetch + transform PaleoDB data into (genus, species, occ) dataframes.

    This mirrors the original create_tables.py transformation exactly; only the
    PaleoDB query parameters are parameterized and the Wikipedia classification
    pass is made optional (it is Dinosauria-specific).
    """
    logger.info("Creating occurrences dataframe...")
    occ = fetch_paleodb(
        OCC_TEMPLATE.format(base=base_name, max_ma=max_ma, min_ma=min_ma),
        "occurrence data",
    )
    if occ is None:
        return None

    occ = occ[["accepted_name", "lng", "lat", "formation", "cc", "state", "county",
               "collection_no", "geogcomments", "paleolng", "paleolat", "geoplate",
               "geological_group", "member", "paleomodel"]]
    occ.columns = ["Fossil", "Longitude", "Latitude", "Formation", "Country", "State",
                   "County", "Collection", "GeoComments", "PaleoLongitude",
                   "PaleoLatitude", "GeoPlate", "GeoGroup", "Member", "PaleoModel"]

    logger.info("Finished creating occurrences dataframe!\nCreating taxa dataframes...")
    taxa = fetch_paleodb(
        TAXA_TEMPLATE.format(base=base_name, max_ma=max_ma, min_ma=min_ma),
        "taxa data",
    )
    if taxa is None:
        return None

    taxa = taxa[["taxon_rank", "taxon_name", "genus", "family", "taxon_size", "diet",
                 "firstapp_max_ma", "lastapp_min_ma"]]
    taxa = taxa.dropna(subset=["taxon_name"]).query('taxon_rank == "genus" or taxon_rank == "species"')
    taxa.columns = ["Rank", "Name", "Genus", "Family", "TaxonSize", "Diet", "MaxMYA", "MinMYA"]

    taxa = taxa.replace(regex=["NO_FAMILY_SPECIFIED"], value="")
    taxa["Diet"] = taxa["Diet"].str.capitalize()
    taxa = helpers.sort_taxa_ages(taxa)

    species = taxa.loc[taxa["Rank"] == "species"].reset_index().drop(columns=["Rank", "TaxonSize", "Family", "index"])
    genus = taxa.loc[taxa["Rank"] == "genus"].reset_index().drop(columns=["Rank", "Genus", "index"])

    # The genus row is counted toward its own taxon size in the source data.
    genus["TaxonSize"] = genus["TaxonSize"].astype(int) - 1
    genus["Informal"] = False

    # Renaming mislabelled dinosaurs
    genus.loc[genus["Name"] == "Megalosaurus (Poekilopleuron)", "Name"] = "Poekilopleuron"
    genus.loc[genus["Name"] == "Bellulia", "Name"] = "Bellulornis"

    # Remove genera that are informally named, are trace/egg fossils, or lack pages.
    genus = genus[~genus["Name"].isin(constants.INFORMAL + constants.NO_PAGE)].reset_index(drop=True)

    genus["Order"] = ""
    genus["Suborder"] = ""
    genus["Infraorder"] = ""
    genus = genus[["Name", "Family", "Infraorder", "Suborder", "Order", "Informal",
                   "TaxonSize", "Diet", "MaxMYA", "MinMYA", "LifespanMYA",
                   "EarlyAge", "LateAge", "EarlyPeriod", "LatePeriod"]]

    if do_wiki:
        logger.info("Finished creating taxa dataframes!\nScraping taxa data...")
        start_time = time.perf_counter()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(scrape_genus_row, i, row["Name"], row["Family"]): i
                for i, row in genus.iterrows()
            }
            for future in as_completed(futures):
                i, result = future.result()
                if result == "informal":
                    genus.at[i, "Informal"] = True
                elif result is not None:
                    for col, val in result.items():
                        genus.at[i, col] = val
        logger.info(f"Finished scraping taxa data in {time.perf_counter() - start_time:.4f}s!")
    else:
        logger.info("Skipping Wikipedia classification pass (--no-wiki / non-Dinosauria).")

    genus = genus.rename(columns={"Name": "Genus"})
    species = species.rename(columns={"Name": "Species"})
    return genus, species, occ


def _clean(value, as_int=False):
    """Coerce a pandas/numpy cell to a native Python value Postgres will accept."""
    if isinstance(value, np.generic):
        value = value.item()
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if as_int and value is not None:
        return int(value)
    return value


def _records(df, columns, clade, int_columns=()):
    """Turn selected dataframe columns into insert dicts, NaN -> None, tagged clade."""
    cols = [c for c in columns if c in df.columns]
    records = []
    for _, row in df[cols].iterrows():
        rec = {"clade": clade}
        for c in cols:
            rec[c] = _clean(row[c], as_int=c in int_columns)
        records.append(rec)
    return records


def write_to_db(genus, species, occ, clade):
    """Replace this clade's rows in genera/species/fossils, wiring real FKs.

    Genera are inserted first so the database assigns ids; we then read those
    ids back (scoped to the clade) to populate genus_id on species and fossils.
    """
    genera_tbl, species_tbl, fossils_tbl = Genus.__table__, Species.__table__, Fossil.__table__

    inspector = inspect(engine)
    missing = [t.name for t in (genera_tbl, species_tbl, fossils_tbl) if not inspector.has_table(t.name)]
    if missing:
        raise SystemExit(
            f"Missing tables {missing}. Run `alembic upgrade head` against the "
            f"target database before ingesting."
        )

    genus_records = _records(genus, GENUS_COLS, clade, int_columns=("TaxonSize",))
    species_records = _records(species, SPECIES_COLS, clade)
    fossil_records = _records(occ, FOSSIL_COLS, clade, int_columns=("Collection",))

    with engine.begin() as conn:
        # Idempotent per clade: clear children before parents (FK order).
        conn.execute(delete(fossils_tbl).where(fossils_tbl.c.clade == clade))
        conn.execute(delete(species_tbl).where(species_tbl.c.clade == clade))
        conn.execute(delete(genera_tbl).where(genera_tbl.c.clade == clade))

        if genus_records:
            conn.execute(insert(genera_tbl), genus_records)

        # Genus name -> id, scoped to this clade, from the just-inserted rows.
        name_to_id = {
            name: gid
            for gid, name in conn.execute(
                select(genera_tbl.c.id, genera_tbl.c.Genus).where(genera_tbl.c.clade == clade)
            )
        }

        for rec in species_records:
            rec["genus_id"] = name_to_id.get(rec.get("Genus"))
        if species_records:
            conn.execute(insert(species_tbl), species_records)

        for rec in fossil_records:
            fossil_name = rec.get("Fossil") or ""
            genus_name = fossil_name.split()[0] if fossil_name else None
            rec["genus_id"] = name_to_id.get(genus_name)
        if fossil_records:
            conn.execute(insert(fossils_tbl), fossil_records)

    return len(genus_records), len(species_records), len(fossil_records)


def _configure_logging():
    log_dir = Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(log_dir / "populate_db.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Ingest a taxonomic group from PaleoDB into the database.")
    p.add_argument("--base-name", default="Dinosauria",
                   help="PaleoDB base taxon to ingest (also stored as `clade`). Default: Dinosauria.")
    p.add_argument("--max-ma", type=float, default=252, help="Oldest age bound in Ma. Default: 252.")
    p.add_argument("--min-ma", type=float, default=65, help="Youngest age bound in Ma. Default: 65.")
    p.add_argument("--max-workers", type=int, default=8, help="Threads for Wikipedia scraping. Default: 8.")
    wiki = p.add_mutually_exclusive_group()
    wiki.add_argument("--wiki", dest="wiki", action="store_true", default=None,
                      help="Force the Wikipedia classification pass on.")
    wiki.add_argument("--no-wiki", dest="wiki", action="store_false",
                      help="Skip the (Dinosauria-specific) Wikipedia classification pass.")
    p.add_argument("--test", action="store_true", help="Verify Wikipedia scraping works, then exit.")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    _configure_logging()

    if args.test:
        logger.info("TEST MODE - scraping a single page to verify scraping works.")
        print(helpers.wiki_scrape_genus(helpers.get_webpage("Archaeopteryx")))
        return

    clade = args.base_name
    # Default: only run the dinosaur-specific Wikipedia pass for Dinosauria.
    do_wiki = args.wiki if args.wiki is not None else (clade == "Dinosauria")

    logger.info(f"Ingesting base_name={clade} into {make_url(str(engine.url)).render_as_string(hide_password=True)}")
    print(f"Target DB: {make_url(str(engine.url)).render_as_string(hide_password=True)}")
    print(f"Ingesting base_name={clade} (wiki={do_wiki})...")

    frames = build_frames(clade, args.max_ma, args.min_ma, do_wiki, args.max_workers)
    if frames is None:
        logger.error("Aborting: could not fetch PaleoDB data.")
        return
    genus, species, occ = frames

    logger.info("Writing to database...")
    n_g, n_s, n_f = write_to_db(genus, species, occ, clade)
    msg = f"Done. Wrote {n_g} genera, {n_s} species, {n_f} fossils for clade '{clade}'."
    logger.info(msg)
    print(msg)
    logger.info("------------------- All done! -------------------")


if __name__ == "__main__":
    main()
