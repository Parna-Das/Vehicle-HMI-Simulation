from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "endpoints" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_telemetry():
    response = client.get("/api/v1/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert "speed" in data
    assert "rpm" in data
    assert "gear" in data
    assert "tire_pressure" in data

def test_update_telemetry_valid():
    payload = {
        "speed": 45.5,
        "rpm": 1800,
        "gear": "D",
        "fuel_level": 60.0,
        "battery_level": 90.0,
        "tire_pressure": {
            "fl": 32.0,
            "fr": 32.0,
            "rl": 31.0,
            "rr": 31.0
        },
        "headlights": False,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    response = client.put("/api/v1/telemetry", json=payload)
    assert response.status_code == 200
    assert response.json()["speed"] == 45.5
    assert response.json()["gear"] == "D"

def test_update_telemetry_invalid_gear():
    payload = {
        "speed": 45.5,
        "rpm": 1800,
        "gear": "X",  # Invalid gear
        "fuel_level": 60.0,
        "battery_level": 90.0,
        "tire_pressure": {
            "fl": 32.0,
            "fr": 32.0,
            "rl": 31.0,
            "rr": 31.0
        },
        "headlights": False,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    response = client.put("/api/v1/telemetry", json=payload)
    assert response.status_code == 422

def test_climate_endpoints():
    # GET climate
    res_get = client.get("/api/v1/climate")
    assert res_get.status_code == 200
    assert "driver_temp" in res_get.json()

    # POST valid climate
    payload = {
        "driver_temp": 22.5,
        "passenger_temp": 23.0,
        "fan_speed": 4,
        "ac_enabled": True,
        "heater_enabled": False,
        "front_defrost": False,
        "rear_defrost": False,
        "seat_heater_driver": 2,
        "seat_heater_passenger": 0
    }
    res_post = client.post("/api/v1/climate", json=payload)
    assert res_post.status_code == 200
    assert res_post.json()["driver_temp"] == 22.5

    # POST invalid temperature (out of range 16-30)
    payload["driver_temp"] = 35.0
    res_invalid = client.post("/api/v1/climate", json=payload)
    assert res_invalid.status_code == 422

def test_navigation_endpoints():
    res_get = client.get("/api/v1/navigation")
    assert res_get.status_code == 200
    assert "destination" in res_get.json()

    # Set destination
    nav_req = {"destination": "Golden Gate Bridge, San Francisco, CA"}
    res_post = client.post("/api/v1/navigation", json=nav_req)
    assert res_post.status_code == 200
    assert res_post.json()["destination"] == "Golden Gate Bridge, San Francisco, CA"
    assert res_post.json()["is_active"] is True

    # Cancel navigation
    res_del = client.delete("/api/v1/navigation")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "success"

def test_media_endpoints():
    res_get = client.get("/api/v1/media")
    assert res_get.status_code == 200
    assert "track_title" in res_get.json()

    # Control media (play / next / volume)
    control_payload = {
        "action": "next",
        "volume": 50,
        "source": "Bluetooth"
    }
    res_post = client.post("/api/v1/media", json=control_payload)
    assert res_post.status_code == 200
    assert res_post.json()["volume"] == 50
    assert res_post.json()["source"] == "Bluetooth"
    assert res_post.json()["is_playing"] is True

    # Invalid action
    bad_control = {"action": "warp_speed"}
    res_bad = client.post("/api/v1/media", json=bad_control)
    assert res_bad.status_code == 422
