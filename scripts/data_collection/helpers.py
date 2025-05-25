import constants
import pandas as pd
import numpy as np
import requests as rq
import bs4 as soup
import io
import re

# an ORGANIZED kitchen drawer of helper methods for the Main function

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

    ages = [*constants.TRIASSIC_AGES, *constants.JURASSIC_AGES, *constants.CRETACEOUS_AGES]

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
    pers = lambda x : [(taxa[x].isin(constants.TRIASSIC_AGES)),
                    (taxa[x].isin(constants.JURASSIC_AGES)),
                    (taxa[x].isin(constants.CRETACEOUS_AGES))]

    eps = lambda x: [(taxa[x].isin(constants.LOW_EP)),
                    (taxa[x].isin(constants.MID_EP)),
                    (taxa[x].isin(constants.UPP_EP))]


    # Adding the Period and Age columns
    taxa['Early Age'] = np.select(mya_args('Max MYA'), ages, default=pd.NaT)

    # We add 0.01 to accomodate for edge cases where a dinosaur is estimated to have lived at the cusp of two mesozoic ages
    taxa['Min MYA'] += 0.01
    taxa['Late Age'] = np.select(mya_args('Min MYA'), ages, default=pd.NaT)
    taxa['Min MYA'] -= 0.01
    taxa['Late Age'] = taxa['Late Age'].fillna(taxa['Early Age'])

    taxa['Early Period'] = np.select(eps('Early Age'), constants.EPOCHS, default=pd.NaT) + ' ' + np.select(pers('Early Age'), constants.PERIODS, default=pd.NaT)
    taxa['Late Period'] = np.select(eps('Late Age'), constants.EPOCHS, default=pd.NaT) + ' ' + np.select(pers('Late Age'), constants.PERIODS, default=pd.NaT)

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

# Scrapes the classification from the wikipedia page
# This function returns a dictionary with the Order, Suborder, Infraorder, and Family of the dinosaur
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
               if bio_name in constants.ORDERS:
                  data['Order'] = bio_name
                  
               elif bio_name in constants.SUBORDERS:
                  data['Suborder'] = bio_name
                  
                  # Setting Default Value for Theropods to be non-avian
                  if bio_name == 'Theropoda':
                     data['Infraorder'] = 'Non-Avian'

                  # Setting Default Value for Sauropods to be Sauropoda 
                  elif bio_name == 'Sauropodamorpha':
                     data['Infraorder'] = 'Sauropoda'      
                     
                                 
               elif bio_name in constants.INFRAORDERS:
                  data['Infraorder'] = bio_name
                     
               # Including edge case of Euornithes since they are also Late Mesozoic Avians
               elif bio_name == 'Euornithes':
                  data = constants.AVIAN
         
            elif bio_class == 'Family':
               data['Family'] = bio_name                         
               
         # In the event that the wikipedia page is not labelled with Dinosauria
         if bio_class == 'Class':
            bio_name = re.match(r'([^A-Za-z][A-Z][a-z]*)|([A-Z][a-z]*)', biota_data.pop(0).text.strip())[0]
            
            if bio_name == 'Aves':
               data = constants.AVIAN       
      
      except:
         pass
      
   return data
