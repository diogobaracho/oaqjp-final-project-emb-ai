import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import (
    EMOTION_MODEL_ID,
    EMOTION_PREDICT_URL,
    REQUEST_TIMEOUT_SECONDS,
    emotion_detector,
)


class TestEmotionDetectorResponse(unittest.TestCase):
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


class TestEmotionDetectorStatements(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_required_statements_dominant_emotions(self, mock_post):
        cases = [
            ("am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        ]

        score_by_emotion = {
            "anger": {
                "anger": 0.95,
                "disgust": 0.02,
                "fear": 0.01,
                "joy": 0.01,
                "sadness": 0.01,
            },
            "disgust": {
                "anger": 0.01,
                "disgust": 0.95,
                "fear": 0.01,
                "joy": 0.01,
                "sadness": 0.02,
            },
            "fear": {
                "anger": 0.01,
                "disgust": 0.01,
                "fear": 0.95,
                "joy": 0.01,
                "sadness": 0.02,
            },
            "joy": {
                "anger": 0.01,
                "disgust": 0.01,
                "fear": 0.01,
                "joy": 0.95,
                "sadness": 0.02,
            },
            "sadness": {
                "anger": 0.01,
                "disgust": 0.01,
                "fear": 0.02,
                "joy": 0.01,
                "sadness": 0.95,
            },
        }

        for statement, expected_dominant in cases:
            with self.subTest(statement=statement, expected_dominant=expected_dominant):
                emotions = score_by_emotion[expected_dominant]
                mock_response = Mock()
                mock_response.text = (
                    '{"emotionPredictions":[{"emotion":{'
                    f'"anger":{emotions["anger"]},'
                    f'"disgust":{emotions["disgust"]},'
                    f'"fear":{emotions["fear"]},'
                    f'"joy":{emotions["joy"]},'
                    f'"sadness":{emotions["sadness"]}'
                    '}}]}'
                )
                mock_post.return_value = mock_response

                result = emotion_detector(statement)

                self.assertEqual(result["dominant_emotion"], expected_dominant)
                self.assertEqual(
                    result,
                    {
                        "anger": emotions["anger"],
                        "disgust": emotions["disgust"],
                        "fear": emotions["fear"],
                        "joy": emotions["joy"],
                        "sadness": emotions["sadness"],
                        "dominant_emotion": expected_dominant,
                    },
                )


if __name__ == "__main__":
    unittest.main()
