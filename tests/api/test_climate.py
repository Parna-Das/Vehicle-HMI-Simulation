import pytest

def test_get_climate(api_client):
    response = api_client.get("/api/v1/climate")
    assert response.status_code == 200
    data = response.json()
    assert "driver_temp" in data
    assert "passenger_temp" in data
    assert "fan_speed" in data

def test_climate_malformed_payload(api_client):
    """Review Focus: Malformed payload - string instead of float for driver_temp should return 422."""
    payload = {
        "driver_temp": "twenty-two",
        "passenger_temp": 22.0,
        "fan_speed": 3,
        "ac_enabled": True,
        "heater_enabled": False,
        "front_defrost": False,
        "rear_defrost": True,
        "seat_heater_driver": 1,
        "seat_heater_passenger": 0
    }
    response = api_client.post("/api/v1/climate", json=payload)
    assert response.status_code == 422

@pytest.mark.parametrize("temp", [15.9, 30.1])
def test_climate_temperature_boundaries(api_client, temp):
    payload = {
        "driver_temp": temp,
        "passenger_temp": 22.0,
        "fan_speed": 3,
        "ac_enabled": True,
        "heater_enabled": False,
        "front_defrost": False,
        "rear_defrost": True,
        "seat_heater_driver": 1,
        "seat_heater_passenger": 0
    }
    response = api_client.post("/api/v1/climate", json=payload)
    assert response.status_code == 422

@pytest.mark.parametrize("fan", [-1, 8])
def test_climate_fan_speed_boundaries(api_client, fan):
    payload = {
        "driver_temp": 21.0,
        "passenger_temp": 22.0,
        "fan_speed": fan,
        "ac_enabled": True,
        "heater_enabled": False,
        "front_defrost": False,
        "rear_defrost": True,
        "seat_heater_driver": 1,
        "seat_heater_passenger": 0
    }
    response = api_client.post("/api/v1/climate", json=payload)
    assert response.status_code == 422
