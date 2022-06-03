from dash import dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
yes_no_options=["Yes","No"]
layout = html.Div(children=[
                    
                    

                    html.Div(className='HeartBeat',children=[html.P("CAN YOU PROVIDE HIGH BP, LOW BP,CHOLESTROL AND GLUCOSE LEVEL VALUES?",style={'text-align':'center','color': '#555','font-size': 'x-large'}),
                    html.Div(children=dcc.Link(html.Button("Yes",style={'margin-bottom': '2rem','width': '30%','margin-left': '34%'}),href="/page3"),),
                    html.Div(dcc.Link(html.Button("No",style={'margin-bottom': '2rem','width': '30%','margin-left': '34%'}),href="/page1"))
                    ])

])