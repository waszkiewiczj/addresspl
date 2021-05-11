#%%
from fuzzywuzzy import fuzz, process

import pandas as pd
import re
import time
from joblib import Parallel, delayed

from acities import get_cities
from astreets import get_streets
from atorecords import to_records
from validatepostalcode import PostalCodeValidator

from typing import List
from models import Address


# %%

df_test = pd.read_csv('data/adresy_dla_studentow.csv', encoding='UTF-8', header=None,  names=['Address'], delimiter=";")
adresy_dla_studentow = df_test['Address'].tolist()

cities_df = pd.read_csv('data/cities.csv', encoding='UTF-8')
cities_list = cities_df['MIASTO'].tolist()

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

def address_parser(ad:str)->List[Address]:
    postal_code = get_postal_code(ad)
    building = get_building(ad)

    cities = get_cities(ad, cities_list)
    records = []
    for c in cities:
        citystreets = merged_df[(merged_df['NAZWA']==c.name)]['ULICA']
        streets = get_streets(ad, citystreets)
        city_records = to_records(ad, c.name, streets, postal_code, building)
        records.extend(city_records)

    validator = PostalCodeValidator()
    records = validator.validate(records)
    print("#####")
    print(ad)
    for i, r in enumerate(records):
        if i < 3:
            err_msg = ''
            if len(r.errors)>0:
                err_msg = r.errors[0]
            
            print(f"score: {r.score} - {r.street} {r.building_number} {r.postal_code} {r.city}. errors: {err_msg}")
        else:
            break
    print("")
    return records

startTime = time.perf_counter()

for i in adresy_dla_studentow:
    address_parser(i)

# results = Parallel(n_jobs=2)(delayed(address_parser)(i) for i in adresy_dla_studentow)

print(time.perf_counter() - startTime)

# %%

