from dash import dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

gender_options=["Male","Female"]
yes_no_options=["Yes","No"]

layout = html.Div(
        
        children=html.Div(children=
                [html.Div(className='HeartBeat', style={'top': '48%','left': '20%'},children=[
                                    html.P("PLEASE FILL OUT THE FOLLOWING DETAILS",style={'color': 'rgb(0, 255, 156)','font-size': 'x-large'}),
                                    html.Div(className='app-controls-block', children=[
                                        html.P("Name"),
                                        dcc.Input(
                                            className='app-input',
                                            id='user-name',
                                        ),
                                    ]),
                                    html.Div(className='app-controls-block', children=[
                                        html.P("Age" ),
                                        dcc.Input(
                                            className='app-input',
                                            id='age',
                                        ),
                                    ]),
                                    html.Div(className='app-controls-block', children=[
                                        html.P("Gender", ),
                                        dcc.Dropdown(id = 'genderdrop',
                                                    options = gender_options,
                                                ),
                                    ]),
                                    html.Div(className='app-controls-block', children=[
                                        html.P("Height(cms)" ),
                                        dcc.Input(
                                            className='app-input',
                                            id='height',
                                        ),
                                    ]),
                                    html.Div(className='app-controls-block', children=[
                        html.P("High BP level", ),
                        dcc.Input(
                            className='app-input',
                            id='highbp',
                        ),
                    ]),
                    html.Div(className='app-controls-block', children=[
                        html.P("Low BP level", ),
                        dcc.Input(
                            className='app-input',
                            id='lowbp',
                        ),
                    ]),]),
        html.Div(className='HeartBeat', style={'top':'50%'},children=[
                        html.Div(className='app-controls-block', children=[
                            html.P("Weight(kgs)" ),
                            dcc.Input(
                                className='app-input',
                                id='weight',
                            ),
                        ]),
                        html.Div(className='app-controls-block', children=[
                            html.P("Do you Smoke?", ),
                            dcc.Dropdown(id = 'smoke',
                                        options = yes_no_options,
                                    ),
                        ]),
                        html.Div(className='app-controls-block', children=[
                            html.P("Do you Drink?", ),
                            dcc.Dropdown(id = 'drink',
                                        options = yes_no_options,
                                    ),
                        ]),
                        html.Div(className='app-controls-block', children=[
                            html.P("Do you Exercise Regularly?", ),
                            dcc.Dropdown(id = 'exercise',
                                        options = yes_no_options,
                                    ),
                        ]),
                        html.Div(className='app-controls-block', children=[
                        html.P("Cholestrol level", ),
                        dcc.Input(
                            className='app-input',
                            id='cholestrol',
                        ),
                    ]),
                    html.Div(className='app-controls-block', children=[
                        html.P("Glucose level", ),
                        dcc.Input(
                            className='app-input',
                            id='glucose',
                        ),
                    ]),
        ]),
                       
                    
                    
                    html.Div(className='app-controls-block',children=
                    html.Div(className='outer',children=[
                        html.Div(className='inner'),html.Div(className="Number",id="predict",children=[])
                    ]
                                )),
                    dcc.Link(html.Button("Show General Stats",style={'width': '22%','margin-left': '70%','margin-top': '2%'}),href="/page2"),
                    
                    
                    
                    

                ]))
                  



@callback(
    Output(component_id='predict_full',component_property= 'children'),
    [Input('age', 'value'),
        Input('genderdrop', 'value'),
        Input('height','value'),
        Input('weight','value'),
        Input('smoke','value'),
        Input('drink','value'),
        Input('exercise','value'),
        Input('highbp','value'),
        Input('lowbp','value'),
        Input('glucose','value'),
        Input('cholestrol','value')
        ])
def predict(age,genderdrop,height,weight,smoke,drink,exercise,highbp,lowbp,glucose,cholestrol):
        #['gender','height','weight','ap_hi','ap_lo','gluc','cholesterol','smoke','alco','active','age in yrs']
        #['gender','height','weight','smoke','alco','active','age in yrs']
        print(age,genderdrop,height,weight,highbp,lowbp,glucose,cholestrol,smoke,drink,exercise)
        
        loaded_model = pickle.load(open("full_finalized_model.sav", 'rb'))
        gender_value=500
        smoke_value=500
        drink_value=500
        exercise_value=500
        

        if(genderdrop=="Male"):
            gender_value=1
        elif(genderdrop=="Female"):
            gender_value=2
        
        if(smoke=="Yes"):
            smoke_value=1
        elif(genderdrop=="No"):
            smoke_value=0
        
        if(drink=="Yes"):
            drink_value=1
        elif(drink=="No"):
            drink_value=0
        
        if(exercise=="Yes"):
            exercise_value=1
        elif(exercise=="No"):
            exercise_value=0
        
        if(age==None or genderdrop==None or height==None or highbp==None or lowbp==None or glucose==None or cholestrol==None or weight==None or smoke==None or drink==None or exercise==None):
            result=[[0,-1]]
        else:
            result = loaded_model.predict_proba([[gender_value,height,weight,highbp,lowbp,glucose,cholestrol,smoke_value,drink_value,exercise_value,age]])
        

        return round(result[0][1],2)