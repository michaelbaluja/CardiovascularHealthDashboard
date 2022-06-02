import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2

# from dash import Dash, html, dcc, Input, Output
# import plotly.express as px

CATEGORICAL_COLUMNS = ['gender', 'cholesterol', 'smoke', 'alcohol', 'active']

def get_categorical_table()-> pd.DataFrame:
    """Returns a section of the table with categorical variables only

    Returns
    -------
    pandas.DataFrame
    """
    # read the kaggle dataset
    df = pd.read_csv('../data/kaggle_cleaned.csv')
    return df[[*CATEGORICAL_COLUMNS, 'cardio']]

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

# print(compute_importance(['smoke', 'alcohol', 'gender'], 'cardio'))
# app = Dash(__name__)
# # data = pd.read_csv("kaggle_cleaned.csv").drop(columns=['id', 'Unnamed: 0.1', 'Unnamed: 0']).corr()['cardio']
# # print(data.drop('cardio').index.tolist())

# app.layout = html.Div(children=[
#     html.Label('Select Risk Factors'),
#     dcc.Dropdown(get_dropdown_options(),
#                     multi=True,
#                     id='corr-factors'
#                 ),
#     dcc.Graph(
#         id='corr-plot',
#     )
# ])

# @app.callback(
#     Output('corr-plot', 'figure'),
#     Input('corr-factors', 'value')
# )
# def correlation_plot(cols):
#     """Correlation between the selected factors and cardiovascular disease risk.
#     """
#     return px.bar(x=cols, y=compute_importance(cols), title='Correlation',
#         labels={'x': 'Risk Factors', 'y':'Correlation'}, width=500)

# if __name__ == '__main__':
#     app.run_server(debug=True)