# CLAUDE.md

EventFlow is a FastAPI microservice for ingesting events. Early stage: `POST /events`
validates and echoes events but does not persist them yet. Planned: storage
(SQLite via SQLAlchemy, `eventflow.db`) and async processing, hence `202 Accepted`.

## Working rules

- **Before changing code, analyze existing solutions.** Read related code, tests,
  Dockerfile and CI; reuse existing patterns instead of duplicating logic or adding
  new libraries.
- Keep changes minimal and scoped to the task. Ask before out-of-scope refactors
  or adding dependencies.
- Never commit or push unless explicitly asked.

## Running and testing

    pip install -r requirements.txt
    uvicorn main:app --reload
    python -m pytest

- Always run tests with `python -m pytest` (as CI does), not bare `pytest`:
  there is no pytest config, so `from main import app` needs the repo root on `sys.path`.
- New endpoints or validation changes need tests for the valid case and at least
  one invalid case (`422`).
- Run tests before reporting work as done; report failures as they are.
- Known issue: `test_health_returns_ok` expects only `{"status": "ok"}`, but `/health`
  returns more fields. Ask which behavior is correct; don't silently change either side.

## Conventions

- Validate input with Pydantic models and `Field(...)` constraints, not manual checks.
- Event types use the `domain.action` format (e.g. `order.created`).
- Configuration only via environment variables, read in one place; no
  environment-specific values hardcoded.
- As the app grows, split into modules (`app/api`, `app/models`, `app/services`,
  `app/db`) rather than expanding `main.py`.

## Docker

    docker build -t eventflow .
    docker run -p 8000:8000 -e APP_ENV=production eventflow

- Keep the Python version in sync with CI (3.12).
- Keep layer order: copy `requirements.txt` and install before `COPY . .`.
- Pass config via `-e` / `--env-file`; never put secrets in `ENV` in the Dockerfile.
- Keep `.dockerignore` excluding `.env`, databases and local files.
- After Dockerfile changes, build the image and check `GET /health` in a running container.

## Security

- Never commit secrets, `.env` or `eventflow.db`.
- Don't log full event payloads; they may contain personal data.
- Constrain field lengths/sizes on all input models.
- Error responses must not expose internals (stack traces, paths, config).
- With a database, use only the ORM or parameterized queries; never build SQL from strings.
- The production container should not run as root (TODO: add `USER` to the Dockerfile).
- Vet new dependencies for maintenance status and known vulnerabilities.
