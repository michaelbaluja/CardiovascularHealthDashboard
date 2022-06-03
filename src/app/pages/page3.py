from dash import dcc, html, Input, Output, callback
import pickle
from utils.defaults import gender_options, yes_no_options
from utils.validation import _convert_imp_metr_height, _convert_imp_metr_weight


layout = html.Div(

    children=html.Div(children=[
    
        
        html.Div(className='HeartBeat', style={'top': '48%', 'left': '20%'}, children=[
        html.P("PLEASE FILL OUT THE FOLLOWING DETAILS", style={
               'color': 'rgb(0, 255, 156)', 'font-size': 'x-large'}),
        html.Div(className='app-controls-block', children=[
            html.P("Age"),
            dcc.Input(
                className='app-input',
                id='age',
                type='numer',
                min=18,
                step=1
            ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("Gender", ),
            dcc.Dropdown(id='genderdrop',
                         options=gender_options,
                         ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("Height (Inches)"),
            dcc.Input(
                className='app-input',
                id='height',
                type='number',
                min=0,
                step=0.1
            ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("High BP level", ),
            dcc.Input(
                className='app-input',
                id='highbp',
                type='number',
                min=0,
                step=0.1
            ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("Low BP level", ),
            dcc.Input(
                className='app-input',
                id='lowbp',
                type='number',
                min=0,
                step=0.1
            ),
        ]), ]),
        html.Div(className='HeartBeat', style={'top': '50%'}, children=[
            html.Div(className='app-controls-block', children=[
                html.P("Weight (Pounds)"),
                dcc.Input(
                    className='app-input',
                    id='weight',
                    type='number',
                    min=0,
                    step=0.1
                ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Do you Smoke?", ),
                dcc.Dropdown(id='smoke',
                             options=yes_no_options,
                             ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Do you Drink?", ),
                dcc.Dropdown(id='drink',
                             options=yes_no_options,
                             ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Do you Exercise Regularly?", ),
                dcc.Dropdown(id='exercise',
                             options=yes_no_options,
                             ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Cholestrol level", ),
                dcc.Input(
                    className='app-input',
                    id='cholestrol',
                    type='number',
                    min=0,
                    step=0.1
                ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Glucose level", ),
                dcc.Input(
                    className='app-input',
                    id='glucose',
                    type='number',
                    min=0,
                    step=0.1
                ),
            ]),
        ]),
        html.Div(className='app-controls-block', children=html.Div(className='outer', children=[
            html.Div(className='inner'), html.Div(
                className="Number", id="predict_full", children=[])
        ]
        )),
        dcc.Link(html.Button("Show General Stats", style={
                 'width': '22%', 'margin-left': '70%', 'margin-top': '2%'}), href="/page2"),
    ]))


@callback(
    Output(component_id='predict_full', component_property='children'),
    [Input('age', 'value'),
        Input('genderdrop', 'value'),
        Input('height', 'value'),
        Input('weight', 'value'),
        Input('smoke', 'value'),
        Input('drink', 'value'),
        Input('exercise', 'value'),
        Input('highbp', 'value'),
        Input('lowbp', 'value'),
        Input('glucose', 'value'),
        Input('cholestrol', 'value')
     ])
def predict(
        age=None, gender=None, height=None, weight=None, smoke=None,
        drink=None, exercise=None, highbp=None, lowbp=None,
        glucose=None, cholestrol=None
):
    height = _convert_imp_metr_height(height)
    weight = _convert_imp_metr_weight(weight)

    model_params = [
        gender, height, weight, highbp, lowbp,cholestrol,glucose,smoke, drink, exercise, age
    ]
    
    if any(map(lambda param: param is None, model_params)):
        result = [[0, 0]]
    else:
        with open('models/full_finalized_model.sav', 'rb') as model_file:
            model = pickle.load(model_file)

        model_params = [
        gender, height, weight, highbp, lowbp, int(smoke),int(drink), int(exercise), age,
        int(cholestrol=='1'),int(cholestrol=='2'),
        int(cholestrol=='3'),int(glucose=='1'),int(glucose=='2'),int(glucose=='3')
    ]
        result = model.predict_proba([model_params])

    return f'{round(result[0][1]*100, 2)}%'
