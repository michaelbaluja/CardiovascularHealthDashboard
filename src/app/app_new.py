from importlib.resources import path
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_extensions as de
from pages import page0,page1, page2, page3,page4



app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

url="https://assets8.lottiefiles.com/packages/lf20_zmf796.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

index_page =html.Div(className="HeartBeat",children=[
    html.Div(de.Lottie(options=options, url=url)),
    dcc.Link(html.Button("Predict my risk of Heart Disease"), href="/page0", refresh=True),
])


@callback(Output('page-content', 'children'),
              Input('url','pathname'))
def display_page(pathname):
    if pathname=='/page0':
        return page0.layout
    elif pathname == '/page1':
        return page1.layout
    elif pathname=='/page2':
       return page2.layout
    elif pathname=='/page3':
       return page3.layout
    elif pathname=='/page4':
        return page4.layout
    else:
        return index_page
    

if __name__ == '__main__':
    app.run_server(debug=True)
