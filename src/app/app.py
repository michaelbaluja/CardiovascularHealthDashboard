from layout_main import run_standalone_app
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc

def layout():
    return html.Div(
        id='test-container'
    )

def header_colors():
    return {
        'bg_color': '#2596be',
        'font_color': 'white'
    }

def callbacks(app):
    return

app = run_standalone_app(layout, callbacks, header_colors, __file__)
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=5006)