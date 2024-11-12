from flask import Flask, jsonify
import json
app = Flask(__name__)


@app.route("/")
def home():
    return "task tracker"
@app.route("/tasks")
def tasks():
    return "tasks"

