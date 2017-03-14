import time
import json
from websocket import create_connection
from mcu.robotcontroller import robot_controller, set_move_destination
from domain.gameboard.position import Position
from mcu.commands import regulator

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
        self.connection.send(json.dumps(data))
        robot_position_json = self.connection.recv()
        print("########DEBUG######\n" + str(robot_position_json))

        robot_position_info = json.loads(robot_position_json)
        pos_x = float(robot_position_info['x'])
        pos_y = float(robot_position_info['y'])
        robot_position = Position(int(pos_x), int(pos_y))
        set_move_destination(position)

        now = time.time()
        last_time = time.time()
        print("Starting position regulator loop!!!")

        while not regulator._is_arrived(robot_position):
            now = time.time()
            if now - last_time > DELTA_T:
                last_time = time.time()
                self.connection.send(json.dumps(data))

                robot_position_json = self.connection.recv()
                robot_position_info = json.loads(robot_position_json)
                pos_x = float(robot_position_info['x'])
                pos_y = float(robot_position_info['y'])
                print("Trying to move, actual position: {} -- {}".format(pos_x, pos_y))
                robot_position = Position(int(pos_x), int(pos_y))

                robot_controller.send_move_command(robot_position)


vision_regulator = VisionRegulation()
