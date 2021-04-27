"""
Clean input address data.

Usage:
    clean_data.py --simc-csv SIMC_CSV \
    --ulic-csv ULIC_CSV \
    --out-path OUT_PATH

Options:
    --simc-csv SIMC_CSV
    Path to CSV file with SIMC records
    --ulic-csv ULIC_CSV
    Path to CSV fil with ULIC records
    --out-path OUT_PATH
    Path to output CSV file
"""
import pandas as pd

from src.input_cleaner import InputCleaner


simc_csv='data\\SIMC_Urzedowy_2021-04-06.csv'
ulic_csv='data\\ULIC_Adresowy_2021-04-06.csv'
out_path='data\\db2.csv'

csv_reader_kwargs = dict(delimiter=";")
simc_df = pd.read_csv(simc_csv,encoding='UTF-8')
ulic_df = pd.read_csv(ulic_csv,encoding='UTF-8')

merged_df = ulic_df.merge(simc_df, left_on='SYM', right_on='SYM')
merged_df = merged_df[["NAZWA", "CECHA", "NAZWA_1", "NAZWA_2"]]
merged_df = merged_df.fillna("")

ads = []
for index, row in merged_df.iterrows():
    address = f'{row["CECHA"]} {row["NAZWA_1"]} {row["NAZWA_2"]} {row["NAZWA"]}'
    ads.append(address)


df = pd.DataFrame({'col':ads})
df.to_csv(out_path, index=False, header=None, encoding="utf-8")