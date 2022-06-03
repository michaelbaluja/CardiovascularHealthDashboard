import pandas as pd
import plotly.express as px
from utils.validation import _zip_to_county
from uszipcode import SearchEngine

# DF_PERCENT_FILEPATH =  '../../data/trends_by_percent.csv'
DF_100K_FILEPATH = '../../data/trends_by_100k.csv'
#TRENDS_DF_PATH = '../../data/trends_heart_disease.csv'
HOSPITAL_DF_PATH = '../../data/us_hospital_locations.csv'

# df_percent = pd.read_csv(DF_PERCENT_FILEPATH)
df_100k = pd.read_csv(DF_100K_FILEPATH)
#trends_df = pd.read_csv(TRENDS_DF_PATH)
hosp_df = pd.read_csv(HOSPITAL_DF_PATH)

def get_all_zips():
    """Returns all the zip codes in the database
    Returns
    -------
    (list :  list of zip codes)
    """
    return hosp_df['ZIP'].unique()

def get_age_statistics(zip: str):
    """Generates the plot with age related statistics

    Parameters
    ----------
    zip : str
        Zipcode of user.
    df: pd.DataFrame
        Dataframe with 100k trends
    Returns
    -------
    (px plot :  plot with age related statistics)
    """
    assert isinstance(zip, str) and all(num.isdigit() for num in zip), 'zip must be a string with no alphabets'

    county_name = _zip_to_county(zip)
    if county_name.rsplit(' ',1)[-1] == 'County':
        county_name = county_name.rsplit(' ', 1)[0]
    county_df = df_100k[df_100k['County'] == county_name].groupby(['Age', 'Topic']).sum().reset_index()
    fig = px.bar(x=county_df["Age"], color=county_df["Topic"], 
                y=county_df["Data_Value"],
                labels={'x': 'Age Group', 'y':'Number of Mortalities', 'color':'Heart Disease Type'},
                title=f"Number of Mortatilies in {county_name} County (per 100k) from 1999-2018 (combined)",
                barmode='group',
                height=400, width=800
            )
    # print(fig.data[0].name)
    # fig.data[0].name = "Number of Mortatilies"
    # fig.data[0].hovertemplate = "Number of Mortatilies"
    return fig
    
def get_trend_statistics(zip: str):
    """Generates a trend plot showing trend from 1999-2018 for different age groups

    Parameters
    ----------
    zip : str
        Zipcode of user.

    Returns
    -------
    (px plot :  trend plot)
    """
    county_name = _zip_to_county(zip)
    if county_name.rsplit(' ',1)[-1] == 'County':
        county_name = county_name.rsplit(' ', 1)[0]
    county_df = df_100k[(df_100k['County'] == county_name) & 
        (df_100k['Topic'] == 'Coronary Heart Disease')].sort_values('Year')
    fig = px.line(x=county_df["Year"], color=county_df["Age"], 
                y=county_df['Data_Value'],
                labels={'x': 'Year','y':'Number of Mortalities', 'color':'Age Group'},
                title=f"Number of Moratilies from Heart Disease in {county_name} County (per 100k) every year, 1999-2018",
                height=600
            )
    return fig

def get_hospital_data(zip: str):
    """Generates a map with hospital information for the given zip code

    Parameters
    ----------
    zip : str
        Zipcode of user.

    Returns
    -------
    (px scatter mapbox :  map plot)
    """
    engine = SearchEngine()
    zip_obj = engine.by_zipcode(int(zip))
    lat_str = zip_obj.lat
    lng_str = zip_obj.lng
    center_dict = {'lat': lat_str, 'lon':lng_str}

    fig = px.scatter_mapbox(hosp_df, lat="LATITUDE", lon="LONGITUDE", hover_name="NAME", hover_data=["ADDRESS", "WEBSITE"],
                            color_discrete_sequence=["light blue"], zoom=12, center=center_dict)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_traces(marker_size=15)
    fig.update_layout(margin={"r":1,"t":1,"l":1,"b":1})
    return fig

