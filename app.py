from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)
sentiment_pipeline = pipeline("sentiment-analysis")

def sentiment_color(sentiment_label):
    if sentiment_label == "POSITIVE":
        return "green"
    elif sentiment_label == "NEGATIVE":
        return "red"
    else:
        return "gray"

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment_result = None
    analysis_text = ""
    color = "black"

    if request.method == "POST":
        analysis_text = request.form["user_text"].strip()
        if analysis_text:
            result = sentiment_pipeline(analysis_text)[0]
            sentiment_result = result["label"]
            confidence = result["score"]
            color = sentiment_color(sentiment_result)
            sentiment_result = f"{sentiment_result} (Confidence: {confidence:.2f})"
        else:
            sentiment_result = "Please enter some text to analyze!"
            color = "orange"

    return render_template(
        "index.html",
        analysis=sentiment_result,
        user_text=analysis_text,
        color=color
    )

if __name__ == "__main__":
    app.run(debug=True)
