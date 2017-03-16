from flask import Blueprint, request, make_response, jsonify
from service import pathfinding_application_service
from domain.gameboard.position import Position
from domain.pathfinding import get_segments
from domain.command.commandcontroller import CommandController
from mcu import robotcontroller

from domain.gameboard.position import Position
from mcu.robotcontroller import robot_controller
from mcu.commands import regulator, MoveCommand
from mcu import protocol
from domain.command.visionregulation import vision_regulator

go_to_position = Blueprint('go-to-position', __name__)

commandcontroller = CommandController(robotcontroller.robot_controller)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        req_info = request.json
    except Exception as e:
        return make_response(jsonify(), 400)
    robot = req_info["robot"]
    robot_pos = robot['position']
    robot_x = robot_pos["x"]
    robot_y = robot_pos["y"]
    theta = robot_pos['theta']
    obstacles = req_info["obstacles"]
    width = req_info["width"]
    length = req_info["length"]
    robot_position = Position(robot_x, robot_y)
    destination = req_info["destination"]
    destination_x = int(float(destination["x"]))
    destination_y = int(float(destination["y"]))
    destination_position = Position(destination_x, destination_y, theta)
    #path = pathfinding_application_service.find(obstacles, width, length,
    #                                            robot_position, destination_position)
    #destinations = get_segments.get_filter_path(path)
    #for point in destinations:
    #    #vision_regulator.go_to_position(point)
    #    pass

    vision_regulator.go_to_position(destination_position)

    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y
        }), 200)
