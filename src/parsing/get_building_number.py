import re

def get_building_number(raw_address: str) -> str: 
    buildingRegex = r"\d+\w{0,3}\/{0,1}\d*\w{0,3}"
    building = ""
    match = re.search(buildingRegex, raw_address)
    if match is not None:
        building = match.group()

    return building
