"""test_app.py"""
from streamlit.testing.v1 import AppTest


def test_app_starts():
    AppTest.from_file("app.py").run()
