import random

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/roll", methods=["POST"])
def roll():
    data = request.get_json(silent=True) or {}
    sides = data.get("sides", 6)
    if sides not in (6, 10, 12):
        return jsonify({"error": "Invalid die type"}), 400
    result = random.randint(1, sides)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
