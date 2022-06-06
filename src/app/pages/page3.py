import pickle

from dash import Input, Output, callback, dcc, html
from utils import data_options, disclaimer
from utils.validation import _convert_imp_metr_height, _convert_imp_metr_weight

header_style = {
    "padding": "25px",
    "text-align": "center",
    "background": "#1abc9c",
    "color": "white",
    "font-size": "xx-large",
}

div_className = 'app-controls-block'

layout = html.Div(
    children=html.Div(
        children=[
            html.H1("Risk Evaluator - Detailed", style=header_style),
            html.Div(
                children=[
                    html.P(
                        disclaimer.disclaimer_text,
                        style=disclaimer.disclaimer_style
                    )
                ]
            ),
            html.Div(
                className='HeartBeat',
                style={'top': '61%', 'left': '8%'},
                children=[
                    data_options.user_age(div_className),
                    data_options.user_gender(div_className),
                    data_options.user_height(div_className),
                    data_options.user_weight(div_className)
                ]
            ),
            html.Div(
                className='HeartBeat',
                style={'top': '61%', 'left': '33%'},
                children=[
                    data_options.user_smoke(div_className),
                    data_options.user_drink(div_className),
                    data_options.user_low_bp(div_className),
                    data_options.user_high_bp(div_className)
                ]
            ),
            html.Div(
                className='HeartBeat',
                style={'top': '49%', 'left': '53%'},
                children=[
                    data_options.user_exercise(div_className),
                    data_options.user_cholesterol(div_className),
                    data_options.user_glucose(div_className)
                ]
            ),
            html.Div(
                children=html.Div(
                    className='outer',
                    children=[
                        html.Div(className='inner'),
                        html.Div(
                            className="Number",
                            id="predict_full",
                            children=[]
                        )
                    ]
                )
            ),
            dcc.Link(
                html.Button(
                    "Show General Stats",
                    style={
                        'width': '22%',
                        'margin-left': '70%',
                        'margin-top': '2%'
                    }
                ),
                href="/page2"
            ),
        ]
    )
)


@callback(
    Output(component_id='predict_full', component_property='children'),
    [
        Input('age', 'value'),
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
    ]
)
def predict(
        age=None,
        gender=None,
        height=None,
        weight=None,
        smoke=None,
        drink=None,
        exercise=None,
        highbp=None,
        lowbp=None,
        glucose=None,
        cholestrol=None
):
    """Predict probability of heart failure via high-data model.

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
    highbp : int in [50, 100]
        High blood pressure level.
    lowbp : int in [20, 80], optional (default=None)
        Low blood pressure level.
    glucose : {
            'Normal(<99mg/dL)',
            'Above Normal(100~125mg/dL)',
            'Abnormal (>126mg/dL)'
    }
        Glucose level.
    cholestrol : {
            'Normal(<200mg/dL)',
            'Above Normal(200~239mg/dL)',
            'Abnormal(>240mg/dL)'
    }
        Cholesterol level.

    Returns
    -------
    str
        Percent prediction of heart complication via high-data model.
    """

    height = _convert_imp_metr_height(height)
    weight = _convert_imp_metr_weight(weight)

    model_params = [
        gender, height, weight, highbp, lowbp, cholestrol, glucose, smoke,
        drink, exercise, age
    ]

    if any(map(lambda param: param is None, model_params)):
        result = [[0, 0]]
    else:
        with open('models/full_finalized_model.sav', 'rb') as model_file:
            model = pickle.load(model_file)

        model_params = [
            int(gender), height, weight, float(highbp), float(
                lowbp), int(smoke), int(drink), int(exercise), age,
            int(cholestrol == 'Normal(<200mg/dL)'), int(cholestrol ==
                                                        'Above Normal(200~239mg/dL)'),
            int(cholestrol == 'Abnormal(>240mg/dL)'), int(glucose ==
                                                          'Normal(<99mg/dL)',),
            int(glucose == 'Above Normal(100~125mg/dL)'), int(glucose ==
                                                              'Abnormal(>126mg/dL)')
        ]
        print(model_params)
        result = model.predict_proba([model_params])

    return f'{round(result[0][1]*100, 2)}%'
