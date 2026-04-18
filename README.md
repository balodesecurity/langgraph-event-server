# langgraph-server

A FastAPI event routing server that accepts HTTP POST events, dispatches them to handler functions by `event_type`, and returns structured responses.

## Installation

**Prerequisites:** Python 3.13+

```bash
python3 -m venv langgraph-server
source langgraph-server/bin/activate
pip install langgraph langchain-anthropic langchain-core fastapi uvicorn
```

## Running the Server

```bash
source bin/activate
uvicorn fastapi_event_server:app --host 0.0.0.0 --port 8000
```

## Testing

**Health check:**
```bash
curl http://localhost:8000/health
```

**Alert event:**
```bash
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d '{"event_type": "alert_fired", "source": "iris", "payload": {"alert_id": "123", "service": "payments-api"}}'
```

**Deploy event:**
```bash
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d '{"event_type": "deploy_completed", "source": "jenkins", "payload": {"version": "v2.1.0"}}'
```

**Unknown event type** (returns 200 with a "no handler" message):
```bash
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d '{"event_type": "unknown_event", "source": "test", "payload": {}}'
```

## Adding a New Event Type

1. Create `handlers/<name>.py` with a function that takes `payload: dict` and returns a `str`.
2. Register it in `handlers/registry.py`:

```python
from handlers.<name> import handle_<name>

HANDLERS = {
    ...
    "<event_type>": handle_<name>,
}
```

## Interactive API Docs

FastAPI provides built-in docs at [http://localhost:8000/docs](http://localhost:8000/docs) when the server is running.
