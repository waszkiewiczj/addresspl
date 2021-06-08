import re
import pandas as pd
from fuzzywuzzy import fuzz
from typing import List

from pandas.core.frame import DataFrame

from ..address_data_provider import AddressDataProvider
from ..models.street import Street
from ..models.city import City

def get_postal_code(raw_address: str) -> str:
    postal_code_regex = r"\b\d{2}-?\d{3}"
    postal_code = ""
    match = re.search(postal_code_regex, raw_address)
    if match is not None:
        postal_code = match.group()

    return postal_code

def get_building_number(raw_address: str) -> str: 
    # building_regex = r"\d+\w{0,3}\/{0,1}\d*\w{0,3}"
    # building_regex = r"(\d+\w{0,3}((\/|-)?\d*(\/|-)?\d*\s?\w{0,3}(\s|$))?)"
    building_regex = r"(\d+\w{0,3}((\/|-)?\d*\s?(\/|-|l|l\.|lok|lok\.|lokal|m|m\.|mieszkania)?\s?\d*\s?\w{0,3}(\s|$))?)"
    building = ""
    match = re.findall(building_regex, raw_address)
    if len(match) > 0:
        building = match[-1][0].strip()

    return building

def get_postal_code_matching_data(pna_data: pd.DataFrame, postal_code: str) -> pd.DataFrame:
    return pna_data[(pna_data['PNA'] == postal_code)]

def get_streets_from_streets_data(raw_address: str, city: City, address_data_provider: AddressDataProvider, add_street: bool = False) -> List[Street]:
    citystreets = _get_city_streets(city.name, address_data_provider)
    ad_without_city = _get_address_without_city(raw_address, city, citystreets)
    citystreets = [city.name] if len(citystreets) == 0 and add_street else citystreets
    return _get_streets(ad_without_city, citystreets)

def _get_city_streets(city: str, address_data_provider: AddressDataProvider) -> pd.DataFrame:
    streets_data = address_data_provider.get_streets_data()
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

def _get_streets(address:str, streets, n:int=5) -> Street:
    scores = _get_scores(address, streets)

    sorted_scores = _sort_scores(scores)
    return sorted_scores[:n]

def _get_address_without_city(raw_address: str, city: City, city_streets: pd.DataFrame) -> str:
    return raw_address if len(city_streets) == 0 else raw_address.replace(city.name, "")

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

def _sort_scores(scores):
    sortedLen = sorted(scores, key=lambda score: len(score.name), reverse=True)
    sortedR = sorted(sortedLen, key=lambda score: score.score, reverse=True)

    return sortedR