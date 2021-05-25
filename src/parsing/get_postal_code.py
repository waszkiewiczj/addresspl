import re


def get_postal_code(raw_address: str) -> str:
    postal_code_regex = r"\d{2}-?\d{3}"
    postal_code = ""
    match = re.search(postal_code_regex, raw_address)
    if match is not None:
        postal_code = match.group()

    return postal_code
