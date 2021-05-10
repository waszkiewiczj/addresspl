from models import Address
from fuzzywuzzy import fuzz

def to_records(address, city, streets, postal_code, building_number):
    records = []
    for street_obj in streets:
        street = street_obj.name
        a = Address(postal_code, street, building_number, city, 0, [])
        pred_address = f'{street} {building_number} {postal_code} {city}'
        score = fuzz.token_set_ratio(address, pred_address)
        a.score = score
        records.append(a)

    return records