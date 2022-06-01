from dash import dcc, html, Input, Output, callback
from utils.defaults import gender_options, yes_no_options
from utils.validation import _convert_imp_metr_height, _convert_imp_metr_weight
import pickle


layout = html.Div(

    children=html.Div(children=[html.Div(className='HeartBeat', style={'top': '38%', 'left': '20%'}, children=[
        html.P("PLEASE FILL OUT THE FOLLOWING DETAILS", style={
               'color': 'rgb(0, 255, 156)', 'font-size': 'x-large'}),
        html.Div(className='app-controls-block', children=[
            html.P("Age"),
            dcc.Input(
                className='app-input',
                id='age',
                type='number',
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
        ]), ]),
        html.Div(className='HeartBeat', style={'top': '40%'}, children=[
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
        ]),



        html.Div(className='app-controls-block', children=html.Div(className='outer', children=[
            html.Div(className='inner'), html.Div(
                className="Number", id="predict", children=[])
        ]
        )),
        dcc.Link(html.Button("Show General Stats", style={
                 'width': '22%', 'margin-left': '36%', 'margin-top': '2%'}), href="/page2"),
    ]))


@callback(
    Output(component_id='predict', component_property='children'),
    [Input('age', 'value'),
        Input('genderdrop', 'value'),
        Input('height', 'value'),
        Input('weight', 'value'),
        Input('smoke', 'value'),
        Input('drink', 'value'),
        Input('exercise', 'value'),
     ])
def predict(
        age=None, gender=None, height=None, weight=None,
        smoke=None, drink=None, exercise=None
):
    # Convert imperial height and weight to metric height and weight
    try:
        height = _convert_imp_metr_height(height)
        weight = _convert_imp_metr_weight(weight)
    except TypeError:
        print(height, weight)

    model_params = [gender, height, weight, smoke, drink, exercise, age]

    if any(map(lambda param: param is None, model_params)):
        result = [[0, 0]]
    else:
        with open('models/half_finalized_model.sav', 'rb') as model_file:
            model = pickle.load(model_file)
        result = model.predict_proba([model_params])

    return f'{round(result[0][1]*100, 2)}%'
