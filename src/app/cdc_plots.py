import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from src.app.utils import validation
from src.app.data import datasets
from uszipcode import SearchEngine

DF_100K_FILEPATH = '../../data/trends_by_100k.csv'
HOSPITAL_DF_PATH = '../../data/us_hospital_locations.csv'

df_100k = datasets.Trends100Dataset().data
hosp_df = datasets.HospitalDataset().data


def get_all_zips() -> list[str]:
    """Returns all the zip codes in the database.

    Returns
    -------
    list of str
    """

    return hosp_df['ZIP'].unique()


def get_age_statistics(zip: str) -> Figure:
    """Generates the plot with number of mortalities from 1999-2018 (combined), 
    categorized by age group and type of heart disease.

    Source - Rates and Trends in Coronary Heart Disease and Stroke by CDC

    Parameters
    ----------
    zip : str
        Zipcode of user.
    df : pd.DataFrame
        Dataframe with trends per 100k.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """

    assert isinstance(zip, str) and all(num.isdigit()for num in zip), \
        'Zip must be a represented as numerical string.'

    county_name = validation._zip_to_county(zip)
    if county_name.rsplit(' ', 1)[-1] == 'County':
        county_name = county_name.rsplit(' ', 1)[0]
    county_df = df_100k[df_100k['County'] == county_name]\
        .groupby(['Age', 'Topic']).sum().reset_index()
    fig = px.bar(
        x=county_df["Age"],
        color=county_df["Topic"],
        y=county_df["Data_Value"],
        labels={
            'x': 'Age Group',
            'y': 'Number of Mortalities',
            'color': 'Heart Disease Type'
        },
        title=f'Number of Mortatilies in {county_name} County '
        '(per 100k) from 1999-2018 (combined)',
        barmode='group',
        height=400, width=800
    )
    return fig


def get_trend_statistics(zip: str) -> Figure:
    """Generates line plot showing cardiovascular disease trend from 1999-2018 for 
    age groups (35-60 and 60 & above), for a particular zipcode area.

    Source - Rates and Trends in Coronary Heart Disease and Stroke by CDC

    Parameters
    ----------
    zip : str
        Zipcode of user.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    assert isinstance(zip, str) and all(num.isdigit()for num in zip), \
        'Zip must be a represented as numerical string.'

    county_name = validation._zip_to_county(zip)
    if county_name.rsplit(' ', 1)[-1] == 'County':
        county_name = county_name.rsplit(' ', 1)[0]
    county_df = df_100k[
        (df_100k['County'] == county_name) &
        (df_100k['Topic'] == 'Coronary Heart Disease')
    ].sort_values('Year')
    fig = px.line(
        x=county_df["Year"], color=county_df["Age"],
        y=county_df['Data_Value'],
        labels={
            'x': 'Year',
            'y': 'Number of Mortalities',
            'color': 'Age Group'
        },
        title=f'Number of Moratilies from Heart Disease in {county_name} '
        'County (per 100k) every year, 1999-2018',
        height=600
    )
    return fig


def get_hospital_data(zip: str) -> Figure:
    """Generates a map with hospital information for the given zip code. Map overlays from Open Street Map.

    Parameters
    ----------
    zip : str
        Zipcode of user.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    assert isinstance(zip, str) and all(num.isdigit()for num in zip), \
        'Zip must be a represented as numerical string.'

    engine = SearchEngine()
    zip_obj = engine.by_zipcode(zip)
    lat_str = zip_obj.lat
    lng_str = zip_obj.lng
    center_dict = {'lat': lat_str, 'lon': lng_str}

    fig = px.scatter_mapbox(
        hosp_df,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="NAME",
        hover_data=["ADDRESS", "WEBSITE"],
        color_discrete_sequence=["light blue"],
        zoom=12,
        center=center_dict
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_traces(marker_size=15)
    fig.update_layout(margin={"r": 1, "t": 1, "l": 1, "b": 1})

    return fig
