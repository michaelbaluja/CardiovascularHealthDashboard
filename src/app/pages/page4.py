from dash.dependencies import Input, Output
from dash import html, dcc, callback
import json
from urllib.request import urlopen
from src.app import cdc_plots
from plotly.graph_objects import Figure

# 1
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
# Used for plotting. We can predownload the json if thats better ?

header_style = {
    "padding": "25px",
    "text-align": "center",
    "background": "#1abc9c",
    "color": "white",
    "font-size": "xx-large",
}

layout = html.Div(
    children=[
        # 1
        html.H1(
            "Risk Factor Analysis",
            style=header_style
        ),
        html.Div(
            style={'display': 'inline-flex', 'margin-top': '-1%'},
            children=[
                dcc.Link(
                    html.Button(
                        "Risk Factor Analysis",
                        style={
                            'width': '271%',
                            'margin-left': '0%',
                            'background': 'rgb(26, 188, 156)',
                            'color': 'white',
                            'border': 'rgb(26, 188, 156)',
                            'text-transform': 'Capitalize',
                            'font-family': ' "Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'
                        }
                    ),
                    href="/page2"
                ),
                dcc.Link(
                    html.Button(
                        "Location Visualizations",
                        style={
                            'width': '247%',
                            'margin-left': '154%',
                            'background': 'rgb(26, 188, 156)',
                            'color': 'white',
                            'border': 'rgb(26, 188, 156)',
                            'text-transform': 'Capitalize',
                            'font-family': ' "Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'
                        }
                    ),
                    href="/page4"),
            ]
        ),
        # 2[
        html.H3("Enter Zip code", style={'margin-left': '2%'}),
        html.P(
            "Enter your zipcode to see location based infographics for cardiovasular related diseases.",
            style={'margin-left': '4%'}
        ),
        dcc.Dropdown(
            id='zip-select',
            options=cdc_plots.get_all_zips(),
            style={"width": "200px", "margin-left": "4%"}
        ),
        html.Br(),
        dcc.Graph(id='mort-county'),
        dcc.Graph(id='mort-trend'),
        html.Br(),
        html.H3("Map of Nearby Hospitals", style={'margin-left': '2%'}),
        dcc.Graph(
            id='hosp-map',
            style={"width": "95%", "height": '100%', 'margin-left': '2.5%'}
        ),
        html.Br(),
        html.Br()
    ]
)


@callback(
    Output('mort-county', 'figure'),
    Input('zip-select', 'value'),
    prevent_initial_call=True
)
def age_plot(zip: str) -> Figure:
    """Callback wrapper for age statistics.

    Parameters
    ----------
    zip : str

    See Also
    --------
    cdc_plots.get_age_statistics
    """

    return cdc_plots.get_age_statistics(zip)


@callback(
    Output('mort-trend', 'figure'),
    Input('zip-select', 'value'),
    prevent_initial_call=True
)
def trend_plot(zip: str) -> Figure:
    """Callback wrapper for age statistics according to trends.

    Parameters
    ----------
    zip : str

    See Also
    --------
    cdc_plots.get_trend_statistics
    """

    return cdc_plots.get_trend_statistics(zip)


@callback(
    Output('hosp-map', 'figure'),
    Input('zip-select', 'value'),
    prevent_initial_call=True
)
def map_plot(zip: int) -> Figure:
    """Callback wrapper for hospital generation map.

    Parameters
    ----------
    zip : str

    See Also
    --------
    cdc_plots.get_hopsital_data
    """

    return cdc_plots.get_hospital_data(zip)
