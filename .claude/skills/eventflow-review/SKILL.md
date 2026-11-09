---
name: eventflow-review
description: Read-only code review of the EventFlow FastAPI project. Use whenever the user asks to review, audit, check, sanity-check or "look over" code, a diff, staged/unstaged changes or a branch in this repo, even if they don't say "review". Covers code quality, API validation and error handling, security, test coverage and consistency with CLAUDE.md. Reports findings only and never changes files.
allowed-tools: Read, Grep, Glob, Bash(git status:*), Bash(git diff:*), Bash(git log:*)
---

# EventFlow review

Review code and report findings. Do not fix anything.

## Read-only rule

This is a review step: the user decides what changes. So do not edit, create,
move or delete files, and do not run commands that write (redirects, `sed -i`,
`git add/commit/checkout/stash/reset`, `pip install`, `docker build/run`).
Do not run tests either: pytest writes cache files, and "read-only" should be
literally true. Assess coverage by reading, and give the user the command
(`python -m pytest`) if they want to run it.

`allowed-tools` above only saves permission prompts. It is not a safety
boundary (for example `git diff --output=<file>` is a "git diff" that writes),
so the rule above is what keeps this read-only. If the user says "review and
fix", report the findings first and offer to fix them as a separate step.

## 1. Pick the scope

- **Default:** current staged and unstaged changes only. Run
  `git status --short`, `git diff --cached` (staged) and `git diff`
  (unstaged). Untracked files (`??`) are not in the diffs, so read them
  directly.
- **Branch review** (user mentions a branch or PR): review the committed
  changes with `git diff master...HEAD`, and report local changes separately.
  Staged (`git diff --cached`), unstaged (`git diff`) and untracked files each
  get their own part of the report, so the reader can tell what is committed
  and what is not.
- **No changes found:** say so and ask before reviewing the whole repository.
  Do not start a full review on your own.

State the scope you used at the top of the report.

## 2. Gather context

Read `CLAUDE.md` now instead of relying on memory: it is the source of truth
for project rules and may have changed. Then read the changed files (in full
when the diff alone is ambiguous), the related tests in `tests/`, and the
Dockerfile or CI file if the change touches them.

## 3. Check

Work through these areas, loading a reference file only when the change
touches that area, to keep the review focused:

- **Quality and maintainability**: duplication, unclear naming, logic in
  `main.py` that CLAUDE.md says should move to `app/*` modules, new patterns
  where an existing one should be reused.
- **API validation and error handling**: see `references/fastapi-checklist.md`.
- **Security**: see `references/security-checklist.md`.
- **Test coverage**: for each new or changed endpoint and validation rule, find
  the test that covers it by reading `tests/`. CLAUDE.md requires a valid case
  and at least one invalid case (`422`) per endpoint or validation change.
  List what is covered and what is not; don't guess at percentages.
- **CLAUDE.md consistency**: for every finding that breaks a rule, cite it.

Focus on the changed code. A pre-existing problem may be mentioned only if the
change touches or depends on it, in a short separate list.

## 4. Report

Use this structure, and skip empty sections with a one-line "nothing found":

```
## Scope
What was reviewed. For a branch review, list committed, staged, unstaged and
untracked changes separately.

## Findings
Ranked by severity. For each:
### [High|Medium|Low] Short title: `path:line`
- Area: quality | validation | security | tests | CLAUDE.md
- Where: committed | staged | unstaged | untracked (branch reviews only)
- Problem: what is wrong, in one or two sentences.
- Impact: what can go wrong, concretely.
- Rule: the CLAUDE.md rule it breaks, if any.
- Suggested fix: described in words or a short snippet. Not applied.

## Test coverage
Endpoint / rule -> covering test, or "not covered".

## Unknown
Anything you could not verify (tests not run, files not read, behaviour that
depends on runtime), so the reader doesn't take silence for a pass.

## Summary
One or two sentences: overall assessment and the most important next step.
```

Severity: **High** is exploitable, data-exposing or breaks a stated CLAUDE.md
security rule. **Medium** is incorrect or missing behaviour or missing required
tests. **Low** is maintainability and style.

Mark each finding as confirmed (you saw it in the code) or suspected (you infer
it). Only report real problems; padding the list with nitpicks hides the
important findings.
