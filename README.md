# EventFlow

[![Tests](https://github.com/muczaczos/eventflow/actions/workflows/tests.yml/badge.svg)](https://github.com/muczaczos/eventflow/actions/workflows/tests.yml)

A small FastAPI service for ingesting events over HTTP.

EventFlow is a **portfolio project that is developed in stages**. It is not a production event-processing
system. This README describes what exists now and clearly separates it from what is planned.

## At a glance

- **What it does:** accepts events on `POST /events`, validates them and acknowledges them with `202 Accepted`.
- **What is implemented:** input validation, two layers of size limits, structured error responses, automated
  tests with CI and a Docker image that runs as a non-root user.
- **What is not implemented yet:** storing and processing events. Both are planned (see [Status](#status)).

## Status

| Area | State |
|---|---|
| `POST /events`: validation, size limits, `202 Accepted` response | Implemented |
| `GET /health` | Implemented |
| Structured validation errors (`422`) and oversized-request rejection (`413`) | Implemented |
| Automated tests and CI (GitHub Actions) | Implemented |
| Docker image running as a non-root user | Implemented |
| Persistence (SQLite via SQLAlchemy) | Planned, not implemented |
| Asynchronous event processing | Planned, not implemented |
| Split of `main.py` into `app/api`, `app/models`, `app/services`, `app/db` | Intended as the codebase grows, not implemented |

The `202 Accepted` status is chosen on purpose, because the service is meant to acknowledge events for later
asynchronous processing. That processing does not exist yet: at this stage the event is only echoed back.

## Tech stack

| Purpose | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | FastAPI, served by Uvicorn |
| Validation | Pydantic (v2 API) |
| Tests | pytest, httpx (FastAPI `TestClient`) |
| Container | Docker (`python:3.12-slim`) |
| CI | GitHub Actions |
| Formatting | Ruff (applied through a development hook, not a project dependency) |
| Storage (planned) | SQLite via SQLAlchemy. SQLAlchemy is already listed in `requirements.txt` but is not used yet. |

## Architecture (current stage)

The whole application lives in a single module, `main.py`. Simplified request flow:

```
Client
  |  HTTP
  v
Uvicorn
  |
  v
BodySizeLimitMiddleware ---- body larger than 128 KiB ------> 413 Request body too large
  |
  v
FastAPI route
  |
  v
EventInput (Pydantic) ------ invalid or payload > 64 KiB ---> 422 Validation error
  |
  v
202 Accepted (the event is echoed back; nothing is stored)
```

Two layers protect the service from oversized input:

1. **Request body limit (128 KiB)**: an ASGI middleware rejects the request with `413` before the JSON
   is parsed. It checks `Content-Length` when present and counts bytes while reading otherwise
   (for example for chunked requests).
2. **Payload limit (64 KiB)**: the `payload` field is validated inside the model and rejected with `422`.

The body limit is intentionally larger than the payload limit, so the rest of the request
(IDs, whitespace, escaped characters) never causes a false `413`.

## Requirements

- Python 3.12 (used by the Docker image and CI; other versions are not tested)
- Docker, optional, only for running the container

## Run locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload
```

On Windows, activate the environment with `.venv\Scripts\activate` instead of `source .venv/bin/activate`, and use
any Python 3.12 interpreter in place of `python3.12` (for example `py -3.12`).

The service listens on <http://127.0.0.1:8000>. FastAPI's interactive API documentation is available at
<http://127.0.0.1:8000/docs> (OpenAPI schema at `/openapi.json`).

### Configuration

| Variable | Default | Meaning |
|---|---|---|
| `APP_ENV` | `development` | Environment name. Currently it is only reported by `GET /health`. |

## Run with Docker

```bash
docker build -t eventflow .
docker run --rm -d --name eventflow -p 8000:8000 -e APP_ENV=production eventflow
curl http://localhost:8000/health
docker stop eventflow
```

The image is based on `python:3.12-slim`, runs Uvicorn on port 8000 and runs as a dedicated non-root
user (`app`). Configuration is passed at runtime with `-e` / `--env-file`; no secrets are stored in the Dockerfile.

## API

| Method | Path | Success response | Description |
|---|---|---|---|
| `GET` | `/health` | `200` | Liveness check |
| `POST` | `/events` | `202` | Validate an event and acknowledge it |

### `POST /events`

Request body (JSON):

| Field | Type | Rules |
|---|---|---|
| `event_id` | string | 1 to 100 characters |
| `event_type` | string | 1 to 100 characters. The project convention is `domain.action` (for example `order.created`); the format is **not enforced yet**. |
| `payload` | JSON object | At most 64 KiB, measured as compact UTF-8 JSON |

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"event_id": "order-1001", "event_type": "order.created", "payload": {"order_id": 1001, "amount": 49.99}}'
```

```json
{"message":"Event received","event_id":"order-1001","event_type":"order.created","payload":{"order_id":1001,"amount":49.99}}
```

Status `202 Accepted`.

### `GET /health`

```bash
curl http://localhost:8000/health
```

```json
{"status":"ok","application":"EventFlow","version":"2.0","environment":"development"}
```

The `version` value is currently a fixed string.

## Limits

| Limit | Value | Result when exceeded |
|---|---|---|
| `event_id`, `event_type` length | 100 characters each | `422` |
| `payload` size | 64 KiB (65,536 bytes), compact UTF-8 JSON | `422` |
| HTTP request body size | 128 KiB (131,072 bytes) | `413` |

The limits are inclusive: a payload of exactly 65,536 bytes and a body of exactly 131,072 bytes are accepted.
The payload size is counted in UTF-8 bytes, not characters.

## Error responses

Validation errors (`422`) list the field location, an error type and a message. The response omits the
submitted values (the `input` field of FastAPI's default error format), so oversized or sensitive input is not
sent back to the client.

Missing field:

```json
{"detail":[{"type":"missing","loc":["body","event_id"],"msg":"Field required"}]}
```

Payload over 64 KiB:

```json
{"detail":[{"type":"value_error","loc":["body","payload"],"msg":"Value error, payload exceeds 65536 bytes"}]}
```

Malformed JSON, for example the body `{"event_id": oops` (the `13` in `loc` is the character offset of the error):

```json
{"detail":[{"type":"json_invalid","loc":["body",13],"msg":"JSON decode error"}]}
```

Request body over 128 KiB (`413`):

```json
{"detail":"Request body too large"}
```

## Tests

```bash
python -m pytest
```

Use `python -m pytest` rather than bare `pytest`: there is no pytest configuration, and the module form puts
the repository root on `sys.path` so that `from main import app` works.

The suite (9 tests in `tests/test_main.py`) covers the health endpoint, accepting a valid event, rejecting an
event without `event_id`, the payload limit at its exact boundary and one byte over, UTF-8 byte counting, and
the request-body limit at its boundary, including chunked requests. GitHub Actions runs the tests on every
push and pull request.

## Main files

```
main.py                       Application: endpoints, model, size limits, error handler
tests/test_main.py            Tests
Dockerfile                    Container image (non-root user)
.dockerignore, .gitignore       Files excluded from the Docker build context and from git
requirements.txt              Runtime dependencies
requirements-dev.txt          Test dependencies (includes requirements.txt)
ruff.toml                     Ruff formatting configuration
.github/workflows/tests.yml   CI: install dependencies and run pytest
CLAUDE.md                     Project rules for the AI coding assistant
.claude/                      Assistant skill and hook (see below)
```

## Development workflow

The project is developed with [Claude Code](https://claude.com/claude-code). The workflow is part of the repository:

- `CLAUDE.md` holds the project rules (testing requirements, conventions, security constraints).
- `.claude/skills/eventflow-review/` is a strictly read-only code review skill for this project.
- `.claude/hooks/ruff-format.sh` formats Python files with Ruff after the assistant edits them.
  It runs Ruff through `uvx`, so Ruff is not a project dependency.

## Current limitations

- Events are not persisted or processed; the endpoint only validates and acknowledges them.
- There is no authentication, rate limiting or duplicate detection for `event_id`.
- The `domain.action` event type format is a convention and is not validated.
- Dependency versions are not pinned.
