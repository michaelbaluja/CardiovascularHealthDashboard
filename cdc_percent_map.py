from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

app = Dash(__name__)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
# Used for plotting. We can predownload the json if thats better ?

data2 = pd.read_csv(
    "data/trends_by_100k.csv").drop(columns=['Unnamed: 0', 'Low_Bound', 'Up_Bound', 'Year'])
data2['Topic'] = data2['Topic'].astype('string')
data2['Age'] = data2['Age'].astype('string')
data2['LocationID'] = data2['LocationID'].astype('string')
data2['LocationID'] = data2['LocationID'].apply((lambda x: x.zfill(5)))

app.layout = html.Div([
    html.H3("The map shows the number of people per 100k that have suffered either a Stroke or Coronary Heart Disease by county in the United States.\
        The two available age groups are 35-64 and 65+. The values are the annual average over the last 20 years."),
    # dcc.Slider(1999, 2018, 1,
    #            value=2008,
    #            id='year'
    # ),

    dcc.Dropdown(['Ages 35-64 years', 'Ages 65 years and older'],
                 'Ages 35-64 years',
                 id='age'
                 ),

    dcc.Dropdown(['Stroke', 'Coronary Heart Disease'],
                 'Stroke',
                 id='topic'
                 ),

    dcc.Graph(
        id='map',
    )
])


@app.callback(
    Output('map', 'figure'),
    Input('age', 'value'),
    Input('topic', 'value'),
)
def correlation_plot(age, topic):
    """Create a map using the three selected targets.
    """
    x = data2[data2['Topic'] == topic]
    x = x[x['Age'] == age]

    fig = px.choropleth(x, geojson=counties, locations='LocationID', color='Data_Value',
                        color_continuous_scale="Viridis",
                        range_color=(x['Data_Value'].min(),
                                     x['Data_Value'].max()),
                        scope="usa",
                        labels={
                            'Data_Value': 'cardiovascular disease per 100k pop.'},
                        hover_data=['County', 'State']
                        )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
