# Final project

This repository contains a small Python Flask exercise for emotion detection using the Watson NLP EmotionPredict endpoint.

## Usage & Examples

### 1. Quick REPL test

Use the function directly from a Python shell:

```bash
uv run python
```

```python
>>> from emotion_detection import emotion_detector
>>> emotion_detector("I love this new technology.")
'{"emotionPredictions":[...]} '
```

Note: the function returns a JSON string (not a Python dict).

### 2. Parse the returned JSON

If you want to work with fields programmatically, parse the returned string:

```python
import json
from emotion_detection import emotion_detector

raw = emotion_detector("I love this new technology.")
payload = json.loads(raw)

top_emotion_scores = payload["emotionPredictions"][0]["emotion"]
print(top_emotion_scores)
```

Example output shape:

```json
{
  "emotionPredictions": [
    {
      "emotion": {
        "anger": 0.01,
        "disgust": 0.00,
        "fear": 0.01,
        "joy": 0.97,
        "sadness": 0.05
      }
    }
  ]
}
```

### 3. Handle network and HTTP errors

The function calls `raise_for_status()`, so failed HTTP responses raise an exception.

```python
import requests
from emotion_detection import emotion_detector

try:
    print(emotion_detector("This is a test."))
except requests.HTTPError as err:
    print(f"API returned an HTTP error: {err}")
except requests.RequestException as err:
    print(f"Network or request error: {err}")
```

### 4. Try multiple inputs quickly

```python
from emotion_detection import emotion_detector

samples = [
    "I am excited about this project!",
    "I am worried about the deadline.",
    "This result is disappointing.",
]

for text in samples:
    print(text)
    print(emotion_detector(text))
    print("-" * 40)
```

## Tech stack

- Python 3.12+
- uv for environment and dependency management
- requests for HTTP calls
- Flask as an app dependency
- unittest for tests
- pylint for linting

## Project layout

- emotion_detection.py: Emotion detection client function
- test_emotion_detection.py: Unit tests for emotion detection
- templates/: HTML templates
- static/: Static frontend assets
- pyproject.toml: Project metadata and dependencies
- uv.lock: Locked dependency graph for reproducible installs

## Setup with uv

1. Install dependencies (including dev dependencies):

	 uv sync

2. Run tests:

	 uv run python -m unittest -v

3. Run lint checks:

	 uv run pylint emotion_detection.py test_emotion_detection.py

## Dependency management with uv

- Add a runtime package:

	uv add <package>

- Add a development package:

	uv add --dev <package>

- Re-lock dependencies after changes (usually automatic when adding/removing):

	uv lock

- Sync environment to the lockfile:

	uv sync

## Best practices for this repository

- Keep service configuration as module-level constants.
- Use explicit request timeouts for all network calls.
- Call raise_for_status on HTTP responses before using response data.
- Keep functions small and focused on one responsibility.
- Mock external API calls in unit tests to keep tests fast and deterministic.
- Run both tests and lint checks before committing.
- Commit both pyproject.toml and uv.lock whenever dependencies change.
- Prefer type hints for function signatures.

## Typical workflow

1. Pull latest changes.
2. Run uv sync.
3. Implement changes.
4. Run uv run python -m unittest -v.
5. Run uv run pylint emotion_detection.py test_emotion_detection.py.
6. Commit code and dependency metadata updates together.
