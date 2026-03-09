from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_camera() -> None:
    payload = {
        "name": "Test Camera",
        "location": "Arlington",
        "source_url": "sample.mp4",
        "stop_line_y": 340,
        "red_light_roi": [10, 10, 20, 20],
    }
    response = client.post("/streams/register", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
