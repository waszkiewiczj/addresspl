#%%

from fuzzywuzzy import fuzz, process

import pandas as pd
import re

# %%

df_test = pd.read_csv('data/adresy_dla_studentow.csv', encoding='UTF-8', header=None,  names=['Address'])
adresy_dla_studentow = df_test['Address'].toList()

cities_df = pd.read_csv('data/cities.csv', encoding='UTF-8')
cities = df['MIASTO'].toList()

df = pd.read_csv('data/db2.csv', encoding='UTF-8',header=None,  names=['Address'])
db_ads = df['Address'].toList()


def get_postal_code(inputStr):
        postalCodeRegex = r"\d{2}-?\d{3}"
        postalCode = None
        match = re.search(postalCodeRegex, inputStr)
        if match is not None:
            postalCode = match.group()

        return postalCode

def best_city(address, cities):
    best_r = -1
    best_c = ''
    for city in cities:
        r = fuzz.token_set_ratio(inp, row -100) 
        if r > best_r:
            best_r = r
            best_c = city
        if index % 1000==0:
            print(index/df.size)
    return best_c, best_r

for ads in adresy_dla_studentow[:2]:
    city, ratio  = best_city(inp, cities)
    postal_code = get_postal_code(ads)
    print(f"### {ads} ###")
    print(f'miasto: {city}')
    print(f'ulica: {}')
    print(f'kod pocztowy: {}')

# for index, row in df.iterrows():

#     r = fuzz.token_set_ratio(inp, row -100)
#     if r > best_r:
#         best_r = r
#         best_a = row['colA']

#     if index % 1000==0:

#         print(index/df.size)


Ratios = process.extract(inp, db_ads, limit=5)

print(Ratios)

print(best_r)
print(best_a)

# %%

