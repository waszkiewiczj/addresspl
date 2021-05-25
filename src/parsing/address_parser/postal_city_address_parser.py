import pandas as pd
from typing import List
from fuzzywuzzy import fuzz


from .address_parser import AddressParser
from ..models.address import Address
from ..models.city import City
from ..models.street import Street
from ..address_data_provider import AddressDataProvider
from ..address_builder import AddressBuilder
from ..get_postal_code import get_postal_code
from ..get_building_number import get_building_number


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
        matching_cities = self._get_matching_cities(pna_data, postal_code)

        records = []
        for (i, city_data) in matching_cities.iterrows():
            city_name = city_data['MIEJSCOWOŚĆ']
            city_score = 1 if city_name in raw_address else fuzz.token_set_ratio(raw_address, city_name) / 100
            city = City(city_name, city_score)

            citystreets = self._get_city_streets(city.name)
            if len(citystreets) == 0:
                citystreets = [city_name]
                ad_without_city = ad_without_postal_code
            else:
                ad_without_city = ad_without_postal_code.replace(city.name,"")
            streets = self._get_streets(ad_without_city, citystreets)

            for street in streets:
                address = self._address_builder.build_address(raw_address, city, street, postal_code, building)
                records.append(address)
        return records

    def _get_city_streets(self, city: str) -> pd.DataFrame:
        streets_data = self._address_data_provider.get_streets_data()
        if "Warszawa" in city:
            return streets_data[(streets_data['RODZ_GMI_x']==8) | (streets_data['NAZWA']==city)]['ULICA']
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

    def _get_streets(self, address:str, streets, n:int=5) -> Street:
        scores = self._get_scores(address, streets)

        sorted_scores = self._sort_scores(scores)
        return sorted_scores[:n]

    @staticmethod
    def _get_scores(address, streets):
        scores = []

        for street in streets:
            street = street.strip()
            if street in address:
                scores.append(Street(name=street, score=1))
                continue

            r = fuzz.token_set_ratio(address, street) / 100
            scores.append(Street(name=street, score=r))
        return scores

    @staticmethod
    def _sort_scores(scores):
        sortedLen = sorted(scores, key=lambda score: len(score.name), reverse=True)
        sortedR = sorted(sortedLen, key=lambda score: score.score, reverse=True)

        return sortedR

    def _get_matching_cities(self, pna_data: pd.DataFrame, postal_code: str) -> pd.DataFrame:
        return pna_data[(pna_data['PNA'] == postal_code)]
