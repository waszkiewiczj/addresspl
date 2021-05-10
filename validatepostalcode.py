import pandas as pd

from typing import List
from models import Address

INVALID_POSTAL_ERROR = "postal code and city do not match"


class PostalCodeValidator:
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


def validate_postal_code(records: List[Address]) -> List[Address]:
    validator = PostalCodeValidator()

    validated = map(lambda address: _validate_single_postal_code(address, validator), records)

    return list(validated)


def _validate_single_postal_code(address: Address, validator: PostalCodeValidator) -> Address:
    if validator.is_valid(address):
        address.errors += [INVALID_POSTAL_ERROR]

    return address
