
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_event_is_accepted():
    response = client.post(
        "/events",
        json={
            "event_id": "order-1001",
            "event_type": "order.created",
            "payload": {"order_id": 1001},
        },
    )

    assert response.status_code == 202
    assert response.json()["event_id"] == "order-1001"


def test_event_without_id_is_rejected():
    response = client.post(
        "/events",
        json={
            "event_type": "order.created",
            "payload": {"order_id": 1001},
        },
    )

    assert response.status_code == 422
