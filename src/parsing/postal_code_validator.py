import pandas as pd

from typing import List
from .models.address import Address



class PostalCodeValidator:
    INVALID_POSTAL_ERROR = "postal code and city do not match"

    def __init__(
            self,
            config,
            city_column_name: str = "MIEJSCOWOŚĆ",
            postal_code_column_name: str = "KOD POCZTOWY",
    ):
        self.config = config
        self.city_column_name = city_column_name
        self.postal_code_column_name = postal_code_column_name
        self.postal_code_df = pd.read_csv(self.config['postal_code_path'], sep=";").loc[:, [city_column_name, postal_code_column_name]]

    def is_valid(self, address: Address) -> bool:
        bool_df = (self.postal_code_df[self.city_column_name].str.lower() == address.city.name.lower()) & (
                self.postal_code_df[self.postal_code_column_name] == address.postal_code)
        filtered_df = self.postal_code_df[bool_df]

        return len(filtered_df) > 0

    def validate_single(self, address: Address) -> Address:
        address.is_postal_code_matching = self.is_valid(address)
        if not address.is_postal_code_matching:
            error_msg = "Postal code doesnt match" if address.postal_code else "Postal code not found"
            address.errors.append(error_msg)

        return address

    def validate(self, address: Address) -> Address:
        return self.validate_single(address)
