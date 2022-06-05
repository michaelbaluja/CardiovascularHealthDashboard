from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import itertools

app = Dash(__name__)

data = pd.read_csv("kaggle_cleaned.csv")[
    ['smoke', 'gender', 'alco', 'active', 'cardio']]
# This only uses the columns ['smoke', 'gender', 'alco', 'active', 'cardio'] from the kaggle_cleaned.csv

app.layout = html.Div(children=[
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(['smoke', 'gender', 'alco', 'active'],
                 ['gender'],
                 multi=True,
                 id='select-columns'
                 ),

    dcc.Graph(
        id='grouped-plot',
    )
])


@app.callback(
    Output('grouped-plot', 'figure'),
    Input('select-columns', 'value')
)
def changing_plot(cols):
    """Plot that changes based on the user input.
    """
    if len(cols) == 1:
        return px.bar(data.groupby(by=cols).mean(), y="cardio")

    elif len(cols) > 1:
        # Plotly doesn't like multiindex so this is a hacky way of converting every multi index into a tupple and then assigning the value of the groupby() to it.
        counts = {}
        unique_combs = data[cols[0]].unique().tolist()
        unique_combs = [j for j in itertools.product(
            unique_combs, data[cols[1]].unique().tolist())]
        if len(cols) > 2:
            for i in range(2, len(cols)):
                unique_combs = [
                    j[0]+(j[1],) for j in itertools.product(unique_combs, data[cols[i]].unique().tolist())]
        for i in unique_combs:
            counts[i] = data.groupby(by=cols).mean()['cardio'].loc[i]
        output = pd.DataFrame(counts.values(), index=[
                              f"{i}" for i in counts.keys()])
        print(data.groupby(by=cols).mean())
        return px.bar(output)

    return {"layout": {
        "xaxis": {
            "visible":
            False
        },
        "yaxis": {
            "visible":
            False
        },
        "annotations": [{
            "text":
                        "Please select some columns.",
                        "showarrow":
                        False,
                        "font": {
                            "size": 28
                        }
                        }]
    }}


if __name__ == '__main__':
    app.run_server(debug=True)
