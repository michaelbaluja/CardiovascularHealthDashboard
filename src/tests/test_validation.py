from multiprocessing.sharedctypes import Value
import pytest
import uszipcode

from src import validation
from src.exceptions import InvalidZipCodeError


@pytest.fixture
def zipcode_engine():
    return uszipcode.SearchEngine()


def test_validate_user_input_valid():
    user_input = ('92592', '71', '160', '24')
    expected_validation = ('Riverside County', 22.32, 24)
    assert validation.validate_user_information(
        *user_input) == expected_validation


def test_zip_to_county_valid(zipcode_engine):
    assert validation._zip_to_county('92037') == 'San Diego County'


def test_zip_to_county_invalid(zipcode_engine):
    with pytest.raises(InvalidZipCodeError):
        validation._zip_to_county('00000')


def test_calculate_bmi_valid():
    # Accurate up to ten's digit
    assert round(validation._calculate_bmi(69, 145) - 21.4, 1) == 0


def test_calculate_bmi_invalid_height_type():
    with pytest.raises(ValueError):
        validation._calculate_bmi('ten', 100)


def test_calculate_bmi_invalid_height_value():
    with pytest.raises(ValueError):
        validation._calculate_bmi(-60, 130)


def test_calculate_bmi_invalid_weight_type():
    with pytest.raises(ValueError):
        validation._calculate_bmi(60, 'onehundred')


def test_calculate_bmi_invalid_weight_valid():
    with pytest.raises(ValueError):
        validation._calculate_bmi(65, -120)


def test_validate_age_invalid_value():
    with pytest.raises(ValueError):
        validation._validate_age(-15)


def test_validate_age_invalid_type():
    with pytest.raises(ValueError):
        validation._validate_age('seventy')


def test_validate_age_valid_str():
    assert validation._validate_age('15') == 15


def test_validate_age_valid_int():
    assert validation._validate_age(15) == 15


def test_validate_age_valid_float():
    assert validation._validate_age(15.5) == 15
