import json
import requests as req
from flask import Flask, request, current_app
app = Flask(__name__)

ROBOT_API_URL = "http://localhost:5000/"
PORT = 12345


@app.route('/')
def hello_world():
    return current_app.send_static_file('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


@app.route("/go-to-position/", methods=['POST'])
def goto_position():
    pos_x = request.form['x']
    pos_y = request.form['y']
    print(pos_x)
    print(pos_y)
    response = req.post(ROBOT_API_URL + "go-to-position")
    print(response.status_code)
    print(response.content)
    print(response.content[0])
    print(response.content[1])
    return json.dumps("succeed"), 200

app.run(port=PORT)
