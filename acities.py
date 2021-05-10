from typing import List
from models import City
from fuzzywuzzy import fuzz

def get_cities(address: str, cities: List[str])-> List[City]:
    N_MAX = 5
    result = []

    for city in cities:
        score = 1 if city in address else fuzz.token_set_ratio(address, city) / 100
        result.append(City(name=city, score=score))
    result_by_len = sorted(result, key=lambda city: len(city.name),reverse=True)
    result_sorted = sorted(result_by_len, key=lambda city: city.score,reverse=True)
    return result_sorted[:N_MAX]
