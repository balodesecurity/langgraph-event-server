# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI event routing server that accepts HTTP POST events, dispatches them to handler functions by `event_type`, and returns structured responses. The venv includes the full LangChain/LangGraph/Anthropic stack, making this a foundation for LLM-based event processing.

## Running and Testing

**Activate the virtual environment:**
```bash
source bin/activate
```

**Start the server:**
```bash
uvicorn server.fastapi_event_server:app --host 0.0.0.0 --port 8000
```

**Send a test event:**
```bash
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d '{"event_type": "alert_fired", "source": "iris", "payload": {"alert_id": "123", "service": "payments-api"}}'
```

**Health check:**
```bash
curl http://localhost:8000/health
```

## Architecture

The server entrypoint is `server/fastapi_event_server.py`; event handlers live in `event_handlers/`. The design has three layers:

1. **Pydantic models** — `Event` (incoming) and `EventResponse` (outgoing). `Event.payload` is an untyped `dict`; schema is implicit per event type.

2. **Handler functions** — each takes `payload: dict` and returns a `str` result message. Handlers are registered in the `HANDLERS` dict (`event_type` → function). Unrecognized event types return a 200 with "No handler for event_type: ..." — this is intentional.

3. **Two endpoints** — `POST /event` dispatches to handlers; `GET /health` returns `{"status": "healthy"}`.

**To add a new event type:** write a handler function, then add it to `HANDLERS`.

## Available Dependencies (pre-installed in venv)

Key packages available but not yet used in the application code:
- `langgraph`, `langgraph-sdk`, `langgraph-prebuilt` — graph-based agent orchestration
- `langchain-core`, `langchain-anthropic` — LangChain with Anthropic backend
- `anthropic` — direct Claude API access
- `httpx` — async HTTP client for calling external services

Python version: **3.13.7**
