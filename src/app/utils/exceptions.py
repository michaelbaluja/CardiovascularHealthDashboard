class InvalidZipCodeError(Exception):
    def __init__(self, zip):
        super().__init__(f'\'{zip}\' is not a valid US zipcode.')
