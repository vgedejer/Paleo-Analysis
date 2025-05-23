import pandas as pd
import numpy as np
import requests as rq
import bs4 as soup
import io
import re
import sqlite3
import time

# Establishing some constants
nondinos = ['Krzyzanowskisaurus', 'Actiosaurus', 'Volgavis', 'Yacoraitichnus', 'Yezosaurus', 'Brasileosaurus', 'Subtiliolithus', 'Fuscinapedis', 'Himeoolithus', 'Protoavis', 'Salfitichnus', 'Nyasasaurus']
no_webpage = ['Crateropteryx', 'Bellulornis', 'Alethoalaornis', 'Eopengornis', 'Fortunguavis', 'Gretcheniao', 'Holbotia', 'Linyiornis', 'Microenantiornis', 'Monoenantiornis', 'Otogornis', 'Pterygornis', 'Shangyang', 'Horezmavis', 'Platanavis']
orders = ['Ornithischia', 'Saurischia']
suborders = ['Neornithischia', 'Thyreophora', 'Sauropodomorpha', 'Theropoda']
infraorders = ['Ornithopoda', 'Ceratopsia', 'Pachycephalosauria', 'Stegosauria', 'Ankylosauria', 'Sauropoda', 'Titanosauria', 'Avialae', 'Non-Avian']

# Creating a dictionary to use when the dinosaur is noted to be avian
avian = {'Order': orders[1], 'Suborder': suborders[3], 'Infraorder': infraorders[7], 'Family': ''}

# Get PaleoDB data
# Returns a dataframe from the PaleoDB
def get_df(url):
    url_data = rq.get(url)
    if url_data.status_code == 200:
        return pd.read_csv(io.StringIO(url_data.content.decode('utf-8')))
    else:
        raise ValueError(f"Error: {url_data.status_code} - {url_data.reason}")

# Sort taxa ages
# This function takes a dataframe of taxa and sorts them into Mesozoic ages, periods, and epochs
def sort_taxa_ages(taxa):
    # Looking at the dataframe, we need to clean the columns relating to species lifetime --> Some dinosaurs have NaN as their entries for Early and Late Ages
    periods = ['Triassic', 'Jurassic', 'Cretaceous']
    epochs = ['Lower', 'Middle', 'Upper']


    tri_ages = ['Induan', 'Olenekian', 'Anisian', 'Ladinian', 'Carnian', 'Norian', 'Rhaetian']
    jur_ages = ['Hettangian', 'Sinemurian', 'Pliensbachian', 'Toarcian', 'Aalenian', 'Bajocian', 'Bathonian', 'Callovian', 'Oxfordian', 'Kimmeridgian', 'Tithonian']
    cre_ages = ['Berriasian', 'Valanginian', 'Hauterivian', 'Barremian', 'Aptian', 'Albian', 'Cenomanian', 'Turonian', 'Coniacian', 'Santonian', 'Campanian', 'Maastrichtian']

    low_ep = ['Induan', 'Olenekian', 'Hettangian', 'Sinemurian', 'Pliensbachian', 'Toarcian', 'Berriasian', 'Valanginian', 'Hauterivian', 'Barremian', 'Aptian', 'Albian']
    mid_ep = ['Anisian', 'Ladinian', 'Aalenian', 'Bajocian', 'Bathonian', 'Callovian']
    upp_ep = ['Carnian', 'Norian', 'Rhaetian', 'Oxfordian', 'Kimmeridgian', 'Tithonian', 'Cenomanian', 'Turonian', 'Coniacian', 'Santonian', 'Campanian', 'Maastrichtian']


    ages = [*tri_ages, *jur_ages, *cre_ages]

    # Arguements for Age
    mya_args = lambda x : [(taxa[x] <= 251.9) & (taxa[x] > 251.2), 
                    (taxa[x] <= 251.2) & (taxa[x] > 247.2),
                    (taxa[x] <= 247.2) & (taxa[x] > 242),
                    (taxa[x] <= 242) & (taxa[x] > 237),
                    (taxa[x] <= 237) & (taxa[x] > 227),
                    (taxa[x] <= 227) & (taxa[x] > 208.5),
                    (taxa[x] <= 208.5) & (taxa[x] > 201.4),
                    (taxa[x] <= 201.4) & (taxa[x] > 199.5),
                    (taxa[x] <= 199.5) & (taxa[x] > 192.9),
                    (taxa[x] <= 192.9) & (taxa[x] > 184.2),
                    (taxa[x] <= 184.2) & (taxa[x] > 174.7),
                    (taxa[x] <= 174.7) & (taxa[x] > 170.9),
                    (taxa[x] <= 170.9) & (taxa[x] > 168.2),
                    (taxa[x] <= 168.2) & (taxa[x] > 165.3),
                    (taxa[x] <= 165.3) & (taxa[x] > 161.5),
                    (taxa[x] <= 161.5) & (taxa[x] > 154.8),
                    (taxa[x] <= 154.8) & (taxa[x] > 149.2),
                    (taxa[x] <= 149.2) & (taxa[x] > 145),
                    (taxa[x] <= 145) & (taxa[x] > 139.8),
                    (taxa[x] <= 139.8) & (taxa[x] > 132.6),
                    (taxa[x] <= 132.6) & (taxa[x] > 125.77),
                    (taxa[x] <= 125.77) & (taxa[x] > 121.4),
                    (taxa[x] <= 121.4) & (taxa[x] > 113),
                    (taxa[x] <= 113) & (taxa[x] > 100.5),
                    (taxa[x] <= 100.5) & (taxa[x] > 93.9),
                    (taxa[x] <= 93.9) & (taxa[x] > 89.8),
                    (taxa[x] <= 89.8) & (taxa[x] > 86.3),
                    (taxa[x] <= 86.3) & (taxa[x] > 83.6),
                    (taxa[x] <= 83.6) & (taxa[x] > 72.1),
                    (taxa[x] <= 72.1) & (taxa[x] > 66)] 
                    
    # Arguments for Period and Epoch (will combine into one column later)
    pers = lambda x : [(taxa[x].isin(tri_ages)),
                    (taxa[x].isin(jur_ages)),
                    (taxa[x].isin(cre_ages))]

    eps = lambda x: [(taxa[x].isin(low_ep)),
                    (taxa[x].isin(mid_ep)),
                    (taxa[x].isin(upp_ep))]


    # Adding the Period and Age columns
    taxa['Early Age'] = np.select(mya_args('Max MYA'), ages, default=pd.NaT)

    # We add 0.01 to accomodate for edge cases where a dinosaur is estimated to have lived at the cusp of two mesozoic ages
    taxa['Min MYA'] += 0.01
    taxa['Late Age'] = np.select(mya_args('Min MYA'), ages, default=pd.NaT)
    taxa['Min MYA'] -= 0.01
    taxa['Late Age'] = taxa['Late Age'].fillna(taxa['Early Age'])

    taxa['Early Period'] = np.select(eps('Early Age'), epochs, default=pd.NaT) + ' ' + np.select(pers('Early Age'), periods, default=pd.NaT)
    taxa['Late Period'] = np.select(eps('Late Age'), epochs, default=pd.NaT) + ' ' + np.select(pers('Late Age'), periods, default=pd.NaT)

    # Adding a lifespan column to show how long each species/genus lived
    taxa['Lifespan (MYA)'] = taxa['Max MYA'] - taxa['Min MYA']

    return taxa

# Helper function that finds the corresponding wikipedia page for each dinosaur
def get_webpage(genus):
    
    # Edge case when looking up Qianlong and Wulong since they redirect to different pages
    if genus == 'Qianlong':
        return get_webpage('Qianlong shouhu')
    elif genus == 'Wulong':
        return get_webpage('Wulong bohaiensis')
   
   # Web scraping each genus name to figure out classification
    try:
        page = f'https://en.wikipedia.org/wiki/{genus}'
        response = rq.get(page)
      
        biota = soup.BeautifulSoup(response.text, 'html.parser')
        
        # Checking for informal dinosaurs
        if ('informally named dinosaurs' in biota.find('title').text) or (genus in ['Tiantaisaurus', 'Khanazeem']):
            return 'Informally Named Dinosaur'
        else:
            biota = biota.find('table', {'class': 'infobox biota'}).find_all('tr')
      
    except:
      
      # Covering case where the genus is named after an existing topic
        try:
            page = f'https://en.wikipedia.org/wiki/{genus}_(dinosaur)'
            response = rq.get(page)
      
            biota = soup.BeautifulSoup(response.text, 'html.parser').find('table', {'class': 'infobox biota'}).find_all('tr')
      
        except:
            pass
   
    return biota

def wiki_scrape_genus(biota):
   # Defining the dictionary that will be put into the dataframe
   data = {'Order':'', 'Suborder':'', 'Infraorder':'', 'Family':''}
   
   # iterating through rows that feature classification terms
   for row in biota:
      biota_data = row.find_all('td')
      
      try:
         bio_class = re.match(r'([A-Z][a-z]*)', biota_data.pop(0).text.strip())[0]
         
         # Only iterating through Clades, Families, and Genera
         if bio_class in ['Clade', 'Family', 'Genus']:
            bio_name = re.match(r'([^A-Za-z][A-Z][a-z]*)|([A-Z][a-z]*)', biota_data.pop(0).text.strip())[0]
            bio_name = re.sub('†', '', bio_name)
            
            # Setting values for Order, Suborder, and Infraorder
            if bio_class in ['Clade', 'Superfamily']:
               if bio_name in orders:
                  data['Order'] = bio_name
                  
               elif bio_name in suborders:
                  data['Suborder'] = bio_name
                  
                  # Setting Default Value for Theropods to be non-avian
                  if bio_name == 'Theropoda':
                     data['Infraorder'] = 'Non-Avian'

                  # Setting Default Value for Sauropods to be Sauropoda 
                  elif bio_name == 'Sauropodamorpha':
                     data['Infraorder'] = 'Sauropoda'      
                     
                                 
               elif bio_name in infraorders:
                  data['Infraorder'] = bio_name
                     
               # Including edge case of Euornithes since they are also Late Mesozoic Avians
               elif bio_name == 'Euornithes':
                  data = avian
                  
         
            elif bio_class == 'Family':
               data['Family'] = bio_name                         
               
         # In the event that the wikipedia page is not labelled with Dinosauria
         if bio_class == 'Class':
            bio_name = re.match(r'([^A-Za-z][A-Z][a-z]*)|([A-Z][a-z]*)', biota_data.pop(0).text.strip())[0]
            
            if bio_name == 'Aves':
               data = avian       
      
      except:
         pass
      
   return data

def main():
    
    # Get PaleoDB data and create the dataframe
    print('Creating occurrences dataframe...')
    
    occ = get_df('https://paleobiodb.org/data1.2/occs/list.csv?base_name=Dinosauria&taxon_reso=species&idqual=certain&pres=regular&max_ma=252&min_ma=65&show=class,coords,loc,strat,acconly')
    occ = occ[['accepted_name', 'lng', 'lat', 'formation', 'cc', 'state', 'county', 'collection_no']]
    occ.columns = ['Species', 'Longitude', 'Latitude', 'Formation', 'Country', 'State', 'County', 'Collection']
    
    print('Finished creating occurrences dataframe!\nCreating taxa dataframes...')
    
    taxa = get_df('https://paleobiodb.org/data1.2/occs/taxa.csv?base_name=Dinosauria&idreso=species&idqual=certain&pres=regular&max_ma=252&min_ma=65&show=class,size,app,ecospace,img')

    taxa = taxa[['taxon_rank', 'taxon_name', 'genus', 'family', 'taxon_size', 'diet', 'firstapp_max_ma', 'lastapp_min_ma']]
    taxa = taxa.dropna(subset=['taxon_name']).query('(taxon_rank == \'genus\') or (taxon_rank == \'species\')')
    taxa.columns = ['Rank', 'Name', 'Genus', 'Family', 'Taxon Size', 'Diet', 'Max MYA', 'Min MYA']
    
    taxa = taxa.replace(regex=['NO_FAMILY_SPECIFIED'], value='')

    taxa['Diet'] = taxa['Diet'].str.capitalize()
    
    taxa = sort_taxa_ages(taxa)
    
    species = taxa.loc[taxa['Rank'] == 'species'].reset_index().drop(columns=['Rank', 'Taxon Size', 'Family', 'index'])
    genus = taxa.loc[taxa['Rank'] == 'genus'].reset_index().drop(columns=['Rank', 'Genus', 'index'])

    # Dropping this count by 1 because because the genus in the original dataframe was counted towards the taxon size
    genus['Taxon Size'] = genus['Taxon Size'].astype(int) - 1

    # Adding columns for informal dinosaurs
    genus['Informal'] = False

    # Renaming mislabelled dinosaurs
    genus.at[genus.index[genus['Name'] == 'Megalosaurus (Poekilopleuron)'].values[0], 'Name'] = 'Poekilopleuron'
    genus.at[genus.index[genus['Name'] == 'Bellulia'].values[0], 'Name'] = 'Bellulornis'

    # Removing genera that are informally named, are trace/egg fossils, or don't have web pages to get data from
    for i in nondinos + no_webpage:
        try:
            x = genus.index[genus['Name'] == i].values[0]
            genus = genus.drop(axis=0, index=x)
        except:
            pass
    genus = genus.reset_index()
    
    genus['Order'] = ''
    genus['Suborder'] = ''
    genus['Infraorder'] = ''

    genus = genus[['Name', 'Family', 'Infraorder', 'Suborder', 'Order', 'Informal', 'Taxon Size', 'Diet', 'Max MYA', 'Min MYA', 'Lifespan (MYA)', 'Early Age', 'Late Age', 'Early Period', 'Late Period']]

    print('Finished creating taxa dataframes!\nScraping taxa data...')
    
    start_time = time.perf_counter()

    for i, row in genus.iterrows():
        
        try:
            dino = genus.iloc[i]['Name']
            
            biota = get_webpage(dino)
            if (biota == 'Informally Named Dinosaur'):
                genus.at[i, 'Informal'] = True
            else:
                wiki_data = wiki_scrape_genus(biota)
                for col in wiki_data:
                    genus.loc[i, col] = wiki_data[col]
                    
        except:
            if genus.iloc[i]['Family'] != '':
                try:
                    fam = genus.iloc[i]['Family']
                    biota = get_webpage(dino)
                    wiki_data = wiki_scrape_genus(biota)
                    for col in wiki_data:
                        genus.loc[i, col] = wiki_data[col]
                except:
                    pass
                
    end_time = time.perf_counter()
    elapsed = end_time - start_time
                
    genus = genus.rename(columns={'Name':'Genus'})
    species = species.rename(columns={'Name':'Species'})
            
    print(f'Finished scraping taxa data in {elapsed:.4f}!\nCreating SQL tables...')

    conn = sqlite3.connect("paleo.db")
    print("Database paleo.db formed")
    
    # Push the dataframe to sql 
    occ.to_sql("occurrences", conn, if_exists="replace")
    genus.to_sql("genera", conn, if_exists="replace")
    species.to_sql("species", conn, if_exists="replace")
    
    print('Finished creating SQL tables!')

    
if __name__ == "__main__":
    main()
