#%%

from fuzzywuzzy import fuzz, process

import pandas as pd
import re
import time
from joblib import Parallel, delayed

# %%

df_test = pd.read_csv('data/adresy_dla_studentow.csv', encoding='UTF-8', header=None,  names=['Address'], delimiter=";")
adresy_dla_studentow = df_test['Address'].tolist()

cities_df = pd.read_csv('data/cities.csv', encoding='UTF-8')
cities = cities_df['MIASTO'].tolist()

df = pd.read_csv('data/db2.csv', encoding='UTF-8',header=None,  names=['Address'])
db_ads = df['Address'].tolist()

csv_reader_kwargs = dict(delimiter=";")
simc_df = pd.read_csv('data/SIMC_Urzedowy_2021-04-06.csv', **csv_reader_kwargs)
ulic_df = pd.read_csv('data/ULIC_Adresowy_2021-04-06.csv', **csv_reader_kwargs)

merged_df = ulic_df.merge(simc_df, left_on='SYM', right_on='SYM')
merged_df = merged_df[["NAZWA", "CECHA", "NAZWA_1", "NAZWA_2"]]
merged_df = merged_df.fillna("")
merged_df["ULICA"] = merged_df["NAZWA_2"].map(str) + " " + merged_df["NAZWA_1"].map(str)

def get_postal_code(inputStr):
    postalCodeRegex = r"\d{2}-?\d{3}"
    postalCode = "Not found"
    match = re.search(postalCodeRegex, inputStr)
    if match is not None:
        postalCode = match.group()

    return postalCode

def get_building(inputStr):
    buildingRegex = r"\d+\w{0,3}\/{0,1}\d*\w{0,3}"
    building = "Not found"
    match = re.search(buildingRegex, inputStr)
    if match is not None:
        building = match.group()

    return building

def best_city(address, cities):
    best_r = -1
    best_c = ''
    l = len(cities)
    for i, city in enumerate(cities):
        r = fuzz.token_set_ratio(address, city) 
        if r > best_r :
            best_r = r
            best_c = city
        if r == 1 and len(best_c) < len(city):
            best_r = r
            best_c = city
    return best_c, best_r

def best_city(address, cities):
    best_r = -1
    best_c = ''
    best_inx = -1
    for city in cities:
        if city in address:
            best_r = 1
            inx = address.index(city)
            if inx > best_inx:
                best_c = city
                best_inx = inx
            if inx == best_inx and len(best_c) < len(city):
                best_c = city
                best_inx = inx
            
    if best_r == 1:
        return best_c, best_r

    for city in cities:
        r = fuzz.token_set_ratio(address, city) 
        if r > best_r :
            best_r = r
            best_c = city
        if r == 1 and len(best_c) < len(city):
            best_r = r
            best_c = city
    return best_c, best_r


def address_parser(ad):
    city, ratio  = best_city(ad, cities)
    citystreets = merged_df[(merged_df['NAZWA']==city)]['ULICA']
    street, ratio = best_city(ad, citystreets)
    postal_code = get_postal_code(ad)
    a = ad.replace(city, "")
    a = a.replace(postal_code, "")
    building = get_building(a)
    print("")
    print(f"### {ad} ###")
    print(f'miasto: {city}')
    print(f'budynek: {building}')
    print(f'ulica: {street}')
    print(f'kod pocztowy: {postal_code}')

startTime = time.perf_counter()
results = Parallel(n_jobs=2)(delayed(address_parser)(i) for i in adresy_dla_studentow)

print(time.perf_counter() - startTime)

# %%

