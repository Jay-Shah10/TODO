import random

from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/roll", methods=["POST"])
def roll():
    result = random.randint(1, 6)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
