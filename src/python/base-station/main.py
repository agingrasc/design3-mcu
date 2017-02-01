import json
import requests
from flask import Flask, current_app
app = Flask(__name__)

URL = "http://localhost"
PORT = ":5000/"

@app.route('/')
def hello_world():
    return current_app.send_static_file('index.html')

@app.route("/goto-position")
def goto_position():
    #response = requests.post(URL + PORT + "goto-position")
    #print(response.status_code)
    #print(response.content)
    return json.dumps("Goto position"), 200

app.run()
