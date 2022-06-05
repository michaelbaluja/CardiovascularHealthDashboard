from dash import dcc, html, Input, Output, callback
from utils.defaults import gender_options
from utils.validation import _convert_imp_metr_height, _convert_imp_metr_weight
import pickle
yes_no_options = {0: 'Yes', 1: 'No'}
yes_no_option_exercise = {1: 'Yes', 0: 'No'}

header_style = {
    'padding': '25px',
    'text-align': 'center',
    'background': '#1abc9c',
    'color': 'white',
    'font-size': 'xx-large',
}
disclaimer_style = {
    'position': 'absolute',
    'width': '36%',
    'height': '10%',
    'opacity': '0.9',
    'left': '58%'
}

disclaimer_text = 'We do not claim to be medical professionals.\n Please consult your healthcare supervisor before \n taking action on any advice or results.'

layout = html.Div(
    children=html.Div(
        children=[
            html.H1('Risk Evaluator - General', style=header_style),
            html.Div(
                className='disclaimer-2',
                children=[html.P(disclaimer_text, style=disclaimer_style)]
            ),
            html.Div(
                className='HeartBeat',
                style={'top': '56%', 'left': '8%'},
                children=[
                    html.Div(
                        className='app-controls-block1',
                        children=[
                            html.P("Age"),
                            dcc.Input(
                                className='app-input',
                                id='age',
                                type='number',
                                min=18,
                                step=1
                            ),
                        ]
                    ),
                    html.Div(
                        className='app-controls-block1',
                        children=[
                            html.P('Gender', ),
                            dcc.Dropdown(
                                id='genderdrop',
                                options=gender_options,
                            ),
                        ]
                    ),
                    html.Div(
                        className='app-controls-block1',
                        children=[
                            html.P('Height (Inches)'),
                            dcc.Input(
                                className='app-input',
                                id='height',
                                type='number',
                                min=0,
                                step=1
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                className='HeartBeat',
                style={'top': '57.5%', 'left': '32%'},
                children=[
                    html.Div(
                        className='app-controls-block1',
                        children=[
                            html.P('Weight (Pounds)'),
                            dcc.Input(
                                className='app-input',
                                id='weight',
                                type='number',
                                min=0,
                                step=1
                            ),
                        ]
                    ),
                    html.Div(
                        className='app-controls-block1',
                        children=[
                            html.P('Do you Smoke?', ),
                            dcc.Dropdown(
                                id='smoke',
                                options=yes_no_options,
                            ),
                        ]
                    ),
                    html.Div(
                        className='app-controls-block1',
                        children=[
                            html.P('Do you Drink?', ),
                            dcc.Dropdown(
                                id='drink',
                                options=yes_no_options,
                            ),
                        ]
                    ),
                    html.Div(
                        className='app-controls-block1',
                        children=[
                            html.P('Do you Exercise Regularly?', ),
                            dcc.Dropdown(
                                id='exercise',
                                options=yes_no_option_exercise,
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                children=html.Div(
                    style={'left': '59%'},
                    className='outer',
                    children=[
                        html.Div(className='inner'),
                        html.Div(className='Number', id='predict', children=[])
                    ]
                )
            ),
            dcc.Link(
                html.Button(
                    'Show General Stats',
                    style={
                        'width': '22%',
                        'margin-left': '62.5%',
                        'margin-top': '1%'
                    }
                ),
                href='/page2'
            ),
        ]
    )
)


@callback(
    Output(component_id='predict', component_property='children'),
    [
        Input('age', 'value'),
        Input('genderdrop', 'value'),
        Input('height', 'value'),
        Input('weight', 'value'),
        Input('smoke', 'value'),
        Input('drink', 'value'),
        Input('exercise', 'value'),
    ]
)
def predict(
        age=None,
        gender=None,
        height=None,
        weight=None,
        smoke=None,
        drink=None,
        exercise=None
):
    """Predict probability of heart failure via low-data model.

    Parameters
    ----------
    age : int, optional (default=None)
    gender : {'male', 'female'}, optional (default=None)
    height : float, optional (default=None)
        Height in inches.
    weight : float, optional (default=None)
        Weight in pounds.
    smoke : bool, optional (default=None)
        Binary indicator for smoking.
    drink : bool, optional (default=None)
        Binary indicator for drinking.
    exercise : bool, optional (default=None)
        Binary indicator for exercising.

    Returns
    -------
    str
        Percent prediction of heart complication via low-data model.
    """

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
        model_params = [
            int(gender),
            height, weight,
            int(smoke),
            int(drink),
            int(exercise),
            age
        ]
        result = model.predict_proba([model_params])
        print(result)

    return f'{round(result[0][1]*100, 2)}%'
