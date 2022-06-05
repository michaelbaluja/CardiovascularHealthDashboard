import uszipcode

from .exceptions import InvalidZipCodeError


def _zip_to_county(zipcode: str):
    """Validate format of zipcode and return corresponding county.

    Parameters
    ----------
    zipcode : str

    Returns
    -------
    str

    Raises
    -----
    InvalidZipCodeError
        The provided zipcode is not present in the United States.
    """

    engine = uszipcode.SearchEngine()
    loc = engine.by_zipcode(zipcode)
    if loc:
        return loc.county
    else:
        raise InvalidZipCodeError(zipcode)


def _convert_imp_metr_height(height: float):
    """Convert a height in inches to centimeters.

    Parameters
    ----------
    height : float
        Height in inches.

    Returns
    -------
    float
        Height in centimeters.
    """
    if height is None:
        return
    return height * 2.54


def _convert_imp_metr_weight(weight: float):
    """Convert a weight in pounds to kilograms.

    Parameters
    ----------
    weight : float
        Weight in pounds.

    Returns
    -------
    float
        Weight in kilograms.
    """

    if weight is None:
        return
    return weight * 0.45359237
