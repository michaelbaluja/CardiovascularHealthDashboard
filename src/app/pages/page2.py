from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
import plotly.graph_objects as go
from sklearn.feature_selection import SelectKBest, chi2

header_style = {
    "padding": "25px",
    "text-align": "center",
    "background": "#1abc9c",
    "color": "white",
    "font-size": "xx-large",
}

app = Dash(__name__)
# 1

CATEGORICAL_COLUMNS = ['gender', 'High cholesterol',
                       'smoke', 'alco', 'active', 'High glucose']


def get_categorical_table() -> pd.DataFrame:
    """Returns a section of the table with categorical variables only
    Returns
    -------
    pandas.DataFrame
    """

    # read the kaggle dataset
    df = pd.read_csv('../../data/kaggle_cleaned.csv')
    dummies = pd.get_dummies(df['cholesterol'], prefix='cholesterol')
    res = pd.concat([df, dummies], axis=1)
    res = res.drop(['cholesterol', 'cholesterol_1', 'cholesterol_3'], axis=1)
    res = res.rename(columns={"cholesterol_2": "High cholesterol"})
    dummies = pd.get_dummies(df['gluc'], prefix='gluc')
    res = pd.concat([res, dummies], axis=1)
    res = res.drop(['gluc', 'gluc_1', 'gluc_3'], axis=1)
    res = res.rename(columns={"gluc_2": "High glucose"})
    return res[[*CATEGORICAL_COLUMNS, 'cardio']]


df = get_categorical_table()


def get_dropdown_options():
    """Returns all the varibles to populate the dropdown
    Returns
    -------
    list(str)
    """
    return CATEGORICAL_COLUMNS


def compute_importance(x_vars) -> list:
    """Computes the importance score using the chi-squared statistic
    Input
    -------
    x_vars : list of fields for which the importance is computed
    y : Dependent variable
    Returns
    -------
    list: importance scores for each x with respect to y
    """
    assert isinstance(x_vars, list)
    assert all([(isinstance(x, str) and x in df.columns) for x in x_vars])

    x_df = df[[*x_vars]]
    y_ds = df['cardio']

    fs = SelectKBest(score_func=chi2, k='all')
    fs.fit(x_df, y_ds)
    return fs.scores_


# 2
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# data
dataset1 = pd.read_csv("../../data/Kagglecleaned3.csv")
dataset1.loc[dataset1['cardio'] == 0, 'cardio'] = 'No heart condition'
dataset1.loc[dataset1['cardio'] == 1, 'cardio'] = 'Heart condition'
dataset1.rename(columns={'ap_hi': 'systolic pressure',
                'ap_lo': 'diastolic pressure'}, inplace=True)
dataset1.loc[dataset1['active'] == 0, 'active'] = 'Regular Exercise'
dataset1.loc[dataset1['active'] == 1, 'active'] = 'Lack of Exercise'

dataset2 = pd.read_csv('../../data/kaggle_cleaned.csv')  # for easy use
dataset2.loc[dataset2['cardio'] == 0, 'cardio'] = 'No heart condition'
dataset2.loc[dataset2['cardio'] == 1, 'cardio'] = 'Heart condition'
dataset2.loc[dataset2['cholesterol'] == 1,
             'cholesterol'] = 'Normal (<200mg/dL)'
dataset2.loc[dataset2['cholesterol'] == 2,
             'cholesterol'] = 'Above Normal (200~239mg/dL)'
dataset2.loc[dataset2['cholesterol'] == 3,
             'cholesterol'] = 'Well Above Normal (>240mg/dL)'
dataset2.loc[dataset2['gluc'] == 1, 'gluc'] = 'Normal (<99mg/dL)'
dataset2.loc[dataset2['gluc'] == 2, 'gluc'] = 'Above Normal (100~125mg/dL)'
dataset2.loc[dataset2['gluc'] == 3, 'gluc'] = 'Well Above Normal (>126mg/dL)'
dataset2.rename(columns={'gluc': 'Glucose Level'}, inplace=True)

# figure for high blood pressure
fig1 = px.box(dataset1, y='systolic pressure', x='cardio', color='cardio')
fig2 = px.box(dataset1, y='diastolic pressure', x='cardio', color='cardio')

# figure for Smoking (data from heart_2020_cleaned.csv, the other dataset does not show significant relationship on smoking, weird)
fig3 = go.Figure(data=[go.Table(header=dict(values=['', 'Heart condition', 'No heart condition']),
                 cells=dict(values=[['Smoker', 'Non-Smoker'], [16037, 11336], [115871, 176551]]))])

# figure for cholesterol
fig4 = px.histogram(dataset2, x='cardio', color="cholesterol", barmode='group')

# fig for high glucolse
fig5 = px.histogram(dataset2, x='cardio',
                    color="Glucose Level", barmode='group')
# fig for Inactivity
fig6 = px.histogram(dataset1, x='cardio', color="active", barmode='group')
# fig for Obsease
dataset1['BMI'] = dataset1['weight']/(dataset1['height']**2)*10000
dataset1 = dataset1[dataset1['BMI'] < 50]
fig7 = px.box(dataset1, y='BMI', x='cardio', color='cardio')


risk_suggestions = {
    'Diabetes': html.Div(
        children=[
            html.Div(dcc.Graph(figure=fig5), className='graphs'),
            html.Div(
                className='writings',
                children=[
                    html.P(
                        [
                            '''If you have diabetes, you’re twice as likely to have heart disease or a
                            stroke than someone who doesn’t have diabetes. Diabetes also causes some other risk factors such as blood pressure 
                            to rise. People diagnosed with type 1 diabetes also require regular insulin injections for the 
                            rest of their life. As type 2 diabetes is a progressive condition, medicine may eventually be required, 
                            usually in the form of tablets.'''
                        ]
                    ),
                    html.Br(),
                    html.P(
                        [
                            'To reduce the risk of diabetes you could:', html.Br(),
                            '· Follow a balanced diet', html.Br(),
                            '· Exercise regularly', html.Br(),
                            '· Check your blood sugar levels regularly', html.Br()
                        ]
                    ),
                    html.P(
                        [
                            'Useful Links',
                            html.Br(),
                            html.A(
                                'https://www.cdc.gov/diabetes/library/features/diabetes-and-heart.html',
                                href='https://www.cdc.gov/diabetes/library/features/diabetes-and-heart.html',
                                target='_blank'
                            ),
                            html.Br(),
                            html.A(
                                'https://www.diabetes.org/diabetes/cardiovascular-disease',
                                href='https://www.diabetes.org/diabetes/cardiovascular-disease',
                                target='_blank'
                            ),
                            html.Br(),
                        ]
                    ),
                ]
            )
        ]
    ),
    'High blood Pressure': html.Div(
        children=[
            html.Div(
                className='graphs',
                children=[
                    dcc.Graph(figure=fig1),
                    dcc.Graph(figure=fig2)
                ]
            ),
            html.Div(
                className='writings',
                children=[
                    html.P(
                        [
                            '''Among the risk factors for cardiovascular diseases (CVD), high blood pressure is the most prevalent 
                            and has the highest causation. The ideal blood pressure is usually considered to be between 90/60mmHg and 120/80mmHg. 
                            Blood pressure readings between 120/80mmHg and 140/90mmHg could mean you're at risk of developing high blood pressure 
                            if you do not take steps to keep it under control. Blood pressure readings above 140/90mmHg are considered high 
                            blood pressure.'''
                        ]
                    ),
                    html.P(
                        [
                            'If you have high blood pressure you could', html.Br(),
                            '· Reduce salt intake in your diet', html.Br(),
                            "· Exercise regularly for at least 20-30 minutes a day", html.Br(),
                            "· Cut down on caffeine", html.Br(),
                            "· Quit smoking"
                        ]
                    ),
                    html.P(
                        [
                            'Useful Links', html.Br(),
                            html.A(
                                "https://www.cdc.gov/bloodpressure/prevent.html'",
                                href='https://www.cdc.gov/bloodpressure/prevent.html',
                                target="_blank"
                            ),
                            html.Br(),
                            html.A(
                                "https://www.cdc.gov/bloodpressure/index.htm",
                                href='https://www.cdc.gov/bloodpressure/index.htm',
                                target="_blank"
                            ),
                            html.Br(),
                        ]
                    ),
                ]
            ),
        ]
    ),
    'Smoking': html.Div(
        children=[
            html.Div(
                dcc.Graph(figure=fig3),
                className='graphs'
            ),
            html.Div(
                className='writings',
                children=[
                    html.P(
                        [
                            '''Smoking is a major cause of cardiovascular diseases (CVD) and causes approximately one of every four deaths 
                            related to heart issues. The risk of CVD increases with the number of cigarettes smoked per day, and when smoking continues 
                            for many years. Smoking cigarettes with lower levels of tar or nicotine does not reduce the risk for cardiovascular disease.'''
                        ]
                    ),
                    html.P(
                        [
                            'From the data, the odds-ratio = 2.16. Smoking siginificantly increases the probability of getting a heart disease.'
                        ]
                    ),
                    html.P(
                        [
                            'If you want to quit smoking you could - ', html.Br(),
                            '· Use Nicotine Replacement Therapy (NRT)', html.Br(
                            ),
                            "· Talk to your Healthcare Provider About Using a Pill Prescription Medication", html.Br(),
                            "· Seek counseling to make a plan to quit smoking and help with withdrawal symptoms", html.Br()
                        ]
                    ),
                    html.P(
                        [
                            'Useful Links', html.Br(),
                            html.A(
                                "https://www.cdc.gov/tobacco/data_statistics/sgr/50th-anniversary/pdfs/fs_smoking_CVD_508.pdf",
                                href='https://www.cdc.gov/tobacco/data_statistics/sgr/50th-anniversary/pdfs/fs_smoking_CVD_508.pdf',
                                target="_blank"
                            ),
                            html.Br(),
                            html.A(
                                "https://www.cdc.gov/tobacco/quit_smoking/index.htm",
                                href='https://www.cdc.gov/tobacco/quit_smoking/index.htm',
                                target="_blank"
                            ),
                            html.Br(),
                        ]
                    ),
                ]
            ),
        ]
    ),
    'High Cholesterol': html.Div(
        children=[
            html.Div(dcc.Graph(figure=fig4), className='graphs'),
            html.Div(
                className='writings',
                children=[
                    html.P(
                        [
                            '''About 38% of American adults have high cholesterol 
                            (total blood cholesterol ≥ 200 mg/dL). Cholesterol is a fatty substance found in the blood. High values of 
                            cholesterol can block your blood vessels. It makes you more likely to have heart problems or a stroke.'''
                        ]
                    ),
                    html.P(
                        [
                            'To reduce your cholesterol you could -', html.Br(),
                            '· Increase physical activity', html.Br(),
                            "· Limit alcohol consumption", html.Br(),
                            "· Consult a physician and dietician", html.Br()
                        ]
                    ),
                    html.P(
                        [
                            'Useful Links', html.Br(),
                            html.A(
                                "https://www.cdc.gov/dhdsp/data_statistics/fact_sheets/fs_state_cholesterol.htm",
                                href='https://www.cdc.gov/dhdsp/data_statistics/fact_sheets/fs_state_cholesterol.htm',
                                target="_blank"
                            ),
                            html.Br(),
                            html.A(
                                "https://www.cdc.gov/cholesterol/prevention.htm",
                                href='https://www.cdc.gov/cholesterol/prevention.htm',
                                target="_blank"
                            ),
                            html.Br(),
                        ]
                    ),
                ]
            )
        ]
    ),
    'Inactivity': html.Div(
        children=[
            html.Div(dcc.Graph(figure=fig6), className='graphs'),
            html.Div(
                className='writings',
                children=[
                    html.P(
                        [
                            '''Not getting enough physical activity can lead to heart 
                            disease—even for people who have no other risk factors. It can also increase the likelihood of developing other 
                            heart disease risk factors. '''
                        ]
                    )
                ]
            ),
            html.P(
                [
                    'If you want to increase your physical activity, you could - ', html.Br(),
                    '· Walk whenever Possible', html.Br(),
                    "· Track daily physical activity and compete with yourself", html.Br(),
                    "· Take short breaks from work every hour and do some stretching", html.Br()
                ]
            ),
            html.P(
                [
                    'Useful Links', html.Br(),
                    html.A(
                        "Link to CDC Resource",
                        href='''https://www.cdc.gov/chronicdisease/resources/publications/factsheets/physical-activity.htm#:
                            ~:text=Not%20getting%20enough%20physical%20activity%20can%20lead%20to%20heart%20disease,cholesterol%2C%20a
                            nd%20type%202%20diabetes.''',
                        target="_blank"
                    ),
                    html.Br(),
                    html.A(
                        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4626000/",
                        href='https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4626000/',
                        target="_blank"
                    ),
                    html.Br(),
                ]
            ),
        ]
    ),
    'Obesity': html.Div(
        children=[
            html.Div(
                dcc.Graph(figure=fig7), className='graphs'),
            html.Div(
                className='writings',
                children=[
                    html.P(
                        [
                            'The best way to treat obesity is to eat a healthy reduced-calorie diet and exercise regularly.', html.Br(),
                            'To do this, you should:', html.Br(),
                            '· Eat a balanced calorie-controlled diet as recommended by a GP or weight loss management health professional (such as a dietitian).', html.Br(
                            ),
                            '· Take up activities such as fast walking, jogging or swimming for 150 to 300 minutes (2.5 to 5 hours) a week.', html.Br(
                            ),
                            '· You may also benefit from receiving psychological support from a trained healthcare professional to help change the way you think about food and eating.', html.Br(),
                            html.Br(),
                            html.P(
                                [
                                    'Useful Links', html.Br(),
                                    html.A(
                                        "https://www.cdc.gov/dhdsp/pubs/docs/sib_heartbeat.pdf",
                                        href='https://www.cdc.gov/dhdsp/pubs/docs/sib_heartbeat.pdf',
                                        target="_blank"
                                    ),
                                    html.Br(),
                                    html.A(
                                        "https://www.cdc.gov/obesity/index.html",
                                        href='https://www.cdc.gov/obesity/index.html',
                                        target="_blank"
                                    ),
                                    html.Br(),
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ]
    ),
}
# 3

layout = html.Div(
    children=[
        html.H1(
            "Risk Factor Analysis",
            style=header_style
        ),
        html.Div(
            style={'display': 'inline-flex', 'margin-top': '-1%'},
            children=[
                dcc.Link(
                    html.Button(
                        "Risk Factor Analysis",
                        style={
                            'width': '271%',
                            'margin-left': '0%',
                            'background':
                            'rgb(26, 188, 156)',
                            'color': 'white',
                            'border': 'rgb(26, 188, 156)',
                            'text-transform': 'Capitalize',
                            'font-family': ' "Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'
                        }
                    ),
                    href="/page2"
                ),
                dcc.Link(
                    html.Button(
                        "Location Visualizations",
                        style={
                            'width': '247%',
                            'margin-left': '154%',
                            'background': 'rgb(26, 188, 156)',
                            'color': 'white', 'border':
                            'rgb(26, 188, 156)',
                            'text-transform': 'Capitalize',
                            'font-family': ' "Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'
                        }
                    ),
                    href="/page4"
                ),
            ]
        ),
        # 1
        html.Br(),
        html.H3("Select Risk Factor", style={"margin-left": "15px"}),
        html.Div(
            [
                dcc.Dropdown(
                    id="risk_factors",
                    options=[
                        {"label": l.capitalize(), "value": l}
                        for l in risk_suggestions.keys()
                    ],
                    value='Diabetes',
                    style={"width": "200px", "margin-left": "7px"}
                ),
                html.Div(
                    style={
                        "margin-top": "3%",
                        "margin-bottom": "3%",
                        "margin-right": "3%",
                        "margin-left": "3%"
                    },
                    id='suggestions'
                ),
            ]
        ),
        html.Br(),
        # 2
        html.Div(
            children=[
                html.H3(
                    "Correlation Analysis",
                    style={"margin-left": "1%"}
                ),
                html.P(
                    "Understand the correlation between the risk factors and Cardiovasular diseases",
                    style={
                        "margin-top": "15px",
                        "margin-bottom": "3%",
                        "margin-right": "3%",
                        "margin-left": "3%"
                    }
                ),
                dcc.Dropdown(
                    get_dropdown_options(),
                    value=['alco', 'smoke'],
                    multi=True,
                    id='corr-factors',
                    style={
                        'width': '800px',
                        'margin-left': '2%'
                    }
                ),
                html.Div(
                    dcc.Graph(
                        id='corr-plot',
                    ),
                    className='graphs'
                ),
            ]
        ),
    ]
)
# 1


@callback(
    Output('corr-plot', 'figure'),
    Input('corr-factors', 'value')
)
def correlation_plot(cols):
    """Correlation between selected factors and cardiovascular disease risk."""

    return px.bar(
        x=cols,
        y=compute_importance(cols),
        title='Correlation',
        labels={'x': 'Risk Factors', 'y': 'Correlation'}
    )

# 2


@callback(
    Output('suggestions', 'children'),
    Input('risk_factors', 'value')
)
def give_suggestions(factors):
    return risk_suggestions[factors]


if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
