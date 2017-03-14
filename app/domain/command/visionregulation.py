from websocket import create_connection


class VisionRegulation:
    def __init__(self):
        self.connection = None

    def set_url(self, url):
        self.connection = create_connection("ws://" + url + ":3000")

    def go_to_position(self, position):
        data = {}
        data["headers"] = "pull_robot_position"
        data["data"] = {}
        self.connection.send(data)
        robot_position = self.connection.recv()
