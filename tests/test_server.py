from fastapi.testclient import TestClient
from unittest.mock import patch
from server.fastapi_event_server import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_known_event_type(mocker):
    mocker.patch("event_handlers.alert.handle_alert", return_value="alert handled")
    response = client.post("/event", json={
        "event_type": "alert_fired",
        "source": "test",
        "payload": {"alert_id": "1", "service": "payments"}
    })
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_unknown_event_type():
    response = client.post("/event", json={
        "event_type": "unknown_event",
        "source": "test",
        "payload": {}
    })
    assert response.status_code == 200
    assert "No handler" in response.json()["message"]


def test_response_has_received_at():
    response = client.post("/event", json={
        "event_type": "unknown_event",
        "source": "test",
        "payload": {}
    })
    assert "received_at" in response.json()
