import re


def get_building_number(raw_address: str) -> str: 
    building_regex = r"\d+\w{0,3}\/{0,1}\d*\w{0,3}"
    building = ""
    match = re.search(building_regex, raw_address)
    if match is not None:
        building = match.group()

    return building
