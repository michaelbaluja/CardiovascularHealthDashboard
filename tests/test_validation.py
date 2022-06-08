import pytest
import uszipcode

from ..src.app.utils import validation
from ..src.app.utils.exceptions import InvalidZipCodeError


@pytest.fixture
def zipcode_engine():
    return uszipcode.SearchEngine()


def test_zip_to_county_valid(zipcode_engine):
    assert validation._zip_to_county('92037') == 'San Diego County'


def test_zip_to_county_invalid(zipcode_engine):
    with pytest.raises(InvalidZipCodeError):
        validation._zip_to_county('00000')


def test_convert_imp_metr_height_valid():
    assert validation._convert_imp_metr_height(1) == 2.54


def test_cconvert_imp_metr_height_invalid():
    assert validation._convert_imp_metr_height(None) is None


def test_convert_imp_metr_weight_valid():
    assert validation._convert_imp_metr_weight(1) == 0.45359237


def test_convert_imp_metr_weight_invalid():
    assert validation._convert_imp_metr_weight(None) is None
