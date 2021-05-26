from abc import ABC, abstractmethod
from typing import List
from src.parsing.models import Address


class AddressParser(ABC):
    
    @abstractmethod
    def parse_address(self, raw_address: str) -> List[Address]:
        ...
