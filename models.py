from typing import List
from dataclasses import dataclass


@dataclass
class Address: 
    postal_code: str
    street: str
    building_number: str
    city: str
    score: float
    is_postal_code_matching: bool = True


@dataclass
class City: 
    name: str
    score: float
