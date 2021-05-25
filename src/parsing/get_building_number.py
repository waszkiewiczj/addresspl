import re


def get_building_number(raw_address: str) -> str: 
    building_regex = r"\d+\w{0,3}\/{0,1}\d*\w{0,3}"
    building = ""
    match = re.findall(building_regex, raw_address)
    if len(match) > 0:
        building = match[-1].strip()

    return building
