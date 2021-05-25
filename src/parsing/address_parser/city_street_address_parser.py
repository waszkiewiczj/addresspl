import pandas as pd
from typing import List

from .address_parser import AddressParser
from ..models.address import Address
from ..models.city import City
from ..address_data_provider import AddressDataProvider
from ..address_builder import AddressBuilder
from ..get_postal_code import get_postal_code
from ..get_building_number import get_building_number
from fuzzywuzzy import fuzz


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
            citystreets = self._get_city_streets(city.name)
            ad_without_city = ad_without_postal_code.replace(city.name,"")
            streets = self._get_streets(ad_without_city, citystreets)
            for street in streets:
                address = self._address_builder.build_address(raw_address, city, street['name'], postal_code, building)
                records.append(address)
        
        return sorted(records, key=lambda r: r.score, reverse=True)[:3]

    def _get_city_streets(self, city: str) -> pd.DataFrame:
        streets_data = self._address_data_provider.get_streets_data()
        if "Warszawa" in city:
            return streets_data[(streets_data['RODZ_GMI_x']==8) | (streets_data['NAZWA']==city)]
        elif "Łódź" in city:
            return streets_data[((streets_data['WOJ_x']==10) & (streets_data['POW_x']==61) & (streets_data['RODZ_GMI_x']==9)) | (streets_data['NAZWA']==city)]['ULICA']
        elif "Kraków" in city:
            return streets_data[((streets_data['WOJ_x']==12) & (streets_data['POW_x']==61) & (streets_data['RODZ_GMI_x']==9)) | (streets_data['NAZWA']==city)]['ULICA']
        elif "Poznań" in city:
            return streets_data[((streets_data['WOJ_x']==30) & (streets_data['POW_x']==64) & (streets_data['RODZ_GMI_x']==9)) | (streets_data['NAZWA']==city)]['ULICA']
        elif "Wrocław" in city:
            return streets_data[((streets_data['WOJ_x']==2) & (streets_data['POW_x']==64) & (streets_data['RODZ_GMI_x']==9)) | (streets_data['NAZWA']==city)]['ULICA']
        else:
            return streets_data[(streets_data['NAZWA']==city)]['ULICA']

    def _get_cities(self, address: str, cities: List[str])-> List[City]:
        N_MAX = 5
        result = []

        for city in cities:
            score = 1 if city in address else fuzz.token_set_ratio(address, city) / 100
            result.append(City(name=city, score=score))
        result_by_len = sorted(result, key=lambda city: len(city.name),reverse=True)
        result_sorted = sorted(result_by_len, key=lambda city: city.score,reverse=True)
        return result_sorted[:N_MAX]

    def _get_streets(self, address:str, streets, n:int=5):
        scores = self._get_scores(address, streets)

        sorted_scores = self._sort_scores(scores)
        return sorted_scores[:n]

    def _get_scores(self, address, streets):
        scores = []

        for street in streets:
            if street in address:
                scores.append({'score': 1, 'name': street})
                continue

            r = fuzz.token_set_ratio(address, street) / 100
            scores.append({'score': r, 'name': street})
        return scores

    def _sort_scores(self, scores):
        sortedLen = sorted(scores, key=lambda score: len(score['name']), reverse=True)
        sortedR = sorted(sortedLen, key=lambda score: score['score'], reverse=True)

        return sortedR