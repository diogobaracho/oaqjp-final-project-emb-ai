# Final project

This repository contains a small Python Flask exercise for emotion detection using the Watson NLP EmotionPredict endpoint.

## Usage & Examples

### 1. Quick REPL test

Use the function directly from a Python shell:

```bash
uv run python
```

```python
>>> from EmotionDetection.emotion_detection import emotion_detector
>>> emotion_detector("I love this new technology.")
{'anger': 0.01, 'disgust': 0.00, 'fear': 0.01, 'joy': 0.97, 'sadness': 0.05, 'dominant_emotion': 'joy'}
```

Note: the function returns a Python dictionary with five emotion scores and `dominant_emotion`.

### 2. Use the returned dictionary

The returned dictionary is ready to use directly:

```python
from EmotionDetection.emotion_detection import emotion_detector

payload = emotion_detector("I love this new technology.")

print(payload["joy"])
print(payload["dominant_emotion"])
```

Example output shape:

```json
{
  "anger": 0.01,
  "disgust": 0.0,
  "fear": 0.01,
  "joy": 0.97,
  "sadness": 0.05,
  "dominant_emotion": "joy"
}
```

### 3. Blank input behavior

When the upstream service returns HTTP 400 (for example, when the input is blank),
the function returns a dictionary with `None` for every field.

```python
from EmotionDetection.emotion_detection import emotion_detector

print(emotion_detector(""))
```

```python
{
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}
```

### 4. Handle network and HTTP errors

The function calls `raise_for_status()`, so failed HTTP responses raise an exception.

```python
import requests
from EmotionDetection.emotion_detection import emotion_detector

try:
    print(emotion_detector("This is a test."))
except requests.HTTPError as err:
    print(f"API returned an HTTP error: {err}")
except requests.RequestException as err:
    print(f"Network or request error: {err}")
```

### 5. Try multiple inputs quickly

```python
from EmotionDetection.emotion_detection import emotion_detector

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

- EmotionDetection/: Package directory
- EmotionDetection/emotion_detection.py: Emotion detection client function
- EmotionDetection/__init__.py: Public package exports
- emotion_detection.py: Backward-compatible import wrapper
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

    uv run pylint EmotionDetection/emotion_detection.py emotion_detection.py server.py test_emotion_detection.py test_server.py

## PyLint guide

Use PyLint regularly during development and before every commit.

1. Run PyLint on all project Python files:

    uv run pylint EmotionDetection/emotion_detection.py emotion_detection.py server.py test_emotion_detection.py test_server.py

2. Run tests after linting:

    uv run python -m unittest -v

3. Treat PyLint warnings as actionable items and fix them before marking work done.

## Run the server and test with curl

1. Start the Flask server:

    uv run python server.py

2. In another terminal, test the endpoint with curl:

    curl "http://localhost:5000/emotionDetector?textToAnalyze=I%20think%20I%20am%20having%20fun"

curl --get \
--data-urlencode "textToAnalyze=I think I am having fun" \
"http://localhost:5000/emotionDetector"

3. Expected response format:

    For the given statement, the system response is 'anger': <value>, 'disgust': <value>, 'fear': <value>, 'joy': <value> and 'sadness': <value>. The dominant emotion is <b><emotion></b>.

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
5. Run uv run pylint EmotionDetection/emotion_detection.py emotion_detection.py server.py test_emotion_detection.py test_server.py.
6. Commit code and dependency metadata updates together.
