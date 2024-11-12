from flask import Flask, jsonify
import json
app = Flask(__name__)


@app.route("/")
def home():
    return "task tracker"
@app.route("/tasks")
def tasks():
    with open("tasks.json", "r") as f:
        tas = json.load(f)
    task = ""
    for i in range(2):
        task += f"{tas[i]['date']}, {tas[i]['time']}, {tas[i]['task']} \n"

    return task

