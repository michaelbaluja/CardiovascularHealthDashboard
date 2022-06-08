import os

import pandas as pd


class BaseDataset:
    def __init__(self, filename, **kwargs):
        filepath = os.path.join(
            os.path.dirname(__file__),
            filename
        )
        self.filename = filename
        self._data = pd.read_csv(filepath, **kwargs)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, df: pd.DataFrame):
        self._data = df


class KaggleDataset(BaseDataset):
    def __init__(self):
        super().__init__('kaggle_cleaned.csv')


class Kaggle3Dataset(BaseDataset):
    def __init__(self):
        super().__init__('Kagglecleaned3.csv')


class Trends100Dataset(BaseDataset):
    def __init__(self):
        super().__init__('trends_by_100k.csv')


class HospitalDataset(BaseDataset):
    def __init__(self):
        super().__init__('us_hospital_locations.csv', dtype={'ZIP': str})
