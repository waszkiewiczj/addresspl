from src.parsing.postal_code_validator import PostalCodeValidator
from src.parsing.models import Address, City, Street

from fuzzywuzzy import fuzz


class AddressBuilder:
    def __init__(self, postal_code_validator: PostalCodeValidator) -> None:
        self._postal_code_validator = postal_code_validator

    def build_address(self, raw_address: str, city: City, street: Street, postal_code: str, building_number: str) -> Address:
        address = Address(postal_code, street, building_number, city)
        pc = postal_code
        building = building_number
        pred_address = f'{street.name} {building} {pc} {city}'
        validated_address = self._postal_code_validator.validate(address)

        fuzzy_score = fuzz.token_set_ratio(raw_address, pred_address)/100
        postal_score = 1 if validated_address else 0
        if address.postal_code == '':
            postal_score = city.score

        pred = f'{address.street} {address.building_number} {address.postal_code} {address.city.name}'
        raw_letters =  [char for char in raw_address]
        for char in pred:
            if char in raw_letters:
                raw_letters.remove(char)
                if len(raw_letters) == 0:
                    break

        letter_score = (1 - len(raw_letters)/len(raw_address))
        score =  (fuzzy_score *1 + postal_score * 1 + street.score * 7 + city.score * 3 + letter_score * 1 ) / 13
        address.score = round(score, 4)

        return validated_address

    def _score_prediction():
        pass
