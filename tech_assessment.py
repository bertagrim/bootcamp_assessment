import csv
import numpy as np


#this function counts the total population of a neighborhood or district
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




#Diversity as variety
#this function counts the number of nationalities of an area (district or neighbourhood) and lists them in a dictionary.
def count_nationalities(areas, dict_key, data):
  nationalities_per_area={}
  for area in areas:
    local_nationalities=[]
    for row in data:
      if row[dict_key]==area and int(row['Nombre'])>0:
          local_nationalities.append(row['Nacionalitat'])
    
    local_set_nationalities=set(local_nationalities)
    nationalities_per_area[area]=[len(local_set_nationalities), local_set_nationalities]
  return nationalities_per_area


#Simpson Method (variety+balance)
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
  


#this function tells you in which neighbourhood/district there are more non-Spaniards (gives you a ranking)
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



#this function counts the number of women and men of an area (district or neighbourhood) or in a nationality and also gives you the percentage over the total populaiton (in an ordered list from higher to lower proportion of women).
#it's only interesting for the case of nationalities, since gender is very much balanced wrt neighbourhoods/districts
def gender_count(items, dict_key, data):
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



#this function gives you a ranking of the neighbourhoods where there is higher concentration of people from a certain nationality
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
    

#this function looks at the number of people (divided by gender) that do not have studies of any kind in each area
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
    academic_level_stats.append({
       'Name': item,
       'Women': women_count, 
       'Men': men_count
     })
  academic_level_stats.sort(key=lambda x: x.get('Women'),reverse=True)
  return academic_level_stats

#this function gives you a ranking of neighborhood by percentage of unemployment
def unemployment_neighborhood(dict_key, data):
  unemployment_stats=[]
  for neighborhood in set_neighborhoods:
    unemployment_in_area=0
    for row in data:
      if row[dict_key]==neighborhood and row['Mes']=='1':
        unemployment_in_area=float(row['Pes_atur'])
    unemployment_stats.append({'Name': neighborhood, 'Unemployment': unemployment_in_area})
  unemployment_stats.sort(key=lambda x: x.get('Unemployment'),reverse=True)
  return unemployment_stats
        

#this function gives you a ranking of districts by percentage of unemployment
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
  unemployment_stats.sort(key=lambda x: x.get('Unemployment'),reverse=True)
  return unemployment_stats


#this funcioin gives you a ranking of the amount of uses of computers and wifi of people from a neighborhood, in absolute numbers and relative to total population of area
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
  usos_tic_stats.sort(key=lambda x: x.get('Usos ordinadors i wifi')[1],reverse=True)
  return usos_tic_stats


#this function gives you a ranking of the amount of uses of computers and wifi of people from a district, in absolute numbers and relative to total population of area
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
  usos_tic_stats.sort(key=lambda x: x.get('Usos ordinadors i wifi')[1],reverse=True)
  return usos_tic_stats



#this fucntion gives you a translation between nnumbers and the qualitative answers to the survey on bretxa digital
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

#this function gives you the amount of people per neighborhood that said they don't have internet at home + the percentage relative to the amount of people surveyed
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
  no_internet_stats.sort(key=lambda x: x.get('No internet')[1],reverse=True)
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
  no_internet_stats.sort(key=lambda x: x.get('No internet')[1],reverse=True)
  return no_internet_stats
  
  






# def bretxa_digital_districts(data, translation_districts):
#   for item in translation_areas:
#     for item['Codi']:
#       for row in data:
#         if row['Districte']==item['Codi']:








      

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
#print(population_neighborhoods)

#print(count_nationalities(set_districts, 'Nom_Districte', rows_nationalities))
#print(count_nationalities(set_neighborhoods, 'Nom_Barri', rows_nationalities))

#print(gender_count(set_districts, 'Nom_Districte', rows_nationalities))
#print(gender_count(set_neighborhoods, 'Nom_Barri', rows_nationalities))
#print(gender_count(set_nationalities, 'Nacionalitat', rows_nationalities))

#print(count_non_spaniard(set_districts, 'Nom_Districte', rows_nationalities))
#print(count_non_spaniard(set_neighborhoods, 'Nom_Barri', rows_nationalities))

#print(simpson_index(set_districts, 'Nom_Districte', rows_nationalities))
#print(simpson_index(set_neighborhoods, 'Nom_Barri', rows_nationalities))

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
#print(academic_level_areas(set_neighborhoods, 'Nom_Barri', rows_nivell_academic))
  


csvfile_atur=open('2018_pes_atur.csv', newline='')
reader_atur = csv.DictReader(csvfile_atur)
rows_atur = list(reader_atur)

#print(unemployment_district('Nom_Districte', rows_atur))
#print(unemployment_neighborhood('Nom_Barri', rows_atur))



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