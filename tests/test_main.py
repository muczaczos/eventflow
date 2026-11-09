import json

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


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
    for error in response.json()["detail"]:
        assert "input" not in error
        assert "ctx" not in error


MAX_PAYLOAD_BYTES = 64 * 1024
MAX_BODY_BYTES = 128 * 1024
JSON_HEADERS = {"content-type": "application/json"}


def post_event(payload):
    """POST an event with a compact UTF-8 JSON body (size is exactly what we send)."""
    body = json.dumps(
        {"event_id": "e-1", "event_type": "order.created", "payload": payload},
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return client.post("/events", content=body, headers=JSON_HEADERS)


def padded_body(total_size):
    """Valid small event JSON padded with trailing spaces to exactly total_size bytes."""
    body = b'{"event_id":"e-1","event_type":"order.created","payload":{}}'
    return body + b" " * (total_size - len(body))


def chunks(data, size=4096):
    for i in range(0, len(data), size):
        yield data[i : i + size]


def test_payload_of_exactly_max_size_is_accepted():
    # {"k":"..."} has 8 bytes of JSON overhead around the value.
    payload = {"k": "x" * (MAX_PAYLOAD_BYTES - 8)}
    assert len(json.dumps(payload, separators=(",", ":")).encode()) == MAX_PAYLOAD_BYTES

    response = post_event(payload)

    assert response.status_code == 202


def test_payload_over_max_size_is_rejected_without_echoing_it():
    response = post_event({"k": "x" * (MAX_PAYLOAD_BYTES - 8 + 1)})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail[0]["loc"] == ["body", "payload"]
    assert "x" * 100 not in response.text


def test_payload_size_is_measured_in_utf8_bytes_not_characters():
    # "é" is 2 bytes in UTF-8: 32764 of them fit exactly, 32765 are 2 bytes too many,
    # although both are far below 64K characters.
    assert post_event({"k": "é" * 32764}).status_code == 202
    assert post_event({"k": "é" * 32765}).status_code == 422


def test_body_of_exactly_max_size_is_accepted():
    response = client.post("/events", content=padded_body(MAX_BODY_BYTES), headers=JSON_HEADERS)

    assert response.status_code == 202


def test_body_over_max_size_is_rejected_with_413():
    response = client.post("/events", content=padded_body(MAX_BODY_BYTES + 1), headers=JSON_HEADERS)

    assert response.status_code == 413
    assert response.json() == {"detail": "Request body too large"}


def test_chunked_body_without_content_length_is_limited_too():
    ok = client.post("/events", content=chunks(padded_body(MAX_BODY_BYTES)), headers=JSON_HEADERS)
    too_big = client.post(
        "/events", content=chunks(padded_body(MAX_BODY_BYTES + 1)), headers=JSON_HEADERS
    )

    assert ok.status_code == 202
    assert too_big.status_code == 413
    assert too_big.json() == {"detail": "Request body too large"}
