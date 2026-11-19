from tests.pages.base_page import BasePage
from playwright.sync_api import Page, TimeoutError

class HmiPage(BasePage):
    """Page Object for the Automotive HMI Web Application."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Selectors for HMI controls
        self.climate_tab = "#climate-tab"
        self.media_tab = "#media-tab"
        self.nav_tab = "#nav-tab"
        self.telemetry_tab = "#telemetry-tab"

        self.ac_toggle_btn = "#ac-toggle"
        self.temp_driver_up = "#temp-driver-up"
        self.temp_driver_display = "#temp-driver-display"

        self.play_pause_btn = "#media-play-pause"
        self.track_title_display = "#media-track-title"

        self.nav_input = "#nav-destination-input"
        self.nav_submit = "#nav-submit-btn"
        self.nav_status = "#nav-status-display"

    def click_climate_control(self):
        """Navigate to or toggle climate control section."""
        self.page.click(self.climate_tab)

    def toggle_ac(self):
        """Toggle AC state."""
        self.page.click(self.ac_toggle_btn)

    def play_media(self):
        """Play or pause media."""
        self.page.click(self.play_pause_btn)

    def set_navigation_destination(self, destination: str):
        """Set navigation destination."""
        self.page.fill(self.nav_input, destination)
        self.page.click(self.nav_submit)

    def test_element_timeout(self, selector: str = "#non-existent-element", timeout: int = 1000):
        """Helper to test element timeout behavior as specified in Review Focus."""
        try:
            self.page.locator(selector).wait_for(timeout=timeout)
        except TimeoutError:
            raise TimeoutError(f"Element {selector} failed to load within {timeout}ms")
