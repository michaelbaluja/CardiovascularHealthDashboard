import pandas as pd
import plotly.express as px
from utils.validation import _zip_to_county

DF_PERCENT_FILEPATH =  '../../data/trends_by_percent.csv'
DF_100K_FILEPATH = '../../data/trends_by_100k.csv'
TRENDS_DF_PATH = '../../data/trends_heart_disease.csv'

df_percent = pd.read_csv(DF_PERCENT_FILEPATH)
df_100k = pd.read_csv(DF_100K_FILEPATH)
trends_df = pd.read_csv(TRENDS_DF_PATH)

def get_age_statistics(zip: str, df: pd.DataFrame):
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
    assert isinstance(df, pd.DataFrame), 'Input must be a dataframe'

    county_name = _zip_to_county(zip)
    if county_name.rsplit(' ',1)[-1] == 'County':
        county_name = county_name.rsplit(' ', 1)[0]
    county_df = df_100k[df_100k['County'] == county_name]
    fig = px.bar(county_df, x="Age", color="Topic", 
                y='Data_Value',
                title=f"Number of Moratilies in {county_name} County (per 100k) from 1999-2018 (combined)",
                barmode='group',
                height=600
            )
    fig.show()
    
def get_trend_statistics(zip: str, topic: str):
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
        (df_100k['Topic'] == topic)].sort_values('Year')
    fig = px.line(county_df, x="Year", color="Age", 
                y='Data_Value',
                title=f"Number of Moratilies in {county_name} County (per 100k) every year, 1999-2018",
                height=600
            )
    fig.show()