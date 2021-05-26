from typing import List
from fuzzywuzzy import fuzz

from src.parsing.address_parser.address_parser import AddressParser
from src.parsing.models import Address, City
from src.parsing.address_data_provider import AddressDataProvider
from src.parsing.address_builder import AddressBuilder
from src.parsing.address_parser.address_parser_utils import get_postal_code, get_streets_from_streets_data, get_building_number


class CityStreetAddressParser(AddressParser):
    def __init__(self, address_data_provider: AddressDataProvider, address_builder: AddressBuilder) -> None:
        self._address_data_provider = address_data_provider
        self._address_builder = address_builder

    def parse_address(self, raw_address: str) -> List[Address]:
        postal_code = get_postal_code(raw_address)
        ad_without_postal_code = raw_address.replace(postal_code, "")
        building = get_building_number(ad_without_postal_code)
        cities_data = self._address_data_provider.get_cities_data()
        cities = self._get_cities(ad_without_postal_code, cities_data)
        records = []
        for city in cities:
            streets = get_streets_from_streets_data(ad_without_postal_code, city, self._address_data_provider)
            for street in streets:
                address = self._address_builder.build_address(raw_address, city, street, postal_code, building)
                records.append(address)
        
        return records

    @staticmethod
    def _get_cities(address: str, cities: List[str])-> List[City]:
        N_MAX = 5
        result = []

        for city in cities:
            score = 1 if city in address else fuzz.token_sort_ratio(address, city) / 100
            result.append(City(name=city, score=score))
        result_by_len = sorted(result, key=lambda city: len(city.name),reverse=True)
        result_sorted = sorted(result_by_len, key=lambda city: city.score,reverse=True)
        return result_sorted[:N_MAX]
