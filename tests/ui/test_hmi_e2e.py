import os
import pytest
from tests.pages.hmi_page import HmiPage

@pytest.fixture
def hmi(hmi_page):
    index_path = os.path.abspath("app/static/index.html")
    hmi_page.goto(f"file:///{index_path}")
    return HmiPage(hmi_page)

def test_hmi_climate_tab_interaction(hmi):
    hmi.click_climate_control()
    assert hmi.page.locator("#climate-panel").is_visible()

    # Toggle AC
    hmi.toggle_ac()
    assert hmi.page.locator("#ac-status").inner_text() == "OFF"

def test_hmi_media_interaction(hmi):
    hmi.page.click(hmi.media_tab)
    assert hmi.page.locator("#media-panel").is_visible()

    hmi.play_media()
    assert hmi.page.locator("#media-play-pause").inner_text() == "Playing"

def test_hmi_navigation_interaction(hmi):
    hmi.page.click(hmi.nav_tab)
    assert hmi.page.locator("#nav-panel").is_visible()

    hmi.set_navigation_destination("San Francisco, CA")
    assert "San Francisco, CA" in hmi.page.locator("#nav-status-display").inner_text()
