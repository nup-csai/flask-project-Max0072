from flask import Flask
import json
app = Flask(__name__)


@app.route("/")
def home():
    return "inferior task tracker"


@app.route("/tasks")
def home():
    data = json.load(open("tasks.json"))
    x = data[0]("task")
    return x
