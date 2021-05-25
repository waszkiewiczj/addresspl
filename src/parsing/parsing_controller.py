from typing import List

from .config import config
from .address_data_provider import AddressDataProvider
from .postal_code_validator import PostalCodeValidator
from .address_builder import AddressBuilder
from .address_parser.city_street_address_parser import CityStreetAddressParser
from .models.address import Address
from .address_parser.address_parser import AddressParser



class ParsingController:
    def __init__(self) -> None:
        self._address_data_provider = AddressDataProvider(config)
        self._postal_code_validator = PostalCodeValidator(config)
        self._address_builder = AddressBuilder(self._postal_code_validator)
        self._address_parser = CityStreetAddressParser(self._address_data_provider, self._address_builder)

    def parse_address(self, raw_address: str) -> List[Address]:
        return self._address_parser.parse_address(raw_address)

