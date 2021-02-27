import csv
import numpy as np
from pprint import pprint as pp
import matplotlib.pyplot as plt

#(1) this function counts the total population of a neighborhood or district
def count_total_population_area(areas, dict_key, data):
  population_stats=[]
  for area in areas:
    total_population=0
    for row in data:
      if row[dict_key]==area:
        total_population+=int(row['Nombre'])
    population_stats.append({'Name': area, 'Population':total_population})
  population_stats.sort(key=lambda x: x.get('Population'),reverse=True)
  return population_stats


#(2) Diversity as variety
#this function counts the number of nationalities of an area (district or neighbourhood) and lists them in a dictionary.
def count_nationalities(areas, dict_key, data):
  nationalities_per_area=[]
  for area in areas:
    local_nationalities=[]
    for row in data:
      if row[dict_key]==area and int(row['Nombre'])>0:
          local_nationalities.append(row['Nacionalitat'])
    local_set_nationalities=set(local_nationalities)
    nationalities_per_area.append({'Name': area, 'Number_of_nationalities': len(local_set_nationalities)})
  nationalities_per_area.sort(key=lambda x: x.get('Number_of_nationalities'),reverse=True)
  return nationalities_per_area


#(3) Simpson Method (variety+balance)
#this function counts the total population for an area and then the population of a certain nationality. Based on this, it gives you the simpson index for that area. Finally, I create a sorted dictionary of simpson indices.
def simpson_index(areas, dict_key, data):
  simpson_index_area=[]
  for area in areas:
    props_nationalities={}
    sum_props=0
    total_population=0
    for row in data:
      if row[dict_key]==area:
        total_population+=int(row['Nombre'])
    for nationality in set_nationalities:
      target_population=0
      for row in data:
        if row[dict_key]==area:
          if row['Nacionalitat']==nationality:
            target_population+=int(row['Nombre'])
      sum_props+=(target_population/total_population)**2
    simpson_index=round(1-sum_props,3)
    simpson_index_area.append({'Area': area, 'Simpson index': simpson_index})
  simpson_index_area.sort(key=lambda x: x.get('Simpson index'),reverse=True)
  return simpson_index_area
  


#(4) this function tells you in which neighbourhood/district there are more non-Spaniards (gives you a ranking)
def count_non_spaniard(items, dict_key, data):
  non_spaniard_stats=[]
  for item in items:
    non_spaniard_count=0
    spaniard_count=0
    for row in data:
      if row[dict_key]==item:
          if row['Nacionalitat']!='Espanya':
            non_spaniard_count+=int(row['Nombre'])
          else:
            spaniard_count+=int(row['Nombre'])
    total_count=non_spaniard_count+spaniard_count
    percent_non_spaniard=(non_spaniard_count/total_count)*100
    non_spaniard_stats.append({
      'Name': item,
      'Non-Spaniard': (non_spaniard_count, round(percent_non_spaniard)),
    })
  non_spaniard_stats.sort(key=lambda x: x.get('Non-Spaniard')[1],reverse=True)
  return non_spaniard_stats



#(5) this function counts the number of women and men of a nationality and also gives you the percentage over the total populaiton (in an ordered list from higher to lower proportion of women).
#it's only interesting for the case of nationalities, since gender is very much balanced wrt neighbourhoods/districts. Only when total polation is higher than 5000.
def gender_count_nationalities(items, dict_key, data):
  gender_stats=[]
  for item in items:
    women_count=0
    men_count=0
    for row in data:
      if row[dict_key]==item:
          if row['Sexe']=='Dona':
            women_count+=int(row['Nombre'])
          else:
            men_count+=int(row['Nombre'])
    total_count=women_count+men_count
    percent_women=(women_count/total_count)*100
    percent_men=(men_count/total_count)*100
    if total_count>5000:
      gender_stats.append({
        'Name': item,
        'Women': (women_count, round(percent_women)), 
        'Men': (men_count, round(percent_men))
      })
  gender_stats.sort(key=lambda x: x.get('Women')[1],reverse=True)
  #gender_stats.sort(key=lambda x: x.get('Women')[0],reverse=True)
  return gender_stats


#(5) this function counts the number of women and men of an area (district or neighbourhood) and also gives you the percentage over the total populaiton (in an ordered list from higher to lower proportion of women).
#it's only interesting for the case of nationalities, since gender is very much balanced wrt neighbourhoods/districts. 
def gender_count_areas(items, dict_key, data):
  gender_stats=[]
  for item in items:
    women_count=0
    men_count=0
    for row in data:
      if row[dict_key]==item:
          if row['Sexe']=='Dona':
            women_count+=int(row['Nombre'])
          else:
            men_count+=int(row['Nombre'])
    total_count=women_count+men_count
    percent_women=(women_count/total_count)*100
    percent_men=(men_count/total_count)*100
    gender_stats.append({
      'Name': item,
      'Women': (women_count, round(percent_women)), 
      'Men': (men_count, round(percent_men))
    })
  gender_stats.sort(key=lambda x: x.get('Women')[1],reverse=True)
  #gender_stats.sort(key=lambda x: x.get('Women')[0],reverse=True)
  return gender_stats




#(6) this function gives you a ranking of the neighbourhoods where there is higher concentration of people from a certain nationality
def where_is_each_nationality(areas, nationality, dict_key, data):
  data_count_nationality_per_area=[]
  for area in areas:
    count_nationality=0
    for row in data:
      if row[dict_key]==area:
        if row['Nacionalitat']==nationality:
          count_nationality+=int(row['Nombre'])
    data_count_nationality_per_area.append({'Area': area, 'Number': count_nationality})
  data_count_nationality_per_area.sort(key=lambda x: x.get('Number'),reverse=True)
  return data_count_nationality_per_area
    

#(7) this function looks at the number of people (divided by gender) that do not have studies of any kind in each area
def academic_level_areas(items, dict_key, data):
  academic_level_stats=[]
  for item in items:
    women_count=0
    men_count=0
    for row in data:
      if row[dict_key]==item and row['Nivell_academic']=='Sense estudis':
        if row['Sexe']=='Dona':
          women_count+=int(row['Nombre'])
        else:
          men_count+=int(row['Nombre'])
    if items==set_districts:
      for entry in population_districts:
        if entry['Name']==item:
          academic_level_stats.append({
            'Name': item,
            'Women': women_count, 
            'Men': men_count,
            'Total':round((women_count+men_count)/entry['Population'], 3)
          })
    else:
      for entry in population_neighborhoods:
        if entry['Name']==item:
          academic_level_stats.append({
            'Name': item,
            'Women': women_count, 
            'Men': men_count,
            'Total':round((women_count+men_count)/entry['Population'], 3)
          })

  academic_level_stats.sort(key=lambda x: x.get('Name'),reverse=True)
  return academic_level_stats



#(8) this function gives you a ranking of neighborhood by percentage of unemployment
def unemployment_neighborhood(dict_key, data):
  unemployment_stats=[]
  for neighborhood in set_neighborhoods:
    unemployment_in_area=0
    for row in data:
      if row[dict_key]==neighborhood and row['Mes']=='1':
        unemployment_in_area=float(row['Pes_atur'])
    unemployment_stats.append({'Name': neighborhood, 'Unemployment': unemployment_in_area})
  unemployment_stats.sort(key=lambda x: x.get('Name'),reverse=True)
  return unemployment_stats
        

#(9) this function gives you a ranking of districts by percentage of unemployment
def unemployment_district(dict_key, data):
  unemployment_stats=[]
  for district in set_districts:
    unemployment_in_area=0
    unemployment_per_neighborhood=[]
    population_per_neighborhood=[]
    for row in data:
      if row[dict_key]==district and row['Mes']=='1':
        unemployment_per_neighborhood.append(float(row['Pes_atur']))
        population_per_neighborhood.append(float(row['Població_16_64_anys']))
    unemployment_in_area=round(np.average(unemployment_per_neighborhood, weights=population_per_neighborhood),3)
    unemployment_stats.append({'Name': district, 'Unemployment': unemployment_in_area})
  unemployment_stats.sort(key=lambda x: x.get('Name'),reverse=True)
  return unemployment_stats


#(10) this funcioin gives you a ranking of the amount of uses of computers and wifi of people from a neighborhood, in absolute numbers and relative to total population of area
def biblios_tic_barris(dict_key, data):
  usos_tic_stats=[]
  for neighborhood in set_neighborhoods:
    usos_tic_area=0
    for row in data:
      if row[dict_key]==neighborhood and row['Indicador']=='Usos_Ordinadors_i_Wifis':
        usos_tic_area=float(row['Valor'])
    for item in population_neighborhoods:
      if item['Name']==neighborhood:
        total_population_neighborhood=item['Population']
    usos_tic_stats.append({'Name': neighborhood, 'Usos ordinadors i wifi': [usos_tic_area, round(usos_tic_area/total_population_neighborhood,2)]})
  usos_tic_stats.sort(key=lambda x: x.get('Name'),reverse=True)
  return usos_tic_stats


#(11) this function gives you a ranking of the amount of uses of computers and wifi of people from a district, in absolute numbers and relative to total population of area
def biblios_tic_districtes(dict_key, data):
  usos_tic_stats=[]
  for district in set_districts:
    usos_tic_area=0
    for row in data:
      if row[dict_key]==district and row['Indicador']=='Usos_Ordinadors_i_Wifis':
        usos_tic_area+=float(row['Valor'])
    for item in population_districts:
      if item['Name']==district:
        total_population_district=item['Population']
    usos_tic_stats.append({'Name': district, 'Usos ordinadors i wifi': [usos_tic_area, round(usos_tic_area/total_population_district,2)]})
  usos_tic_stats.sort(key=lambda x: x.get('Name'),reverse=True)
  return usos_tic_stats



#(12) this fucntion gives you a translation between nnumbers and the qualitative answers to the survey on bretxa digital
def translate_metainfo(data):
  translate_districts=[]
  translate_neighborhoods=[]
  for row in data:
    if row['Nom_variable']=='Barri':
      #translate_neighborhoods.append({row['Text_resposta']:row['Codi_resposta']})
      translate_neighborhoods.append({'Codi':row['Codi_resposta'], 'Barri':row['Text_resposta']})
    elif row['Nom_variable']=='Districte':
      #translate_districts.append({row['Text_resposta']:row['Codi_resposta']})
      translate_districts.append({'Codi':row['Codi_resposta'], 'Districte':row['Text_resposta']})
  return translate_districts, translate_neighborhoods

#(13) this function gives you the amount of people per neighborhood that said they don't have internet at home + the percentage relative to the amount of people surveyed
def bretxa_digital_neighborhoods(data, llegenda):
  no_internet_stats=[]
  for item in llegenda:
    no_internet_at_home_count=0
    total_count=0
    for row in data:
      if row['Barri']==item['Codi']:
        total_count+=1
        if row['P1']=='2':
          no_internet_at_home_count+=1
    if total_count!=0:
      percent=no_internet_at_home_count/total_count
    else:
      percent=0
    no_internet_stats.append({'Neighborhood':item['Barri'], 'No internet': [no_internet_at_home_count, round(percent,2)]})
  no_internet_stats.sort(key=lambda x: x.get('Neighborhood'),reverse=True)
  return no_internet_stats


#this function gives you the amount of people per district that said they don't have internet at home + the percentage relative to the amount of people surveyed
def bretxa_digital_districts(data, llegenda):
  no_internet_stats=[]
  for item in llegenda:
    no_internet_at_home_count=0
    total_count=0
    for row in data:
      if row['Districte']==item['Codi']:
        total_count+=1
        if row['P1']=='2':
          no_internet_at_home_count+=1
    if total_count!=0:
      percent=no_internet_at_home_count/total_count
    else:
      percent=0
    no_internet_stats.append({'Districte':item['Districte'], 'No internet': [no_internet_at_home_count, round(percent,2)]})
  no_internet_stats.sort(key=lambda x: x.get('Districte'),reverse=True)
  return no_internet_stats
  

# Plotters

def plot_diversity_variety(data):
  area_names = tuple(
    row['Name']
    for row in data
  )
  y_pos = list(
    range(
      len(area_names)
    )
  )
  nationality_nums = [
    row['Number_of_nationalities']
    for row in data
  ]


  plt.bar(y_pos, nationality_nums, align='center')
  plt.xticks(y_pos, area_names, rotation='vertical', fontsize=8)
  plt.ylabel('Number of nationalities')
  plt.title('Diversity as variety')
  plt.tight_layout()
  plt.show()



def plot_diversity_simpson(data):
  area_names = tuple(
    row['Area']
    for row in data
  )
  y_pos = list(
    range(
      len(area_names)
    )
  )
  simpson_index = [
    row['Simpson index']
    for row in data
  ]

  plt.bar(y_pos, simpson_index, align='center')
  plt.xticks(y_pos, area_names, rotation='vertical', fontsize=8)
  plt.ylabel('Simpson index')
  plt.title('Diversity as variety+balance (Simpson index)')
  plt.tight_layout()
  plt.show()




def plot_non_spaniards(data):
  area_names = tuple(
    row['Name']
    for row in data
  )
  y_pos = list(
    range(
      len(area_names)
    )
  )
  non_spaniard_percent= [
    row['Non-Spaniard'][1]
    for row in data
  ]

  plt.bar(y_pos, non_spaniard_percent, align='center')
  plt.xticks(y_pos, area_names, rotation='vertical', fontsize=8)
  plt.ylabel('Percentage of non-Spaniards')
  plt.title('Proportion of non-Spanish population')
  plt.tight_layout()
  plt.show()
  # plt.savefig('percentage_non_spaniards_neighborhoods.pdf')


def plot_gender_per_nationality(data):
  nationalities = tuple(
    row['Name']
    for row in data
  )
  y_pos = list(
    range(
      len(nationalities)
    )
  )
  women_percent= [
    row['Women'][1]
    for row in data
  ]
  plt.bar(y_pos, women_percent, align='center')
  plt.xticks(y_pos, nationalities, rotation='vertical', fontsize=8)
  plt.ylabel('Percentage of women')
  plt.title('Proportion of women per nationality (only for nationalities with >5000)')
  plt.tight_layout()
  plt.show()



def plot_gender_per_barri(data):
  areas = tuple(
    row['Name']
    for row in data
  )
  y_pos = list(
    range(
      len(areas)
    )
  )
  women_percent= [
    row['Women'][1]
    for row in data
  ]
  plt.bar(y_pos, women_percent, align='center')
  plt.xticks(y_pos, areas, rotation='vertical', fontsize=8)
  plt.ylabel('Percentage of women')
  plt.title('Proportion of women per neighborhood')
  plt.tight_layout()
  plt.show()

def plot_gender_per_districte(data):
  areas = tuple(
    row['Name']
    for row in data
  )
  y_pos = list(
    range(
      len(areas)
    )
  )
  women_percent= [
    row['Women'][1]
    for row in data
  ]
  plt.bar(y_pos, women_percent, align='center')
  plt.xticks(y_pos, areas, rotation='vertical', fontsize=8)
  plt.ylabel('Percentage of women')
  plt.title('Proportion of women per district')
  plt.tight_layout()
  plt.show()




def plot_bretxa_libraries_use(data1, data2):
  level_bretxa=[
    row['No internet'][1]
    for row in data1
  ]
  level_use_libraries=[
    row['Usos ordinadors i wifi'][1]
    for row in data2
  ]
  labels=[
    row['Name']
    for row in data2
  ]
  plt.scatter(level_bretxa, level_use_libraries)

  for i, text in enumerate (labels):
    plt.annotate(text, (level_bretxa[i], level_use_libraries[i]), fontsize=8)

  x=np.array(level_bretxa)
  y=np.array(level_use_libraries)
  m, b = np.polyfit(x, y, 1)
  plt.plot(x, m*x+b)

  plt.title('Correlation between lack of internet at home and use of public libraries\' wifi/computers', fontsize=8)
  plt.ylabel('Use wifi/computers in public libraries per person', fontsize=8)
  plt.xlabel('Percentage people who do not have internet at home', fontsize=8)
  plt.tight_layout()
  plt.show()


def plot_atur_nivell_estudis(data1, data2):
  level_atur=[
    row['Unemployment']
    for row in data1
  ]
  level_studies=[
    row['Total']
    for row in data2
  ]
  labels=[
    row['Name']
    for row in data2
  ]
  plt.scatter(level_atur, level_studies)

  for i, text in enumerate (labels):
    plt.annotate(text, (level_atur[i], level_studies[i]), fontsize=8)

  x=np.array(level_atur)
  y=np.array(level_studies)
  m, b = np.polyfit(x, y, 1)
  plt.plot(x, m*x+b)

  plt.title('Correlation studies level and unemployment', fontsize=8)
  plt.ylabel('Percentage of people without studies', fontsize=8)
  plt.xlabel('Percentage of unemployed people', fontsize=8)
  plt.tight_layout()
  plt.show()




csv_nationalities=open('2018_ine_nacionalitat_per_sexe.csv', newline='')
reader_nationalities = csv.DictReader(csv_nationalities)
rows_nationalities = list(reader_nationalities)

list_districts=[row['Nom_Districte'] for row in rows_nationalities]
set_districts=list(set(list_districts))
#this is the list of unique districts

list_neighborhoods=[row['Nom_Barri'] for row in rows_nationalities]
set_neighborhoods=list(set(list_neighborhoods))
#this is the list of unique neighborhoods

list_nationalities=[row['Nacionalitat'] for row in rows_nationalities]
set_nationalities=list(set(list_nationalities))
#this is the list of unique nationalities

population_districts=count_total_population_area(set_districts, 'Nom_Districte', rows_nationalities)
# print(population_districts)
population_neighborhoods=count_total_population_area(set_neighborhoods, 'Nom_Barri', rows_nationalities)
# print(population_neighborhoods)


# nationalities_count = count_nationalities(set_districts, 'Nom_Districte', rows_nationalities)
# plot_diversity_variety(nationalities_count)


#print(gender_count_areas(set_districts, 'Nom_Districte', rows_nationalities))
#print(gender_count_areas(set_neighborhoods, 'Nom_Barri', rows_nationalities))
#print(gender_count_nationalities(set_nationalities, 'Nacionalitat', rows_nationalities))

# gender_per_nationality_data=gender_count_naitonalitie(set_nationalities, 'Nacionalitat', rows_nationalities)
# plot_gender_per_nationality(gender_per_nationality_data)

# gender_per_barri_data=gender_count_areas(set_neighborhoods, 'Nom_Barri', rows_nationalities)
# plot_gender_per_barri(gender_per_barri_data)

# gender_per_districte_data=gender_count_areas(set_districts, 'Nom_Districte', rows_nationalities)
# plot_gender_per_districte(gender_per_districte_data)




# print(count_non_spaniard(set_districts, 'Nom_Districte', rows_nationalities))
# print(count_non_spaniard(set_neighborhoods, 'Nom_Barri', rows_nationalities))
# # non_spaniards_data_districts=count_non_spaniard(set_districts, 'Nom_Districte', rows_nationalities)
# non_spaniards_data_neighborhoods=count_non_spaniard(set_neighborhoods, 'Nom_Barri', rows_nationalities)
# # plot_non_spaniards(non_spaniards_data_districts)
# plot_non_spaniards(non_spaniards_data_neighborhoods)
 

#print(simpson_index(set_districts, 'Nom_Districte', rows_nationalities))
#print(simpson_index(set_neighborhoods, 'Nom_Barri', rows_nationalities))
#simpson_index_data=simpson_index(set_districts, 'Nom_Districte', rows_nationalities)
# simpson_index_data=simpson_index(set_neighborhoods, 'Nom_Barri', rows_nationalities)
# plot_diversity_simpson(simpson_index_data)


# print(where_is_each_nationality(set_districts, 'Hondures', 'Nom_Districte', rows_nationalities))
# print(where_is_each_nationality(set_districts, 'Nicaragua', 'Nom_Districte', rows_nationalities))
# print(where_is_each_nationality(set_districts, 'Belarús', 'Nom_Districte', rows_nationalities))
# print(where_is_each_nationality(set_districts, 'Paraguai', 'Nom_Districte', rows_nationalities))
# print(where_is_each_nationality(set_districts, 'Rússia', 'Nom_Districte', rows_nationalities))
# print(where_is_each_nationality(set_neighborhoods, 'Hondures', 'Nom_Barri', rows_nationalities))
# print(where_is_each_nationality(set_neighborhoods, 'Nicaragua', 'Nom_Barri', rows_nationalities))
# print(where_is_each_nationality(set_neighborhoods, 'Belarús', 'Nom_Barri', rows_nationalities))
# print(where_is_each_nationality(set_neighborhoods, 'Paraguai', 'Nom_Barri', rows_nationalities))
# print(where_is_each_nationality(set_neighborhoods, 'Rússia', 'Nom_Barri', rows_nationalities))

csvfile_nivell_academic=open('2018_padro_nivell_academic.csv', newline='')
reader_nivell_academic = csv.DictReader(csvfile_nivell_academic)
rows_nivell_academic = list(reader_nivell_academic)

#print(academic_level_areas(set_districts, 'Nom_Districte', rows_nivell_academic))
print(academic_level_areas(set_neighborhoods, 'Nom_Barri', rows_nivell_academic))
academic_level_district_data=academic_level_areas(set_districts, 'Nom_Districte', rows_nivell_academic)
academic_level_neighborhood_data=academic_level_areas(set_neighborhoods, 'Nom_Barri', rows_nivell_academic)
  
csvfile_atur=open('2018_pes_atur.csv', newline='')
reader_atur = csv.DictReader(csvfile_atur)
rows_atur = list(reader_atur)

#print(unemployment_district('Nom_Districte', rows_atur))
print(unemployment_neighborhood('Nom_Barri', rows_atur))
unemployment_district_data=unemployment_district('Nom_Districte', rows_atur)
unemployment_neighborhood_data=unemployment_neighborhood('Nom_Barri', rows_atur)


csvfile_biblios=open('2018_dades_biblioteques.csv', newline='')
reader_biblios = csv.DictReader(csvfile_biblios)
rows_biblios = list(reader_biblios)

# print(biblios_tic_districtes('Nom_Districte', rows_biblios))
# print(biblios_tic_barris('Nom_Barri', rows_biblios))

csvfile_metainfo=open('metainfo.csv', newline='')
reader_metainfo = csv.DictReader(csvfile_metainfo)
rows_metainfo = list(reader_metainfo)

llegenda_districtes, llegenda_barris=translate_metainfo(rows_metainfo)
# print(llegenda_districtes)
# print(llegenda_barris)


csvfile_bretxa_digital=open('bretxa_digital.csv', newline='')
reader_bretxa_digital = csv.DictReader(csvfile_bretxa_digital)
rows_bretxa_digital = list(reader_bretxa_digital)

# print(bretxa_digital_neighborhoods(rows_bretxa_digital, llegenda_barris))
# print(bretxa_digital_districts(rows_bretxa_digital, llegenda_districtes))

# data1=bretxa_digital_neighborhoods(rows_bretxa_digital, llegenda_barris)
# data2=biblios_tic_barris('Nom_Barri', rows_biblios)
# data1=bretxa_digital_districts(rows_bretxa_digital, llegenda_districtes)
# data2=biblios_tic_districtes('Nom_Districte', rows_biblios)
# plot_bretxa_libraries_use(data1, data2)

#plot_atur_nivell_estudis(unemployment_district_data,academic_level_district_data)
plot_atur_nivell_estudis(unemployment_neighborhood_data,academic_level_neighborhood_data)