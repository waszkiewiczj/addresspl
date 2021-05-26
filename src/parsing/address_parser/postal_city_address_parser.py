import pandas as pd
from typing import List
from fuzzywuzzy import fuzz


from .address_parser import AddressParser
from ..models.address import Address
from ..models.city import City
from ..models.street import Street
from ..address_data_provider import AddressDataProvider
from ..address_builder import AddressBuilder
from .address_parser_utils import get_postal_code, get_building_number, get_streets_from_streets_data, get_postal_code_matching_data


class PostalCityAddressParser(AddressParser):
    def __init__(self, address_data_provider: AddressDataProvider, address_builder: AddressBuilder) -> None:
        self._address_data_provider = address_data_provider
        self._address_builder = address_builder


    def parse_address(self, raw_address: str) -> List[Address]:
        postal_code = get_postal_code(raw_address)
        if postal_code is None:
            return []

        ad_without_postal_code = raw_address.replace(postal_code, "")
        building = get_building_number(ad_without_postal_code)
        
        pna_data = self._address_data_provider.get_pna_data()
        matching_cities = get_postal_code_matching_data(pna_data, postal_code)

        records = []
        for (i, city_data) in matching_cities.iterrows():
            city_name = city_data['MIEJSCOWOŚĆ']
            city_score = 1 if city_name in raw_address else fuzz.token_set_ratio(raw_address, city_name) / 100
            city = City(city_name, city_score)
            streets = get_streets_from_streets_data(ad_without_postal_code, city, self._address_data_provider, True)

            for street in streets:
                address = self._address_builder.build_address(raw_address, city, street, postal_code, building)
                records.append(address)
        return records

    def _get_matching_cities(self, pna_data: pd.DataFrame, postal_code: str) -> pd.DataFrame:
        return pna_data[(pna_data['PNA'] == postal_code)]
