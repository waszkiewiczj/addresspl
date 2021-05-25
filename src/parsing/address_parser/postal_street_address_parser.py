import pandas as pd
from typing import List
from fuzzywuzzy import fuzz


from .address_parser import AddressParser
from ..models.address import Address
from ..models.city import City
from ..address_data_provider import AddressDataProvider
from ..address_builder import AddressBuilder
from ..get_postal_code import get_postal_code
from ..get_building_number import get_building_number


class PostalStreetAddressParser(AddressParser):
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
        matching_streets = self._get_matching_streets(pna_data, postal_code)

        records = []
        for (i, street_data) in matching_streets.iterrows():
            street = street_data['ULICA']
            city_name = street_data['MIEJSCOWOŚĆ']
            city_score = 1 if street in raw_address else fuzz.token_set_ratio(raw_address, city_name) / 100
            city = City(city_name, city_score)
            address = self._address_builder.build_address(raw_address, city, street, postal_code, building)
            records.append(address)
        return records


    def _get_matching_streets(self, pna_data: pd.DataFrame, postal_code: str) -> pd.DataFrame:
        matching_streets = pna_data[(pna_data['PNA'] == postal_code)]
        matching_streets_copy = matching_streets.copy(deep=True)
        matching_streets_copy['ULICA'] = matching_streets.apply(lambda x: x['ULICA'] if type(x['ULICA']) != float else x['MIEJSCOWOŚĆ'], axis = 1)
        return matching_streets_copy
