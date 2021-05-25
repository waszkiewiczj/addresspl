from typing import List
from dataclasses import dataclass, field

from .city import City

@dataclass
class Address:
    postal_code: str
    street: str
    building_number: str
    city: City
    errors: List[str] = field(default_factory=lambda: [])
    is_postal_code_matching: bool = True



