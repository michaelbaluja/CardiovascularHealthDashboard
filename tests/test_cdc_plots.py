from ..src.app import cdc_plots
import numpy as np
import plotly
import pytest

def test_get_all_zips():
    zipcodes = cdc_plots.get_all_zips()
    assert isinstance(zipcodes, np.ndarray) and all(isinstance(zipcode, str) for zipcode in zipcodes) 
    assert all(num.isdigit() for zipcode in zipcodes for num in zipcode)

def test_get_age_statistics():
    with pytest.raises(Exception) as e_info:
        cdc_plots.get_age_statistics(int(92037))
    with pytest.raises(Exception) as e_info:
        cdc_plots.get_age_statistics(('923AB'))
    assert isinstance(cdc_plots.get_age_statistics('92037'), plotly.graph_objs.Figure)

def test_get_trend_statistics():
    with pytest.raises(Exception):
        cdc_plots.get_trend_statistics(int(92037))
    with pytest.raises(Exception):
        cdc_plots.get_trend_statistics(('923AB'))
    assert isinstance(cdc_plots.get_trend_statistics('92037'), plotly.graph_objs.Figure)

def test_get_hospital_data():
    with pytest.raises(Exception):
        cdc_plots.get_hospital_data(int(92037))
    with pytest.raises(Exception):
        cdc_plots.get_hospital_data(('923AB'))
    assert isinstance(cdc_plots.get_hospital_data('92037'), plotly.graph_objs.Figure)

