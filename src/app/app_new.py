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

description = "This dashboard aims to provide users with information about their current heart health condition with a personalized \
    risk assessment for users, keeping their privacy in mind. It provide visualizations analyzing the relationship between \
    several risk factors and cardiovascular diseases."

index_page =html.Div(children=[
                    #title
                    html.Div(className="app-header", children=[html.H1("Cardio Care")]),
                    #style={'margin-left': '12%','opacity':'70%'}),style={'background': 'rgb(0,255,156)','opacity':'38%',

                    #description
                    html.Div(html.H5(description),style={'width': '30%',' height':' 43%','margin-top': '6%','margin-left': '10%'}),

                    html.Br(),
                    html.Div(
                    children=[  
                        html.Div(style={'left':'67%', 'width':' 37%'},className="HeartBeat",children=[
                        html.Div(de.Lottie(options=options, url=url)),
                        dcc.Link(html.Button("Get Started",style={'width': '44%','margin-left': '29.25%'}), href="/page0", refresh=True),
                ])
])
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
