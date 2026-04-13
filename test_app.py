import pytest
from dash.testing.application_runners import import_app


@pytest.fixture
def app_instance():
    return import_app("app")


def test_header_present(dash_duo, app_instance):
    """The header element is rendered on the page."""
    dash_duo.start_server(app_instance)
    dash_duo.wait_for_element("#header", timeout=10)
    header = dash_duo.find_element("#header")
    assert header is not None


def test_chart_present(dash_duo, app_instance):
    """The sales line chart is rendered on the page."""
    dash_duo.start_server(app_instance)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None


def test_region_picker_present(dash_duo, app_instance):
    """The region radio-button picker is rendered on the page."""
    dash_duo.start_server(app_instance)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    picker = dash_duo.find_element("#region-filter")
    assert picker is not None
