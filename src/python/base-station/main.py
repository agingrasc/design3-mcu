import requests
from flask import Flask, current_app
app = Flask(__name__)

@app.route('/')
def hello_world():
    return current_app.send_static_file('index.html')

URL = "http://localhost"
PORT = ":5000/"

#response = requests.post(URL + PORT + "goto-position")
#print(response.status_code)
#print(response.content)

app.run()
