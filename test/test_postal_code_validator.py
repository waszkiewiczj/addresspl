import pytest

from validatepostalcode import PostalCodeValidator
from models import Address


def get_validator() -> PostalCodeValidator:
    return PostalCodeValidator(
        postal_code_csv="postal_code_validator_data.csv",
        city_column_name="city",
        postal_code_column_name="postal_code",
    )


class TestPostalCodeValidator:

    @pytest.mark.parametrize("city,postal_code", [
        ["City1", "00-001"],
        ["City2", "00-002"],
        ["City1", "00-004"],
        ["city1", "00-001"],
    ])
    def test_valid_code(self, city, postal_code):
        validator = get_validator()
        valid_address = Address(postal_code, "StreetName", "1", city, 1)

        is_valid = validator.is_valid(valid_address)

        assert is_valid

    @pytest.mark.parametrize("city,postal_code", [
        ["City1", "00-002"],    # postal code and city exists, but don`t match
        ["City4", "00-001"],    # postal code exists, city not
        ["City1", "00-005"],    # postal code doesn't exist, city does
        ["City5", "00-006"],    # postal code and city don't exist
    ])
    def test_invalid_code(self, city, postal_code):
        validator = get_validator()
        invalid_address = Address(postal_code, "StreetName", "1", city, 1)

        is_valid = validator.is_valid(invalid_address)

        assert not is_valid

    @pytest.mark.parametrize("city,postal_code,is_valid", [
        ["City1", "00-001", True],
        ["City7", "00-001", False],
    ])
    def test_validate_single(self, city, postal_code, is_valid):
        validator = get_validator()
        address = Address(postal_code, "StreetName", "1", city, 1)

        validated_address = validator.validate_single(address)

        assert validated_address.is_postal_code_matching == is_valid

    def test_validate(self):
        validator = get_validator()
        valid_address = Address("00-001", "StreetName", "1", "City1", 1)
        invalid_address = Address("00-007", "StreetName", "1", "City1", 1)
        addresses = [valid_address, invalid_address]

        validated_addresses = validator.validate(addresses)

        assert validated_addresses[0].is_postal_code_matching
        assert not validated_addresses[1].is_postal_code_matching
