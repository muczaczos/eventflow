# CLAUDE.md

EventFlow is a FastAPI microservice for ingesting events. Early stage: `POST /events` validates and echoes events but does not persist them. Planned: SQLite via SQLAlchemy (`eventflow.db`) and async processing, hence `202 Accepted`.

## Working rules

- **Before changing code, analyze existing solutions.** Read related code, tests, Dockerfile and CI; reuse existing patterns.
- Keep changes minimal and scoped to the task. Ask before out-of-scope refactors or adding dependencies (vet maintenance and vulnerabilities).
- Never commit or push unless explicitly asked.

## Testing

- Run tests with `python -m pytest`, not bare `pytest`: there is no pytest config, so `from main import app` needs the repo root on `sys.path`.
- Runtime dependencies go in `requirements.txt`; test/dev tools in `requirements-dev.txt`.
- New endpoints or validation changes need tests for the valid case and at least one invalid case (`422`).
- Run tests before reporting work as done.

## Conventions

- Validate input with Pydantic models and `Field(...)` constraints, not manual checks.
- Event types use the `domain.action` format (e.g. `order.created`).
- Configuration only via environment variables, read in one place; nothing environment-specific hardcoded.
- As the app grows, split into `app/api`, `app/models`, `app/services`, `app/db` rather than expanding `main.py`.

## Docker

- Never put secrets in `ENV` in the Dockerfile; pass config via `-e` / `--env-file`.
- After Dockerfile changes, build the image and check `GET /health` in a running container.
- The production container must run as a non-root user.

## Security

- Never commit secrets, `.env` or `eventflow.db`.
- Don't log full event payloads; they may contain personal data.
- Constrain field lengths/sizes on all input models.
- Error responses must not expose internals (stack traces, paths, config).
- With a database, use only the ORM or parameterized queries; never build SQL from strings.
