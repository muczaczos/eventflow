# FastAPI validation and error-handling checklist

Project rules live in CLAUDE.md; this list adds checks it does not spell out.

## Input validation
- Request bodies use Pydantic models; constraints are in `Field(...)`, not in
  manual `if` checks inside handlers.
- Every string field has `min_length` and `max_length`. Numbers have bounds
  where a bound makes sense.
- Free-form containers (`dict`, `list`) have some bound on size or depth, or
  the reviewer notes that they are unbounded.
- Fields with a documented format (event types are `domain.action`) enforce it
  with a pattern or validator, not only by convention.
- Query and path parameters are typed and constrained too.

## Error handling
- Invalid input yields `422` through Pydantic; handlers do not catch and
  re-wrap validation errors without a reason.
- No bare `except:` or `except Exception: pass`. Errors are not swallowed.
- Domain errors use `HTTPException` with an appropriate status code
  (`404`, `409`, ...) and a message safe to show to clients.
- Error responses do not contain stack traces, file paths, SQL or config.

## API contract
- Status codes match the semantics: `202` for accepted-for-async-processing,
  `201` for created resources, `200` for plain reads.
- Responses have a stable shape. Prefer a `response_model` over returning
  loose dicts when a response is part of the public contract.
- A response does not echo more than the client needs (no secrets, no
  internal ids).
- Handlers that do blocking I/O (database, files, network) are not `async def`
  without an async driver, and `def` handlers do not call `await`.

## Maintainability
- Handlers stay thin: parsing in models, logic in `app/services`, storage in
  `app/db`, as CLAUDE.md plans. Flag new logic added to `main.py` that belongs
  elsewhere.
- Configuration is read from environment variables in one place only.
- New code follows the pattern already used by existing endpoints and tests.
- No new dependency was added without it being mentioned to the user.

## Tests (supplements the rule in SKILL.md)
- Test names say the behaviour under test.
- Invalid-case tests assert the status code and, where useful, which field is
  reported, not only that "something failed".
- Boundary values are tested when a constraint is added (for example exactly
  `max_length` and `max_length + 1`).
- Tests do not depend on execution order or on a real `eventflow.db`.
