"""Emotion detection module backed by Watson NLP EmotionPredict."""

import json

import requests

EMOTION_PREDICT_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTION_MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
REQUEST_TIMEOUT_SECONDS = 10


def emotion_detector(text_to_analyze: str) -> dict[str, float | str]:
    """Call Watson NLP EmotionPredict and return extracted emotion scores."""
    headers = {"grpc-metadata-mm-model-id": EMOTION_MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(
        EMOTION_PREDICT_URL,
        headers=headers,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    response_dict = json.loads(response.text)
    emotions = response_dict["emotionPredictions"][0]["emotion"]

    anger = emotions["anger"]
    disgust = emotions["disgust"]
    fear = emotions["fear"]
    joy = emotions["joy"]
    sadness = emotions["sadness"]

    emotion_scores = {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
        "dominant_emotion": dominant_emotion,
    }
