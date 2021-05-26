import pandas as pd

from src.parsing.models import Address


class PostalCodeValidator:

    def __init__(
            self,
            config,
            city_column_name: str = "MIEJSCOWOŚĆ",
            postal_code_column_name: str = "KOD POCZTOWY",
    ):
        self.config = config
        self.city_column_name = city_column_name
        self.postal_code_column_name = postal_code_column_name
        postal_code_path = self.config['postal_code_path']
        self.postal_code_df = pd.read_csv(postal_code_path, sep=";").loc[:, [city_column_name, postal_code_column_name]]

    def is_valid(self, address: Address) -> bool:
        bool_df = (self.postal_code_df[self.city_column_name].str.lower() == address.city.name.lower()) & (
                self.postal_code_df[self.postal_code_column_name] == address.postal_code)
        filtered_df = self.postal_code_df[bool_df]

        return len(filtered_df) > 0

    def validate(self, address: Address) -> Address:
        address.is_postal_code_matching = self.is_valid(address)

        return address
