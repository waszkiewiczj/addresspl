import pandas as pd
from typing import List

class AddressDataProvider:
    def __init__(self, config) -> None:
        self._config = config
        self._create_streets_data()
        self._create_cities_data()
        self._create_pna_data()

    def get_cities_data(self) -> List[str]:
        return self._cities_data
    
    def get_streets_data(self) -> pd.DataFrame:
        return self._streets_data

    def get_pna_data(self) -> pd.DataFrame:
        return self._pna_data

    def _create_pna_data(self):
        self._pna_data = pd.read_csv(self._config['pna_path'], encoding='UTF-8')[["PNA", "MIEJSCOWOŚĆ", "ULICA"]]

    def _create_cities_data(self):
        cities_df = pd.read_csv(self._config['cities_path'], encoding='UTF-8')
        self._cities_data = cities_df['MIASTO'].tolist()

    def _create_streets_data(self):
        csv_reader_kwargs = dict(delimiter=";")
        simc_df = pd.read_csv(self._config['simc_path'], **csv_reader_kwargs)
        ulic_df = pd.read_csv(self._config['ulic_path'], **csv_reader_kwargs)

        merged_df = ulic_df.merge(simc_df, left_on='SYM', right_on='SYM')
        merged_df = merged_df[["NAZWA", "CECHA", "NAZWA_1", "NAZWA_2", "WOJ_x","POW_x","GMI_x","RODZ_GMI_x"]]
        merged_df = merged_df.fillna("")
        merged_df["ULICA"] = merged_df["NAZWA_2"].map(str) + " " + merged_df["NAZWA_1"].map(str)
        self._streets_data = merged_df
