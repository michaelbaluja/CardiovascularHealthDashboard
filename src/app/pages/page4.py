import pandas as pd
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, Dash, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import json
from urllib.request import urlopen
import cdc_plots

#1
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
#Used for plotting. We can predownload the json if thats better ? 

header_style = {
  "padding": "25px",
  "text-align": "center",
  "background": "#1abc9c",
  "color": "white",
  "font-size": "xx-large",
}

layout = html.Div(children=[
                    #1
                    html.H1("Risk Factor Analysis", style=header_style),
                    html.Div(style={ 'display': 'inline-flex'},
                        children=[  dcc.Link(html.Button("Risk Factor Analysis",style={'width': '262%','margin-left': '0%','background': 'rgb(26, 188, 156)','color':'white','border': 'rgb(26, 188, 156)','text-transform':'Capitalize'
                        ,'font-family':' "Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'}), href="/page2"),
                                    dcc.Link(html.Button("Location Visualizations",style={'width': '262%','margin-left': '144%','background': 'rgb(26, 188, 156)','color':'white','border': 'rgb(26, 188, 156)','text-transform':'Capitalize',
                                    'font-family':' "Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'}), href="/page4"),]),
                    #2[
                    html.H3("Enter Zip code", style={'margin-left':'2%'}),
                    html.P("Enter your zipcode to see location based infographics for cardiovasular related diseases.", style={'margin-left':'4%'}),
                    dcc.Dropdown(id='zip-select', options=cdc_plots.get_all_zips(), style={"width":"200px", "margin-left":"4%"}),
                    # dcc.Input(id='zip-input', style={"display": "inline-block","width": "220px", "margin-left": "4%"}),
                    # html.Button(id='submit-button', type='submit', children='Submit', style=
                    #     {"width":"150px","margin-left": "4%"}),
                    html.Br(),
                    dcc.Graph(id='mort-county'),
                    dcc.Graph(id='mort-trend'),
                    html.Br(),
                    html.H3("Map of Nearby Hospitals", style={'margin-left':'2%'}),
                    dcc.Graph(id='hosp-map', style={"width":"95%", "height":'100%', 'margin-left':'2.5%'}),
                    html.Br(),
                    html.Br()
                ])

@callback(
    Output('mort-county', 'figure'),
    Input('zip-select', 'value'), prevent_initial_call=True
)
def age_plot(zip:int):
    return cdc_plots.get_age_statistics(str(zip))

@callback(
    Output('mort-trend', 'figure'),
    Input('zip-select', 'value'), prevent_initial_call=True
)
def trend_plot(zip:int):
    return cdc_plots.get_trend_statistics(str(zip))

@callback(
    Output('hosp-map', 'figure'),
    Input('zip-select', 'value'), prevent_initial_call=True
)
def map_plot(zip:int):
    return cdc_plots.get_hospital_data(str(zip))