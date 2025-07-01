import sqlite3
import time
import constants
import helpers

def main():
    
    # Get PaleoDB data and create the dataframe
    print('Creating occurrences dataframe...')
    
    occ = helpers.get_df('https://paleobiodb.org/data1.2/occs/list.csv?base_name=Dinosauria&taxon_reso=species&idqual=certain&pres=regular&max_ma=252&min_ma=65&show=class,coords,loc,strat,acconly,paleoloc')
    occ = occ[['accepted_name', 'lng', 'lat', 'formation', 'cc', 'state', 'county', 'collection_no', 'geogcomments', 'paleolng', 'paleolat', 'geoplate', 'stratgroup', 'member', 'paleomodel']]
    occ.columns = ['Fossil', 'Longitude', 'Latitude', 'Formation', 'Country', 'State', 'County', 'Collection', 'GeoComments', 'PaleoLongitude', 'PaleoLatitude', 'GeoPlate', 'StratGroup', 'Member', 'PaleoModel']
    
    print('Finished creating occurrences dataframe!\nCreating taxa dataframes...')
    
    taxa = helpers.get_df('https://paleobiodb.org/data1.2/occs/taxa.csv?base_name=Dinosauria&idreso=species&idqual=certain&pres=regular&max_ma=252&min_ma=65&show=class,size,app,ecospace,img')

    taxa = taxa[['taxon_rank', 'taxon_name', 'genus', 'family', 'taxon_size', 'diet', 'firstapp_max_ma', 'lastapp_min_ma']]
    taxa = taxa.dropna(subset=['taxon_name']).query('(taxon_rank == \'genus\') or (taxon_rank == \'species\')')
    taxa.columns = ['Rank', 'Name', 'Genus', 'Family', 'TaxonSize', 'Diet', 'MaxMYA', 'MinMYA']
    
    taxa = taxa.replace(regex=['NO_FAMILY_SPECIFIED'], value='')

    taxa['Diet'] = taxa['Diet'].str.capitalize()
    
    taxa = helpers.sort_taxa_ages(taxa)
    
    species = taxa.loc[taxa['Rank'] == 'species'].reset_index().drop(columns=['Rank', 'TaxonSize', 'Family', 'index'])
    genus = taxa.loc[taxa['Rank'] == 'genus'].reset_index().drop(columns=['Rank', 'Genus', 'index'])

    # Dropping this count by 1 because because the genus in the original dataframe was counted towards the taxon size
    genus['TaxonSize'] = genus['TaxonSize'].astype(int) - 1

    # Adding columns for informal dinosaurs
    genus['Informal'] = False

    # Renaming mislabelled dinosaurs
    genus.at[genus.index[genus['Name'] == 'Megalosaurus (Poekilopleuron)'].values[0], 'Name'] = 'Poekilopleuron'
    genus.at[genus.index[genus['Name'] == 'Bellulia'].values[0], 'Name'] = 'Bellulornis'

    # Removing genera that are informally named, are trace/egg fossils, or don't have web pages to get data from
    for i in constants.INFORMAL + constants.NO_PAGE:
        try:
            x = genus.index[genus['Name'] == i].values[0]
            genus = genus.drop(axis=0, index=x)
        except:
            pass
    genus = genus.reset_index()
    
    genus['Order'] = ''
    genus['Suborder'] = ''
    genus['Infraorder'] = ''

    genus = genus[['Name', 'Family', 'Infraorder', 'Suborder', 'Order', 'Informal', 'TaxonSize', 'Diet', 'MaxMYA', 'MinMYA', 'LifespanMYA', 'EarlyAge', 'LateAge', 'EarlyPeriod', 'LatePeriod']]

    print('Finished creating taxa dataframes!\nScraping taxa data...')
    
    start_time = time.perf_counter()

    for i, row in genus.iterrows():
        
        try:
            dino = genus.iloc[i]['Name']
            
            biota = helpers.get_webpage(dino)
            if (biota == 'Informally Named Dinosaur'):
                genus.at[i, 'Informal'] = True
            else:
                wiki_data = helpers.wiki_scrape_genus(biota)
                for col in wiki_data:
                    genus.loc[i, col] = wiki_data[col]
                    
        except:
            if genus.iloc[i]['Family'] != '':
                try:
                    fam = genus.iloc[i]['Family']
                    biota = helpers.get_webpage(dino)
                    wiki_data = helpers.wiki_scrape_genus(biota)
                    for col in wiki_data:
                        genus.loc[i, col] = wiki_data[col]
                except:
                    pass
                
    end_time = time.perf_counter()
    elapsed = end_time - start_time
                
    genus = genus.rename(columns={'Name':'Genus'})
    species = species.rename(columns={'Name':'Species'})
            
    print(f'Finished scraping taxa data in {elapsed:.4f}!\nCreating SQL tables...')

    conn = sqlite3.connect("../../paleo.db")
    print("Database paleo.database formed")
    
    # Push the dataframe to sql 
    occ.to_sql("dino_fossils", conn, if_exists="replace")
    genus.to_sql("dino_genera", conn, if_exists="replace")
    species.to_sql("dino_species", conn, if_exists="replace")
    
    print('Finished creating SQL tables!')
    
if __name__ == "__main__":
    main()
