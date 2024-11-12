from flask import Flask, jsonify
import json
app = Flask(__name__)


@app.route("/")
def home():
    return "task tracker"


@app.route("/tasks")
def tasks():
    x = ""
    with open("tasks.json", "r") as f:
        data = json.load(f)
    #for i in data:
        #x += f"{i["date"]} {["time"]}: {i["task"]}\n"

    return jsonify(data)