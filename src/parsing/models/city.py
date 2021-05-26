from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class City: 
    name: str
    score: float
