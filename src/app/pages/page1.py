import pickle

from dash import Input, Output, callback, dcc, html
from src.app.utils import data_options, disclaimer, validation

header_style = {
    'padding': '25px',
    'text-align': 'center',
    'background': '#1abc9c',
    'color': 'white',
    'font-size': 'xx-large',
}


div_className = 'app-controls-block1'

layout = html.Div(
    children=html.Div(
        children=[
            html.H1('Risk Evaluator - General', style=header_style),
            html.Div(
                className='disclaimer-2',
                children=[
                    html.P(
                        disclaimer.disclaimer_text,
                        style=disclaimer.disclaimer_style
                    )
                ]
            ),
            html.Div(
                className='HeartBeat',
                style={'top': '56%', 'left': '8%'},
                children=[
                    data_options.user_age(div_className),
                    data_options.user_gender(div_className),
                    data_options.user_height(div_className)
                ]
            ),
            html.Div(
                className='HeartBeat',
                style={'top': '57.5%', 'left': '32%'},
                children=[
                    data_options.user_weight(div_className),
                    data_options.user_smoke(div_className),
                    data_options.user_drink(div_className),
                    data_options.user_exercise(div_className)
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
        height = validation._convert_imp_metr_height(height)
        weight = validation._convert_imp_metr_weight(weight)
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
