# Security checklist

CLAUDE.md states the core rules. Check the change against them and the points
below. Report only what the code actually shows.

## Input
- All input models constrain lengths and sizes. Look especially at fields that
  accept arbitrary structures, which can be used to send very large bodies.
- Values are never used to build file paths, shell commands or SQL.

## Data exposure and logging
- Full event payloads are not logged, not in `print`, `logging`, or
  exception messages. Payloads may contain personal data.
- Error responses and `/health` do not reveal internals (paths, versions of
  dependencies, config, environment secrets).
- `/health` returns only what is meant to be public. Note any new fields.

## Database
- Only the ORM or parameterized queries. Flag string-built SQL, f-strings and
  `.format()` inside `text()` or `execute()`.
- Sessions are closed, and failed transactions are rolled back.
- `eventflow.db` and any `.env` are not added to git or to the image.

## Configuration and secrets
- No secrets, tokens, passwords or environment-specific values in code, the
  Dockerfile (`ENV`, `ARG`), CI files or tests.
- Configuration comes from environment variables, read in one place.

## Container
- The image does not run as root: a non-root `USER` is set before `CMD`.
- `.dockerignore` still excludes `.env`, databases and local files.
- Nothing sensitive is copied into the image by `COPY . .`.
- Changes to the Dockerfile are verified by building and checking
  `GET /health`. If the review cannot do that, list it under Unknown.

## Dependencies
- A new dependency in `requirements.txt` or `requirements-dev.txt` is flagged
  for the user, with a reminder to check maintenance status and known
  vulnerabilities. Do not claim a package is safe without evidence.
- Runtime dependencies stay in `requirements.txt`, test tools in
  `requirements-dev.txt`.
