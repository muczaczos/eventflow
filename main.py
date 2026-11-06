import os
from fastapi import FastAPI
from pydantic import BaseModel, Field

APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(title="EventFlow")

class EventInput(BaseModel):
    event_id: str = Field(min_length=1, max_length=100)
    event_type: str = Field(min_length=1, max_length=100)
    payload: dict


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
