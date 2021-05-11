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
merged_df = merged_df[["NAZWA", "CECHA", "NAZWA_1", "NAZWA_2", "WOJ_x","POW_x","GMI_x","RODZ_GMI_x"]]
merged_df = merged_df.fillna("")
merged_df["ULICA"] = merged_df["CECHA"].map(str) + " " + merged_df["NAZWA_2"].map(str) + " " + merged_df["NAZWA_1"].map(str)

def get_postal_code(inputStr):
    postalCodeRegex = r"\d{2}-?\d{3}"
    postalCode = "Not found"
    match = re.search(postalCodeRegex, inputStr)
    if match is not None:
        postalCode = match.group()

    return postalCode

def get_building(inputStr):
    buildingRegex = r"\s(?:\d+\w?)(?:(?:[\s\\\/-]|\s*lok.\s*)\d+)?"
    building = "Not found"
    match = re.findall(buildingRegex, inputStr)
    if len(match) > 0:
        building = match[-1]

    return building

def get_city_streets(city:str):
    if "Warszawa" in city:
        return merged_df[(merged_df['RODZ_GMI_x']==8) | (merged_df['NAZWA']==city)]['ULICA']
    elif "Łódź" in city:
        return merged_df[((merged_df['WOJ_x']==10) & (merged_df['POW_x']==61) & (merged_df['RODZ_GMI_x']==9)) | (merged_df['NAZWA']==city)]['ULICA']
    elif "Kraków" in city:
        return merged_df[((merged_df['WOJ_x']==12) & (merged_df['POW_x']==61) & (merged_df['RODZ_GMI_x']==9)) | (merged_df['NAZWA']==city)]['ULICA']
    elif "Poznań" in city:
        return merged_df[((merged_df['WOJ_x']==30) & (merged_df['POW_x']==64) & (merged_df['RODZ_GMI_x']==9)) | (merged_df['NAZWA']==city)]['ULICA']
    elif "Wrocław" in city:
        return merged_df[((merged_df['WOJ_x']==2) & (merged_df['POW_x']==64) & (merged_df['RODZ_GMI_x']==9)) | (merged_df['NAZWA']==city)]['ULICA']
    else:
        return merged_df[(merged_df['NAZWA']==city)]['ULICA']

def address_parser(ad:str) -> List[Address]:
    postal_code = get_postal_code(ad)
    ad_without_postal_code = ad.replace(postal_code, "")
    building = get_building(ad_without_postal_code)

    cities = get_cities(ad_without_postal_code, cities_list)
    records = []
    for c in cities:
        citystreets = get_city_streets(c.name)
        if len(citystreets) == 0:
            citystreets = [str(c.name)]

        ad_without_city = ad_without_postal_code.replace(c.name,"")
        streets = get_streets(ad_without_city, citystreets)
        city_records = to_records(ad, c, streets, postal_code, building)
        records.extend(city_records)

    records = sorted(records, key=lambda r: r.score, reverse=True)

    validator = PostalCodeValidator()
    records = validator.validate(records)
    print("#####")
    print(ad)
    for i, r in enumerate(records):
        if i < 3:
            err_msg = ''
            if r.is_postal_code_matching == False:
                err_msg = 'Postal code doesnt match'
            
            pc = r.postal_code
            if r.postal_code == 'Not found':
                pc = ""
            
            print(f"score: {r.score} - {r.street} {r.building_number} {pc} {r.city}. errors: {err_msg}")
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




