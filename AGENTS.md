# AGENTS.md

This file defines contribution rules for human and AI agents working in this repository.

## Core standards

- Keep code Pythonic: clear naming, small focused functions, explicit constants, and straightforward control flow.
- Prefer standard-library solutions when they keep code simple and readable.
- Add type hints to public function signatures.
- Keep HTTP/API integrations defensive: explicit timeout and status checks.
- Avoid overengineering; optimize for maintainability and testability.

## Testing policy (required)

- Any behavior change must include related unit tests.
- Update existing tests when contracts change.
- "Done" means tests were generated/updated and executed successfully.
- Do not mark tasks complete while tests are failing or not run.

## Local verification commands

- Run tests: `uv run python -m unittest -v`
- Run lint checks: `uv run pylint emotion_detection.py test_emotion_detection.py`

## Pull request checklist

- Code follows Python best practices and repository conventions.
- New/changed behavior is covered by unit tests.
- All tests pass locally before completion.
