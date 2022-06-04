from dash import dcc, html, Input, Output, callback
import pickle
from utils.defaults import gender_options
from utils.validation import _convert_imp_metr_height, _convert_imp_metr_weight
yes_no_options = {0: 'Yes',1: 'No'}
yes_no_option_exercise={1:'Yes',0:'No'}
header_style = {
  "padding": "25px",
  "text-align": "center",
  "background": "#1abc9c",
  "color": "white",
  "font-size": "xx-large",
}

disclaimer_text = "We do not claim to be medical professionals. Please consult your healthcare supervisor before taking action on any advice or results."

disclaimer_style = {
          'position': 'absolute',
    'width': '36%',
    'height': '10%',
    'opacity': '0.9',
    'left': '64%'
}

layout = html.Div(
    children=html.Div(children=[html.H1("Risk Evaluator - Detailed", style=header_style),
        html.Div(children=[html.P(disclaimer_text, style=disclaimer_style)]),
        html.Div(className='HeartBeat', style={'top': '61%', 'left': '8%'}, children=[
        
        
        html.Div(className='app-controls-block', children=[
            html.P("Age"),
            dcc.Input(
                className='app-input',
                id='age',
                type='number',
                min=18,
                step=1,
                value=22
            ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("Gender", ),
            dcc.Dropdown(id='genderdrop',
                         options=gender_options,
                         value='1'
                         ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("Height (Inches)"),
            dcc.Input(
                className='app-input',
                id='height',
                type='number',
                min=0,
                step=0.1,
                value=70
            ),
        ]),
        html.Div(className='app-controls-block', children=[
                html.P("Weight (Pounds)"),
                dcc.Input(
                    className='app-input',
                    id='weight',
                    type='number',
                    min=0,
                    step=1,
                    value=170
                ),
            ]),
        
        
             ]),

        html.Div(className='HeartBeat', style={'top': '61%','left':'33%'}, children=[
            
            html.Div(className='app-controls-block', children=[
                html.P("Do you Smoke?", ),
                dcc.Dropdown(id='smoke',
                             options=yes_no_options,
                             value='1'
                             ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Do you Drink?", ),
                dcc.Dropdown(id='drink',
                             options=yes_no_options,
                             value='1'
                             ),
            ]),
            html.Div(className='app-controls-block', children=[
            html.P("Low BP level", ),
            dcc.Input(
                className='app-input',
                id='lowbp',
                type='number',
                min=20,
                step=1,
                value=80
            ),
        ]),
        html.Div(className='app-controls-block', children=[
            html.P("High BP level", ),
            dcc.Input(
                className='app-input',
                id='highbp',
                type='number',
                min=50,
                step=1,
                value=100
            ),
        ]),


        ]),
        html.Div(className='HeartBeat', style={'top': '49%','left':'53%'}, children=[
            
            
            html.Div(className='app-controls-block', children=[
                html.P("Do you Exercise Regularly?", ),
                dcc.Dropdown(id='exercise',
                             options=yes_no_option_exercise,
                             value='1'
                             ),
            ]),

            html.Div(className='app-controls-block', children=[
                html.P("Cholestrol level", ),
                dcc.Dropdown(id='cholestrol',
                            options=['Normal(<200mg/dL)','Above Normal(200~239mg/dL)','Abnormal(>240mg/dL)'],
                            value='Normal(<200mg/dL)'
                            ),
            ]),
            html.Div(className='app-controls-block', children=[
                html.P("Glucose level", ),
                dcc.Dropdown(
                    className='app-input',
                    id='glucose',
                    options=['Normal(<99mg/dL)', 'Above Normal(100~125mg/dL)','Abnormal (>126mg/dL)'],
                    value='Normal(<99mg/dL)'
                ),
            ]),
        ]),
        html.Div(children=html.Div(className='outer', children=[
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
        int(cholestrol=='Normal(<200mg/dL)'),int(cholestrol=='Above Normal(200~239mg/dL)'),
        int(cholestrol=='Abnormal(>240mg/dL)'),int(glucose=='Normal(<99mg/dL)',),
        int(glucose=='Above Normal(100~125mg/dL)'),int(glucose=='Abnormal(>126mg/dL)')
    ]
        print(model_params)
        result = model.predict_proba([model_params])

    return f'{round(result[0][1]*100, 2)}%'
