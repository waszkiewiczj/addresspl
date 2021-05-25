import re

def get_postal_code(raw_address: str) -> str:
    postalCodeRegex = r"\d{2}-?\d{3}"
    postalCode = ""
    match = re.search(postalCodeRegex, raw_address)
    if match is not None:
        postalCode = match.group()

    return postalCode