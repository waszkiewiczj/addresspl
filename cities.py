#%%
import pandas as pd

simc_csv='data\\SIMC_Urzedowy_2021-04-06.csv'

csv_reader_kwargs = dict(delimiter=";")
simc_df = pd.read_csv(simc_csv,encoding='UTF-8', **csv_reader_kwargs)


# %%
