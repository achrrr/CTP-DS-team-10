from flask import Flask, render_template, request, redirect
from model import predict

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    headline = request.form["content"]
    pred = predict(headline).get("predicted_class")
    return render_template("index.html", classification="Fake" if pred == 1 else "True")


if __name__ == "__main__":
    app.run(debug=True)
