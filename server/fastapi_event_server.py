# fastapi_event_server.py
#
# A generic FastAPI server that consumes events via HTTP POST,
# routes them to the appropriate handler based on event_type,
# and returns a response.
#
# Run:   uvicorn fastapi_event_server:app --host 0.0.0.0 --port 8000
# Test:  curl -X POST http://localhost:8000/event \
#          -H "Content-Type: application/json" \
#          -d '{"event_type": "alert_fired", "source": "iris", "payload": {"alert_id": "123", "service": "payments-api"}}'

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, UTC
from event_handlers.registry import HANDLERS

app = FastAPI()


# --- Request/Response models ---

class Event(BaseModel):
    """Incoming event from any producer (monitoring system, CI/CD, etc.)."""
    event_type: str   # Determines which handler processes this event (e.g. "alert_fired")
    source: str       # Origin system for traceability (e.g. "iris", "jenkins")
    payload: dict     # Arbitrary event data — schema depends on event_type


class EventResponse(BaseModel):
    """Response returned after processing an event."""
    status: str       # "ok" or "error"
    message: str      # Human-readable result of processing
    received_at: str  # ISO timestamp of when the server received the event


# --- API endpoints ---

@app.post("/event", response_model=EventResponse)
async def consume_event(event: Event):
    """Accept an event, route it to the matching handler, return the result.

    If no handler exists for the event_type, returns a message saying so
    (still 200 — the event was received, just not actionable).
    """
    handler = HANDLERS.get(event.event_type)
    if handler:
        message = handler(event.payload)
    else:
        message = f"No handler for event_type: {event.event_type}"

    return EventResponse(
        status="ok",
        message=message,
        received_at=datetime.now(UTC).isoformat(),
    )


@app.get("/health")
async def health():
    """Simple health check for load balancers / readiness probes."""
    return {"status": "healthy"}
