from playwright.sync_api import Page, Locator

class BasePage:
    """Base class for all Page Object Model classes."""
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)

    def wait_for_selector(self, selector: str, timeout: float = 5000) -> Locator:
        """Wait for selector and return locator."""
        return self.page.locator(selector)
