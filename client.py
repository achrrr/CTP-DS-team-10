from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    headline = request.form["content"]
    return render_template("index.html", classification="fake")


if __name__ == "__main__":
    app.run(debug=True)
