from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import itertools

app = Dash(__name__)
data = pd.read_csv("kaggle_cleaned.csv").drop(
    columns=['id', 'Unnamed: 0.1', 'Unnamed: 0']).corr()['cardio']
print(data.drop('cardio').index.tolist())

app.layout = html.Div(children=[
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(data.drop('cardio').index.tolist(),
                 ['gender'],
                 multi=True,
                 id='corr-factors'
                 ),

    dcc.Graph(
        id='corr-plot',
    )
])


@app.callback(
    Output('corr-plot', 'figure'),
    Input('corr-factors', 'value')
)
def correlation_plot(cols):
    """Correlation between the selected factors and cardiovascular disease risk.
    """
    return px.bar(data[cols])


if __name__ == '__main__':
    app.run_server(debug=True)
