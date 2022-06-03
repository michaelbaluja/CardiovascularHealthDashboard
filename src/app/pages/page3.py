from dash import dcc, html, Input, Output, callback
import pickle
from utils.defaults import gender_options, yes_no_options
from utils.validation import _convert_imp_metr_height, _convert_imp_metr_weight


layout = html.Div(
   
    children=html.Div(children=[html.H1("Heart Disease Risk Prediction Model",style={'margin-left': '23%'}),
    
        
        html.Div(className='HeartBeat', style={'top': '56%', 'left': '20%'}, children=[
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
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("High BP level", ),
            dcc.Input(
                className='app-input',
                id='highbp',
                type='number',
                min=50,
                step=1
            ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("Low BP level", ),
            dcc.Input(
                className='app-input',
                id='lowbp',
                type='number',
                min=20,
                step=1
            ),
        ]),
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
             ]),
        html.Div(className='HeartBeat', style={'top': '50%'}, children=[
            
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
                dcc.Dropdown(id='cholestrol',
                            options=['Normal (<200mg/dL)','Above Normal (200~239mg/dL)','Well Above Normal (>240mg/dL)'],
                            ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Glucose level", ),
                dcc.Dropdown(
                    className='app-input',
                    id='glucose',
                    options=['Normal (<99mg/dL)', 'Above Normal (100~125mg/dL)','Well Above Normal (>126mg/dL)']
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
        int(gender), height, weight, float(highbp), float(lowbp), int(smoke),int(drink), int(exercise), age,
        int(cholestrol=='Normal (<200mg/dL)'),int(cholestrol=='Above Normal (200~239mg/dL)'),
        int(cholestrol=='Well Above Normal (>240mg/dL)'),int(glucose=='Normal (<99mg/dL)',),
        int(glucose=='Above Normal (100~125mg/dL)'),int(glucose=='Well Above Normal (>126mg/dL)')
    ]
        print(model_params)
        result = model.predict_proba([model_params])

    return f'{round(result[0][1]*100, 2)}%'
