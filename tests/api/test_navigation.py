import pytest

def test_get_navigation(api_client):
    response = api_client.get("/api/v1/navigation")
    assert response.status_code == 200
    data = response.json()
    assert "destination" in data
    assert "is_active" in data

def test_navigation_missing_destination(api_client):
    """Review Focus: Missing destination field should return 422."""
    payload = {}
    response = api_client.post("/api/v1/navigation", json=payload)
    assert response.status_code == 422

def test_set_and_cancel_navigation(api_client):
    nav_req = {"destination": "Tech Summit Arena, Seattle, WA"}
    res_post = api_client.post("/api/v1/navigation", json=nav_req)
    assert res_post.status_code == 200
    assert res_post.json()["destination"] == "Tech Summit Arena, Seattle, WA"
    assert res_post.json()["is_active"] is True

    res_del = api_client.delete("/api/v1/navigation")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "success"

    res_get = api_client.get("/api/v1/navigation")
    assert res_get.json()["is_active"] is False
