"""Backward-compatible imports for the EmotionDetection package."""

from EmotionDetection.emotion_detection import (
    EMOTION_MODEL_ID,
    EMOTION_PREDICT_URL,
    REQUEST_TIMEOUT_SECONDS,
    emotion_detector,
)

__all__ = [
    "EMOTION_PREDICT_URL",
    "EMOTION_MODEL_ID",
    "REQUEST_TIMEOUT_SECONDS",
    "emotion_detector",
]
