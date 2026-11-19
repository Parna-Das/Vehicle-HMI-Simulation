import pytest
from fastapi.testclient import TestClient
from app.main import app
from playwright.sync_api import sync_playwright

@pytest.fixture
def api_client():
    """FastAPI TestClient fixture for backend API testing."""
    return TestClient(app)

@pytest.fixture
def hmi_page():
    """Playwright browser page fixture for HMI UI testing."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

# Review Focus tests required by plan
def test_api_connection_failure(api_client):
    """Test behavior when API client encounters invalid route or connection issue."""
    response = api_client.get("/nonexistent-endpoint")
    assert response.status_code == 404

def test_invalid_fixture_state(api_client):
    """Test invalid state setup raises validation error."""
    invalid_data = {
        "speed": 300.0, # invalid, max is 240.0
        "rpm": 2200,
        "gear": "P",
        "fuel_level": 78.5,
        "battery_level": 95.0,
        "tire_pressure": {"fl": 32.0, "fr": 32.0, "rl": 31.5, "rr": 31.5},
        "headlights": True,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    response = api_client.put("/api/v1/telemetry", json=invalid_data)
    assert response.status_code == 422
