from dash import html

from .. import app


def test_display_page0():
    page = app.display_page('/page0')
    assert isinstance(page, html.Div)
