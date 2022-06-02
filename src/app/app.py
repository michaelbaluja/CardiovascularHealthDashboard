from layout_main import run_standalone_app
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px

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
    
def layout():
    return html.Div(id='dash-view-body', className='app-body', children=[
        html.Div(
            id='dash-view-container',
            children=[
                html.Div(
                    id='dash-view-graph-container-1',
                    children=[
                        dcc.Graph(id='pie-plot')
                    ]
                ),
                html.Div(
                    id='dash-view-graph-container-2',
                    children=[
                        dcc.Graph(id='pie-plot-2')
                    ]
                ),
            ]
        ),
    html.Div(id='dash-view-control-tabs', className='control-tabs', children=[
        dcc.Tabs(id='dash-view-tabs', value='what-is', children=[
            dcc.Tab(
                label='About',
                value='what-is',
                children=html.Div(className='control-tab', children=[
                    html.H4(className='what-is', children='Cardiovasular disease Analysis'),
                    html.P('Text to be added'),
                ])
            ),
            dcc.Tab(
                label='General',
                value='data',
                children=html.Div(className='general-tab', children=[
                    html.Div(className='app-controls-block', children=[
                        html.P("Name", style={'margin-left': '15px'}),
                        dcc.Input(
                            className='app-input',
                            id='user-name',
                        ),
                        html.Br(),
                        html.Div(className='app-controls-block', children=[
                            html.Div(style={'float': 'left'}, children=[
                                #html.P("Age", style={'margin-left': '15px'}),
                                html.P("State", style={'margin-left': '15px'}),
                                dcc.Dropdown(id = 'general-state',
                                    options = state_labels,
                                ),
                                # dcc.Input(
                                #     className='app-input',
                                #     id='user-age',
                                # ),
                            ]),
                            html.Div(style={'float': 'right'}, children=[
                                html.P("Do you smoke?", style={'margin-left': '15px'}),
                                dcc.RadioItems(
                                    id='smoke-select',
                                    options=[
                                        {
                                            'label': 'Yes',
                                            'value': 'y'
                                        },
                                        {
                                            'label': 'No',
                                            'value': 'n'
                                        }
                                    ],
                                ),
                            ]),
                        ]),
                        html.Br(),
                        html.Br(),
                        html.Div(className='app-controls-block', children=[
                            html.Div(style={'float': 'left'}, children=[
                                #html.P("Weight", style={'margin-left': '15px'}),
                                html.P("County", style={'margin-left': '15px'}),
                                dcc.Dropdown(id = 'general-county',
                                    #options = state_labels,
                                ),
                                # dcc.Input(
                                #     className='app-input',
                                #     id='user-weight',
                                # ),
                                html.Br(),
                                html.Br(),
                            ]),
                            html.Div(style={'float': 'right'}, children=[
                                html.Br(),
                                html.P("Are you active?", style={'margin-left': '15px'}),
                                dcc.RadioItems(
                                    id='active-select',
                                    options=[
                                        {
                                            'label': 'Yes',
                                            'value': 'y'
                                        },
                                        {
                                            'label': 'No',
                                            'value': 'n'
                                        }
                                    ],
                                ),
                                html.Br(),
                                html.Br(),
                            ]),
                        ]),
                        html.Br(),
                        html.Br(),
                        html.Div(className='app-controls-block', children=[
                            html.P("Height"),
                            dcc.Input(
                                className='app-input',
                                id='user-height',
                            ),
                            html.Br(),
                            html.Br(),
                        ]),
                        html.A(
                        children=html.Button(
                            "Submit",
                            id='dash-view-submit-data',
                            className='control-download',
                        ),
                    )
                    ]),
                ])
            ),
            dcc.Tab(
                label='Detailed',
                children=html.Div(className='control-tab', children=[
                    html.Div(
                        id='dash-view-entry-dropdown-container',
                        className='app-controls-block',
                        children=[]
                    ),
                    html.Br(),
                    html.Div(
                        id='dash-view-sel-or-cov-container',
                        children=[]),
                        ]),
                    ),
                ]),
            ])
        ])

def header_colors():
    return {
        'bg_color': '#2596be',
        'font_color': 'white'
    }

def callbacks(_app):
    @_app.callback(
    Output(component_id='general-county', component_property='options'),
    Input(component_id='general-state', component_property='value')
    )
    def update_counties(input_value):
        return df.groupby('State').get_group(input_value)['County'].unique()

    @_app.callback(
    Output(component_id='pie-plot', component_property='figure'),
    [Input(component_id='general-county', component_property='value'),
    Input(component_id='general-state', component_property='value'),
    Input(component_id='dash-view-submit-data', component_property='n_clicks')]
    )
    def plot_pie_graph(county_value, state_value, n_clicks):
        if n_clicks != 0:
            reduced_df = df.groupby(['State', 'County', 'Data_Value_Unit','Topic']).sum().loc[
                state_value, county_value, 'per 100,000']
            fig = px.pie(df, values='Data_Value', names='Topic', title='Types of Heart Disease (per 100,000)',
                width=400, height=375)
            return fig


df = read_data('../../data/Trends_heart_disease.csv')
clean_df(df)

state_labels = [{'label' : i, 'value' : i} for i in df['State'].unique()]

app = run_standalone_app(layout, callbacks, header_colors, __file__)
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=5006)