from flask import Flask
import json
app = Flask(__name__)


@app.route("/")
def home():
    return "task tracker"


@app.route("/tasks")
def tasks():
    with open("tasks.json", "r") as f:
        data = json.load(f)
    y = data[0]["task"]
    x = data[1]["task"]
    return y, x
