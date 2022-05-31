from dash import dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

gender_options=["Male","Female"]
yes_no_options=["Yes","No"]
layout = html.Div(
        
        children=html.Div(children=
                [html.Div(className='HeartBeat', style={'top': '38%','left': '20%'},children=[
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
                                    ]),]),
        html.Div(className='HeartBeat', style={'top':'40%'},children=[
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
        ]),
                       
                    
                    
                    html.Div(className='app-controls-block',children=
                    html.Div(className='outer',children=[
                        html.Div(className='inner'),html.Div(className="Number",id="predict",children=[])
                    ]
                                )),
                    dcc.Link(html.Button("Show General Stats",style={'width': '22%','margin-left': '36%','margin-top': '2%'}),href="/page2"),
                    
                    
                    
                    

                ]))
            



@callback(
    Output(component_id='predict',component_property= 'children'),
    [Input('age', 'value'),
        Input('genderdrop', 'value'),
        Input('height','value'),
        Input('weight','value'),
        Input('smoke','value'),
        Input('drink','value'),
        Input('exercise','value'),
        ])
def predict(age,genderdrop,height,weight,smoke,drink,exercise):
    
        #['gender','height','weight','smoke','alco','active','age in yrs']
        print(age,genderdrop,height,weight,smoke,drink,exercise)
        
        loaded_model = pickle.load(open("half_finalized_model.sav", 'rb'))
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
        
        if(age==None or genderdrop==None or height==None or weight==None or smoke==None or drink==None or exercise==None):
            result=[[0,-1]]
        else:
            result = loaded_model.predict_proba([[gender_value,height,weight,smoke_value,drink_value,exercise_value,age]])
        

        return round(result[0][1],2)