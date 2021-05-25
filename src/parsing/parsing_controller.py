from typing import List

from src.parsing.config import config
from src.parsing.address_data_provider import AddressDataProvider
from src.parsing.postal_code_validator import PostalCodeValidator
from src.parsing.address_builder import AddressBuilder
from src.parsing.address_parser import CityStreetAddressParser
from src.parsing.models import Address


class ParsingController:
    def __init__(self) -> None:
        self._address_data_provider = AddressDataProvider(config)
        self._postal_code_validator = PostalCodeValidator(config)
        self._address_builder = AddressBuilder(self._postal_code_validator)
        self._address_parser = CityStreetAddressParser(self._address_data_provider, self._address_builder)

    def parse_address(self, raw_address: str) -> List[Address]:
        return self._address_parser.parse_address(raw_address)
