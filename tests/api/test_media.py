import pytest

def test_get_media(api_client):
    response = api_client.get("/api/v1/media")
    assert response.status_code == 200
    data = response.json()
    assert "track_title" in data
    assert "volume" in data

def test_media_invalid_action(api_client):
    """Review Focus: Invalid media action should return 422."""
    payload = {"action": "warp_speed"}
    response = api_client.post("/api/v1/media", json=payload)
    assert response.status_code == 422

@pytest.mark.parametrize("action", ["play", "pause", "toggle", "next", "prev"])
def test_media_control_actions(api_client, action):
    payload = {"action": action}
    response = api_client.post("/api/v1/media", json=payload)
    assert response.status_code == 200
    assert "is_playing" in response.json()
