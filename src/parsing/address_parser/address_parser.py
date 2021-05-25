from abc import ABC, abstractmethod
from typing import List

from ..models.address import Address

class AddressParser(ABC):
    
    @abstractmethod
    def parse_address(self, raw_address: str) -> List[Address]:
        pass