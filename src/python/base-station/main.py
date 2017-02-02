import json
import requests
from flask import Flask, current_app
app = Flask(__name__)

ROBOT_API_URL = "http://localhost:5000/"
PORT = 12345


@app.route('/')
def hello_world():
    return current_app.send_static_file('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


@app.route("/go-to-position")
def goto_position():
    response = requests.post(ROBOT_API_URL + "go-to-position")
    print(response.status_code)
    print(response.content)
    return json.dumps("succeed"), 200

app.run(port=PORT)
