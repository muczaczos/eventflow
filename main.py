import json
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from starlette.datastructures import Headers

APP_ENV = os.getenv("APP_ENV", "development")

# Size of the "payload" field as compact UTF-8 JSON (validated -> 422).
MAX_PAYLOAD_BYTES = 64 * 1024
# Size of the whole HTTP request body on the wire (enforced before parsing -> 413).
# Larger than the payload limit so the envelope never causes a false 413.
MAX_BODY_BYTES = 128 * 1024


class BodySizeLimitMiddleware:
    """Reject request bodies larger than max_bytes with 413, before JSON parsing."""

    def __init__(self, app, max_bytes: int = MAX_BODY_BYTES):
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        declared = Headers(scope=scope).get("content-length")
        if (
            declared is not None
            and declared.isascii()
            and declared.isdigit()
            and int(declared) > self.max_bytes
        ):
            # Declared too large: answer without reading a single body byte.
            response = JSONResponse(
                {"detail": "Request body too large"}, status_code=413
            )
            await response(scope, receive, send)
            return

        received = 0

        async def limited_receive():
            # Covers chunked bodies and requests without Content-Length.
            # Must be FastAPI's HTTPException: FastAPI turns any other exception
            # raised while reading the body into a generic 400.
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_bytes:
                    raise HTTPException(status_code=413, detail="Request body too large")
            return message

        await self.app(scope, limited_receive, send)


app = FastAPI(title="EventFlow")
app.add_middleware(BodySizeLimitMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    # Default 422 responses echo the rejected value ("input"), which would send
    # an oversized payload (and possibly personal data) back to the client.
    errors = [
        {"type": e["type"], "loc": list(e["loc"]), "msg": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse({"detail": errors}, status_code=422)


class EventInput(BaseModel):
    event_id: str = Field(min_length=1, max_length=100)
    event_type: str = Field(min_length=1, max_length=100)
    payload: dict

    @field_validator("payload")
    @classmethod
    def payload_must_not_be_too_large(cls, value: dict) -> dict:
        size = len(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
        if size > MAX_PAYLOAD_BYTES:
            raise ValueError(f"payload exceeds {MAX_PAYLOAD_BYTES} bytes")
        return value


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "application": "EventFlow",
        "version": "2.0",
        "environment": APP_ENV
    }


@app.post("/events", status_code=202)
def receive_event(event: EventInput):
    return {
        "message": "Event received",
        "event_id": event.event_id,
        "event_type": event.event_type,
        "payload": event.payload,
    }
