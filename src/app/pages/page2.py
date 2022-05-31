from dash import dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import plotly.express as px
import plotly.graph_objects as go
from pages import page2



def read_data(filepath):
    return pd.read_csv(filepath)

def clean_df(df):
    '''
    Cleans dataframe IN PLACE
    '''
    assert isinstance(df, pd.DataFrame)
    
    df['Data_Value'] = df["Data_Value"].str.replace(",","").astype(float)
    df.drop('StratificationCategory1', axis=1, inplace=True)
    df.rename(columns={'Stratification1': 'Age Group', 'LocationAbbr': 'State', 
                      'LocationDesc': 'County'}, inplace=True)
df = read_data('../../data/Trends_heart_disease.csv')
clean_df(df)

state_labels = [{'label' : i, 'value' : i} for i in df['State'].unique()]

layout = html.Div(html.Div(className='app-controls-block', children=[
                            html.Div(style={'float': 'left'}, children=[
                                html.P("State", style={'margin-left': '15px'}),
                                dcc.Dropdown(id = 'general-state',
                                    options = state_labels,
                                ),
                            ]),
                            html.Div(style={'float': 'left'}, children=[
                                html.P("County", style={'margin-left': '15px'}),
                                dcc.Dropdown(id = 'general-county',
                                    
                                ),
                                
                                html.Br(),
                                html.Br(),
                            ]),
                            #html.Div(html.Button(id='dash-view-submit-data')),
                            html.Div(
                            id='dash-view-container',
                            children=
                                html.Div(
                                    id='dash-view-graph-container-1',
                                    children=
                                        dcc.Graph(id='pie-plot')
                                    
                                ),)
                            
                            ]),
                        
                                    
                                )

@callback(Output(component_id='general-county', component_property='options'),
    Input(component_id='general-state', component_property='value')
    )
def update_counties(input_value):
    return df.groupby('State').get_group(input_value)['County'].unique()

@callback(
    Output(component_id='pie-plot', component_property='figure'),
   
    [Input(component_id='general-county', component_property='value'),
    Input(component_id='general-state', component_property='value'),
    Input(component_id='predict', component_property='number')
    ]
    )
def plot_pie_graph(county_value, state_value,predict):
    if(state_value==None or county_value==None):
        labels = ['Select state and county']
        values = [4500]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        return fig,
    '''
    reduced_df = df.groupby(['State', 'County', 'Data_Value_Unit','Topic']).sum().loc[
        state_value, county_value, 'per 100,000']
    fig = px.pie(df, values='Data_Value', names='Topic', title='Types of Heart Disease (per 100,000)',
        width=400, height=375)
    return fig'''



