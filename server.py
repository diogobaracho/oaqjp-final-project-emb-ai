"""Flask entrypoint for the emotion detection web application."""

from flask import Flask, request, render_template

from EmotionDetection import emotion_detector

app = Flask("Emotion Detection")


@app.route("/")
def render_index_page() -> str:
	"""Render the main application page."""
	return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route() -> str:
	"""Analyze input text and return a formatted response string."""
	text_to_analyze = request.args.get("textToAnalyze", "")
	response = emotion_detector(text_to_analyze)

	return (
		"For the given statement, the system response is "
		f"'anger': {response['anger']}, "
		f"'disgust': {response['disgust']}, "
		f"'fear': {response['fear']}, "
		f"'joy': {response['joy']} and "
		f"'sadness': {response['sadness']}. "
		f"The dominant emotion is <b>{response['dominant_emotion']}</b>."
	)


if __name__ == "__main__":
	app.run(host="127.0.0.1", port=5000)
