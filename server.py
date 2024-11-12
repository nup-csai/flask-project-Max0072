from flask import Flask, jsonify
import json
app = Flask(__name__)


@app.route("/")
def home():
    return "task tracker"
@app.route("/tasks")
def tasks():
    with open("tasks.json", "r") as f:
        task = json.load(f)

    return task

