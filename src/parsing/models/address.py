from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from src.parsing.models.city import City
from src.parsing.models.street import Street


@dataclass_json
@dataclass
class Address:
    postal_code: str
    street: Street
    building_number: str
    city: City
    is_postal_code_matching: bool = True
    score: float
