from typing import List
import re

from .address_parser.postal_city_address_parser import PostalCityAddressParser
from .address_parser.city_street_address_parser import CityStreetAddressParser
from .address_parser.postal_street_address_parser import PostalStreetAddressParser
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
        self._parsers = [CityStreetAddressParser(self._address_data_provider, self._address_builder),
                        PostalStreetAddressParser(self._address_data_provider, self._address_builder),
                        PostalCityAddressParser(self._address_data_provider, self._address_builder)]

    def parse_address(self, raw_address: str) -> List[Address]:
        RECORDS_THRESHOLD = 0.85
        records = []
    
        addresses = [raw_address, self._split_uppercase(raw_address)]

        for parser in self._parsers:
            for address in addresses: 
                new_records = parser.parse_address(address)
                records.extend(new_records)
                records = sorted(records, key=lambda r: r.score, reverse=True)[:3]
                if len(records) > 0 and records[0].score >= RECORDS_THRESHOLD:
                    return records
        return records

    def _split_uppercase(self, raw_address: str) -> str:
        return ' '.join(re.findall('[A-Z][^A-Z]*', raw_address))