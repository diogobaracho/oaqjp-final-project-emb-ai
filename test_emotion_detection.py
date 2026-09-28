import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import (
    EMOTION_MODEL_ID,
    EMOTION_PREDICT_URL,
    REQUEST_TIMEOUT_SECONDS,
    emotion_detector,
)


class TestEmotionDetector(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_emotion_detector_returns_emotion_scores_and_dominant(self, mock_post):
        text_to_analyze = "I am very happy today"
        mock_response = Mock()
        mock_response.text = (
            '{"emotionPredictions":[{"emotion":{'
            '"anger":0.1,'
            '"disgust":0.05,'
            '"fear":0.2,'
            '"joy":0.6,'
            '"sadness":0.05'
            '}}]}'
        )
        mock_post.return_value = mock_response

        result = emotion_detector(text_to_analyze)

        self.assertEqual(
            result,
            {
                "anger": 0.1,
                "disgust": 0.05,
                "fear": 0.2,
                "joy": 0.6,
                "sadness": 0.05,
                "dominant_emotion": "joy",
            },
        )
        mock_post.assert_called_once_with(
            EMOTION_PREDICT_URL,
            headers={"grpc-metadata-mm-model-id": EMOTION_MODEL_ID},
            json={"raw_document": {"text": text_to_analyze}},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        mock_response.raise_for_status.assert_called_once_with()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_emotion_detector_raises_for_http_error(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP error")
        mock_post.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            emotion_detector("test")


if __name__ == "__main__":
    unittest.main()
