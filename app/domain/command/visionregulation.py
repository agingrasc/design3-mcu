import time
from websocket import create_connection
from app.mcu.robotcontroller import robot_controller, set_move_destination
from app.domain.gameboard.position import Position
from app.mcu.commands import regulator

DELTA_T = 0.1


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
        robot_position_info = self.connection.recv()

        robot_position = Position(robot_position_info["x"],
                                  robot_position_info["y"])
        set_move_destination(position)

        now = time.time()
        last_time = time.time()
        while regulator._is_arrived(robot_position):
            now = time.time()
            if now - last_time > DELTA_T:
                last_time = time.time()
                self.connection.send(data)
                robot_position_info = self.connection.recv()
                robot_position = Position(robot_position_info["x"],
                                          robot_position_info["y"])
                robot_controller.send_move_command(robot_position)


vision_regulator = VisionRegulation()
