from typing import List
from dataclasses import dataclass

@dataclass
class Address: 
    postal_code: str
    street: str
    building_number: str
    city: str
    score: float
    errors: List[str]

@dataclass
class City: 
    name: str
    score: float
