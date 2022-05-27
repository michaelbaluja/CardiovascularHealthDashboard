import uszipcode

from .exceptions import InvalidZipCodeError


def validate_user_information(
        zip: str,
        height: str,
        weight: str,
        age: str
) -> tuple:
    """Validate user-inputted personal information.

    Parameters
    ----------
    zip : str
        Zipcode of user.
    height : float
        User's height in inches.
    weight : float
        User's weight in pounds.
    age : int
        User's Age.

    Returns
    -------
    (county: str, bmi: float, age: int)
    """

    return (
        _zip_to_county(zip),
        _calculate_bmi(height, weight),
        _validate_age(age)
    )


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


def _calculate_bmi(height: str, weight: str) -> float:
    """Calcuate BMI from height in inches and weight in pounds.

    Parameters
    ----------
    height : float
    weight : float

    Returns
    -------
    float

    Raises
    ------
    ValueError
        height and/or weight are not castable to float.
    ValueError
        height and/or weight are nonpositive.

    Notes
    -----
    BMI is calculated as weight / (height^2) for weight in kilograms
    and height in meters. To calculate for weight in pounds and height
    in inches, we multiply height in inches by 0.0254 to convert to 
    meters, and multiply weight in pounds by 0.4535924 to convert to
    kilograms. If we perform the original calculation with weight in
    pounds and height in inches, conversion corresponds to multiplying 
    this calculation by 703.072416
    """

    height = float(height)
    weight = float(weight)

    if height <= 0:
        raise ValueError(
            f'Height must be positive (Entered: {height})'
        )
    if weight <= 0:
        raise ValueError(
            f'Weight must be positive (Entered: {weight})'
        )

    conversion = 703.072416

    return round(conversion * (weight/height**2), 2)


def _validate_age(age: str) -> int:
    """Validate and return user age as integer.

    Parameters
    ----------
    age : str

    Returns
    -------
    int

    Raises
    ------
    TypeError
        age cannot be converted to integer value.
    """

    if int(age) > 0:
        return int(age)
    else:
        raise ValueError('age must be positive')
