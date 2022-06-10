from dash import html

from src.app import data

from .. import app


class TestDisplayPages:
    def test_page0(self):
        page = app.display_page('/page0')
        assert isinstance(page, html.Div)

    def test_page1(self):
        page = app.display_page('/page1')
        assert isinstance(page, html.Div)

    def test_page2(self):
        page = app.display_page('/page2')
        assert isinstance(page, html.Div)

    def test_page3(self):
        page = app.display_page('/page3')
        assert isinstance(page, html.Div)

    def test_page4(self):
        page = app.display_page('/page4')
        assert isinstance(page, html.Div)

    def test_index(self):
        page = app.display_page(None)
        assert isinstance(page, html.Div)
