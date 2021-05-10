import pandas as pd

from typing import List
from models import Address



class PostalCodeValidator:
    INVALID_POSTAL_ERROR = "postal code and city do not match"

    def __init__(
            self,
            postal_code_csv: str = "data/kody.csv",
            city_column_name: str = "MIEJSCOWOŚĆ",
            postal_code_column_name: str = "KOD POCZTOWY",
    ):
        self.city_column_name = city_column_name
        self.postal_code_column_name = postal_code_column_name
        self.postal_code_df = pd.read_csv(postal_code_csv, sep=";").loc[:, [city_column_name, postal_code_column_name]]

    def is_valid(self, address: Address) -> bool:
        bool_df = (self.postal_code_df[self.city_column_name].str.lower() == address.city.lower()) & (
                self.postal_code_df[self.postal_code_column_name] == address.postal_code)
        filtered_df = self.postal_code_df[bool_df]

        return len(filtered_df) > 0

    def mark_invalid(self, address: Address) -> Address:
        address.errors += [self.INVALID_POSTAL_ERROR]

        return address

    def validate(self, addresses: List[Address]):
        validated = map(lambda address: address if self.is_valid(address) else self.mark_invalid(address), addresses)

        return list(validated)
