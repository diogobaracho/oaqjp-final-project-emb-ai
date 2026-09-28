import unittest
from unittest.mock import patch

from server import app


class TestServerEmotionDetectorRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("server.emotion_detector")
    def test_emotion_detector_route_formats_required_response(self, mock_emotion_detector):
        mock_emotion_detector.return_value = {
            "anger": 0.006274985,
            "disgust": 0.0025598293,
            "fear": 0.009251528,
            "joy": 0.9680386,
            "sadness": 0.049744144,
            "dominant_emotion": "joy",
        }

        response = self.client.get(
            "/emotionDetector", query_string={"textToAnalyze": "I love my life"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "For the given statement, the system response is "
            "'anger': 0.006274985, "
            "'disgust': 0.0025598293, "
            "'fear': 0.009251528, "
            "'joy': 0.9680386 and "
            "'sadness': 0.049744144. "
            "The dominant emotion is <b>joy</b>.",
        )

    @patch("server.emotion_detector")
    def test_emotion_detector_route_formats_blank_input_response(self, mock_emotion_detector):
        mock_emotion_detector.return_value = {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

        response = self.client.get("/emotionDetector", query_string={"textToAnalyze": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "For the given statement, the system response is "
            "'anger': None, "
            "'disgust': None, "
            "'fear': None, "
            "'joy': None and "
            "'sadness': None. "
            "The dominant emotion is <b>None</b>.",
        )


if __name__ == "__main__":
    unittest.main()
