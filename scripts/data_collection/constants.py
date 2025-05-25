#Establishing some constants
INFORMAL = ['Krzyzanowskisaurus', 'Actiosaurus', 'Volgavis', 'Yacoraitichnus', 'Yezosaurus', 'Brasileosaurus', 'Subtiliolithus', 'Fuscinapedis', 'Himeoolithus', 'Protoavis', 'Salfitichnus', 'Nyasasaurus']
NO_PAGE = ['Crateropteryx', 'Bellulornis', 'Alethoalaornis', 'Eopengornis', 'Fortunguavis', 'Gretcheniao', 'Holbotia', 'Linyiornis', 'Microenantiornis', 'Monoenantiornis', 'Otogornis', 'Pterygornis', 'Shangyang', 'Horezmavis', 'Platanavis']
ORDERS = ['Ornithischia', 'Saurischia']
SUBORDERS = ['Neornithischia', 'Thyreophora', 'Sauropodomorpha', 'Theropoda']
INFRAORDERS = ['Ornithopoda', 'Ceratopsia', 'Pachycephalosauria', 'Stegosauria', 'Ankylosauria', 'Sauropoda', 'Titanosauria', 'Avialae', 'Non-Avian']

# Creating a dictionary to use when the dinosaur is noted to be avian
AVIAN = {'Order': ORDERS[1], 'Suborder': SUBORDERS[3], 'Infraorder': INFRAORDERS[7], 'Family': ''}

# Looking at the dataframe, we need to clean the columns relating to species lifetime --> Some dinosaurs have NaN as their entries for Early and Late Ages
PERIODS = ['Triassic', 'Jurassic', 'Cretaceous']
EPOCHS = ['Lower', 'Middle', 'Upper']


TRIASSIC_AGES = ['Induan', 'Olenekian', 'Anisian', 'Ladinian', 'Carnian', 'Norian', 'Rhaetian']
JURASSIC_AGES = ['Hettangian', 'Sinemurian', 'Pliensbachian', 'Toarcian', 'Aalenian', 'Bajocian', 'Bathonian', 'Callovian', 'Oxfordian', 'Kimmeridgian', 'Tithonian']
CRETACEOUS_AGES = ['Berriasian', 'Valanginian', 'Hauterivian', 'Barremian', 'Aptian', 'Albian', 'Cenomanian', 'Turonian', 'Coniacian', 'Santonian', 'Campanian', 'Maastrichtian']

LOW_EP = TRIASSIC_AGES[:2] + JURASSIC_AGES[:4] + CRETACEOUS_AGES[:6]
MID_EP = TRIASSIC_AGES[2:4] + JURASSIC_AGES[4:8] 
UPP_EP = TRIASSIC_AGES[4:] + JURASSIC_AGES[8:] + CRETACEOUS_AGES[6:]
