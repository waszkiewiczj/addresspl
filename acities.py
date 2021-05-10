from typing import List
from models import City
from fuzzywuzzy import fuzz

def get_cities(address: str, cities: List[str])-> List[City]:
    N_MAX = 5
    result = []

    for city in cities:
        score = 1 if city in address else fuzz.token_set_ratio(address, city) 
        result.append(City(name=city, score=score))
    result_by_len = sorted(result, lambda city: len(city.name))
    result_sorted = sorted(result_by_len, lambda city: city.score)
    return result_sorted[:N_MAX]
