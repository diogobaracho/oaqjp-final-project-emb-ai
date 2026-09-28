"""

For this project, you'll use the Emotion Predict function of the Watson NLP Library. For accessing this function, the URL, the headers, and the input json format is as follows.


# URL: 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
# Headers: {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
# Input json: { "raw_document": { "text": text_to_analyze } }

"""

import requests

EMOTION_PREDICT_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTION_MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
REQUEST_TIMEOUT_SECONDS = 10


def emotion_detector(text_to_analyze: str) -> str:
    """Call Watson NLP EmotionPredict and return the response text payload."""
    headers = {"grpc-metadata-mm-model-id": EMOTION_MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(
        EMOTION_PREDICT_URL,
        headers=headers,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.text
