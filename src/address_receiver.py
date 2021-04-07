import pandas as pd

from src.input_cleaner import InputCleaner
from src.c2v_parser import Chars2VecParser
from annoy import AnnoyIndex
from typing import Dict


class AddressReceiver:
    def __init__(self, annoy_tree: AnnoyIndex, addresses_df: pd.DataFrame, cleaner: InputCleaner,
                 c2v_parser: Chars2VecParser):
        self.addresses = addresses_df
        self.annoyTree = annoy_tree
        self.cleaner = cleaner
        self.c2v_parser = c2v_parser

    def get_pretty_address(self, input_str: str) -> Dict[str, str]:
        cleaned = self.cleaner.clean_input(input_str)

        best_address = self.get_best_address(cleaned)

        return best_address

    def get_best_address(self, input_str: str) -> Dict[str, str]:
        vector = self.c2v_parser.parse_single(input_str)
        ind = self.annoyTree.get_nns_by_vector(vector, 1)

        best_address_record = self.addresses.loc[ind, ["NAZWA", "CECHA", "NAZWA_1", "NAZWA_2"]]

        best_address_dict = best_address_record.to_dict(orient="records")[0]

        return best_address_dict
