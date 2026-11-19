import pytest

def test_get_telemetry(api_client):
    response = api_client.get("/api/v1/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert "speed" in data
    assert "rpm" in data
    assert "gear" in data
    assert "tire_pressure" in data

def test_telemetry_speed_boundary_overflow(api_client):
    """Review Focus: Boundary Overflow - speed > 240.0 should return 422."""
    payload = {
        "speed": 250.0,
        "rpm": 2200,
        "gear": "D",
        "fuel_level": 78.5,
        "battery_level": 95.0,
        "tire_pressure": {"fl": 32.0, "fr": 32.0, "rl": 31.5, "rr": 31.5},
        "headlights": True,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    response = api_client.put("/api/v1/telemetry", json=payload)
    assert response.status_code == 422

def test_telemetry_speed_boundary_underflow(api_client):
    """Review Focus: Boundary Underflow - speed < 0.0 should return 422."""
    payload = {
        "speed": -5.0,
        "rpm": 2200,
        "gear": "D",
        "fuel_level": 78.5,
        "battery_level": 95.0,
        "tire_pressure": {"fl": 32.0, "fr": 32.0, "rl": 31.5, "rr": 31.5},
        "headlights": True,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    response = api_client.put("/api/v1/telemetry", json=payload)
    assert response.status_code == 422

@pytest.mark.parametrize("gear", ["P", "R", "N", "D", "S", "p", "d"])
def test_telemetry_valid_gears(api_client, gear):
    payload = {
        "speed": 50.0,
        "rpm": 2000,
        "gear": gear,
        "fuel_level": 70.0,
        "battery_level": 90.0,
        "tire_pressure": {"fl": 32.0, "fr": 32.0, "rl": 32.0, "rr": 32.0},
        "headlights": False,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    response = api_client.put("/api/v1/telemetry", json=payload)
    assert response.status_code == 200
    assert response.json()["gear"] == gear.upper()

def test_state_persistence_chain(api_client):
    """Review Focus: Sequential state updates and persistence."""
    payload1 = {
        "speed": 100.0,
        "rpm": 3000,
        "gear": "S",
        "fuel_level": 50.0,
        "battery_level": 80.0,
        "tire_pressure": {"fl": 33.0, "fr": 33.0, "rl": 32.0, "rr": 32.0},
        "headlights": True,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    res1 = api_client.put("/api/v1/telemetry", json=payload1)
    assert res1.status_code == 200

    res2 = api_client.get("/api/v1/telemetry")
    assert res2.status_code == 200
    data = res2.json()
    assert data["speed"] == 100.0
    assert data["gear"] == "S"
    assert data["rpm"] == 3000
