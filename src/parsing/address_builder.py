from src.parsing.postal_code_validator import PostalCodeValidator
from src.parsing.models import Address, City

from fuzzywuzzy import fuzz


class AddressBuilder:
    def __init__(self, postal_code_validator: PostalCodeValidator) -> None:
        self._postal_code_validator = postal_code_validator

    def build_address(
            self,
            raw_address: str,
            city: City,
            street: str,
            postal_code: str,
            building_number: str
    ) -> Address:
        address = Address(postal_code, street, building_number, city)
        pc = postal_code
        building = building_number
        pred_address = f'{street} {building} {pc} {city}'
        score = fuzz.token_set_ratio(raw_address, pred_address) / 100
        address.score = score
        validated_address = self._postal_code_validator.validate(address)
        return validated_address
