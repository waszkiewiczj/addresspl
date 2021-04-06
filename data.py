# %%
import pandas as pd
import numpy as np
import re

#%%
simc = pd.read_csv("data/SIMC_Urzedowy_2021-04-06.csv", delimiter=";")
ulic = pd.read_csv("data/ULIC_Adresowy_2021-04-06.csv", delimiter=";")

df_outer = ulic.merge(simc, left_on='SYM', right_on='SYM')
df_outer = df_outer[["NAZWA", "CECHA","NAZWA_1","NAZWA_2"]]
df_outer = df_outer.replace(np.nan, '', regex=True)

# %%
def removePolishLetters(text):
    lettersDict = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ś":"s", "ź": "z", "ż": "z","ó":"o"}
    for plLetter, engLetter in lettersDict.items():
        text = text.replace(plLetter, engLetter)
    return text

def clean(text):
    text = text.lower()
    text = re.sub(r'\s+|\.', "", text)
    text = removePolishLetters(text)
    return text

combs = [] 
for index, row in df_outer.iterrows():
    ul_miasto = row['NAZWA_2'] + row['CECHA'].replace(",", "") + row['NAZWA_1'] + row['NAZWA']
    ul_miasto = clean(ul_miasto)

    obj = {
        "STRING": ul_miasto,
        "NAZWA": row['NAZWA'],
        "CECHA": row['CECHA'],
        "NAZWA_1": row['NAZWA_1'],
        "NAZWA_2": row['NAZWA_2']
    }

    combs.append(obj)

    miasto_ul = row['NAZWA'] + row['NAZWA_2'] + row['CECHA'].replace(",", "") + row['NAZWA_1']
    miasto_ul = clean(miasto_ul)

    obj = {
        "STRING":miasto_ul,
        "NAZWA": row['NAZWA'],
        "CECHA": row['CECHA'],
        "NAZWA_1": row['NAZWA_1'],
        "NAZWA_2": row['NAZWA_2']
    }
    combs.append(obj)
    if index % 1000 ==0:
        print(f"{index}/{df_outer.shape[0]}, perc: {index/df_outer.shape[0]} ")

combo_df = pd.DataFrame(combs)
combo_df.head()
# %%
combo_df.to_csv('data\\db.csv', index=False)
# %%
