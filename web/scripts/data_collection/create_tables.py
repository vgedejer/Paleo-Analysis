import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import constants
import helpers
import pandas as pd


PALEODB_BASE = 'https://paleobiodb.org/data1.2'
PALEODB_DEV  = 'https://dev.paleobiodb.org/data1.2'

OCC_PARAMS = '/occs/list.csv?base_name=Dinosauria&taxon_reso=species&idqual=certain&pres=regular&max_ma=252&min_ma=65&show=class,coords,loc,strat,acconly,paleoloc'
TAXA_PARAMS = '/occs/taxa.csv?base_name=Dinosauria&idreso=species&idqual=certain&pres=regular&max_ma=252&min_ma=65&show=class,size,app,ecospace,img'


def fetch_paleodb(path, label):
    """Try the main PaleoDB server, then fall back to dev."""
    try:
        return helpers.get_df(PALEODB_BASE + path)
    except Exception:
        print(f'Failed to retrieve {label} from PaleoDB! Trying dev server...')
    try:
        return helpers.get_df(PALEODB_DEV + path)
    except Exception:
        print(f'ERROR !!!! Failed to retrieve {label} from PaleoDB!')
        return None


def scrape_genus_row(i, name, family):
    """Scrape Wikipedia data for a single genus. Returns (index, dict | 'informal' | None)."""
    try:
        biota = helpers.get_webpage(name)
        if biota == 'Informally Named Dinosaur':
            return (i, 'informal')
        return (i, helpers.wiki_scrape_genus(biota))
    except Exception:
        if family:
            try:
                biota = helpers.get_webpage(family)
                return (i, helpers.wiki_scrape_genus(biota))
            except Exception:
                pass
    return (i, None)


def main():
    
    # Get PaleoDB data and create the dataframe
    print('Creating occurrences dataframe...')

    occ = fetch_paleodb(OCC_PARAMS, 'occurrence data')
    if occ is None:
        return
    
    occ = occ[['accepted_name', 'lng', 'lat', 'formation', 'cc', 'state', 'county', 'collection_no', 'geogcomments', 'paleolng', 'paleolat', 'geoplate', 'geological_group', 'member', 'paleomodel']]
    occ.columns = ['Fossil', 'Longitude', 'Latitude', 'Formation', 'Country', 'State', 'County', 'Collection', 'GeoComments', 'PaleoLongitude', 'PaleoLatitude', 'GeoPlate', 'GeoGroup', 'Member', 'PaleoModel']
    
    print('Finished creating occurrences dataframe!\nCreating taxa dataframes...')
    
    taxa = fetch_paleodb(TAXA_PARAMS, 'taxa data')
    if taxa is None:
        return

    taxa = taxa[['taxon_rank', 'taxon_name', 'genus', 'family', 'taxon_size', 'diet', 'firstapp_max_ma', 'lastapp_min_ma']]
    taxa = taxa.dropna(subset=['taxon_name']).query('taxon_rank == "genus" or taxon_rank == "species"')
    taxa.columns = ['Rank', 'Name', 'Genus', 'Family', 'TaxonSize', 'Diet', 'MaxMYA', 'MinMYA']
    
    taxa = taxa.replace(regex=['NO_FAMILY_SPECIFIED'], value='')

    taxa['Diet'] = taxa['Diet'].str.capitalize()
    
    taxa = helpers.sort_taxa_ages(taxa)
    
    species = taxa.loc[taxa['Rank'] == 'species'].reset_index().drop(columns=['Rank', 'TaxonSize', 'Family', 'index'])
    genus = taxa.loc[taxa['Rank'] == 'genus'].reset_index().drop(columns=['Rank', 'Genus', 'index'])

    # Dropping this count by 1 because the genus in the original dataframe was counted towards the taxon size
    genus['TaxonSize'] = genus['TaxonSize'].astype(int) - 1

    # Adding columns for informal dinosaurs
    genus['Informal'] = False

    # Renaming mislabelled dinosaurs
    genus.loc[genus['Name'] == 'Megalosaurus (Poekilopleuron)', 'Name'] = 'Poekilopleuron'
    genus.loc[genus['Name'] == 'Bellulia', 'Name'] = 'Bellulornis'

    # Removing genera that are informally named, are trace/egg fossils, or don't have web pages to get data from
    genus = genus[~genus['Name'].isin(constants.INFORMAL + constants.NO_PAGE)].reset_index(drop=True)
    
    genus['Order'] = ''
    genus['Suborder'] = ''
    genus['Infraorder'] = ''

    genus = genus[['Name', 'Family', 'Infraorder', 'Suborder', 'Order', 'Informal', 'TaxonSize', 'Diet', 'MaxMYA', 'MinMYA', 'LifespanMYA', 'EarlyAge', 'LateAge', 'EarlyPeriod', 'LatePeriod']]

    print('Finished creating taxa dataframes!\nScraping taxa data...')
    
    start_time = time.perf_counter()

    # Scrape Wikipedia pages in parallel (I/O-bound)
    max_workers = 8
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(scrape_genus_row, i, row['Name'], row['Family']): i
            for i, row in genus.iterrows()
        }
        for count, future in enumerate(as_completed(futures), 1):
            i, result = future.result()
            name = genus.at[i, 'Name']
            print(f'Scraped {count}/{len(genus)}: {name}')
            if result == 'informal':
                genus.at[i, 'Informal'] = True
            elif result is not None:
                for col, val in result.items():
                    genus.at[i, col] = val

    elapsed = time.perf_counter() - start_time
                
    genus = genus.rename(columns={'Name':'Genus'})
    species = species.rename(columns={'Name':'Species'})
            
    print(f'Finished scraping taxa data in {elapsed:.4f}s!\nCreating SQL tables...')

    conn = sqlite3.connect("../paleo.db")
    try:
        occ.to_sql("dino_fossils", conn, if_exists="replace")
        genus.to_sql("dino_genera", conn, if_exists="replace")
        species.to_sql("dino_species", conn, if_exists="replace")
        print('Finished creating SQL tables!')
    finally:
        conn.close()

    
if __name__ == "__main__":
    main()
