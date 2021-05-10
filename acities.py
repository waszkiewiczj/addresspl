from typing import List
from models import City


def get_cities(ad)-> List[City]:
    
    return [
        {
            city: "Warszawa",
            score: 0.99
        },
        {
            city: "Gdańsk",
            score: 0.78
        }
    ]