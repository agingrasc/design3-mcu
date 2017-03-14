from flask import Blueprint, request, make_response, jsonify
from app.service import pathfinding_application_service
from app.domain.gameboard.position import Position
from app.domain.pathfinding import get_segments
from app.domain.command.commandcontroller import CommandController
from app.mcu import robotcontroller

go_to_position = Blueprint('go-to-position', __name__)

commandcontroller = CommandController(robotcontroller.robot_controller)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    robot = request.json["robot"]
    robot_x = robot["x"]
    robot_y = robot["y"]
    obstacles = request.json["obstacles"]
    width = request["width"]
    length = request["length"]
    robot_position = Position(robot_x, robot_y)
    destination = request.json["destination"]
    destination_x = destination["x"]
    destination_y = destination["y"]
    destination_position = Position(destination_x, destination_y)
    path = pathfinding_application_service.find(obstacles, width, length,
                                                robot_position, destination)
    destinations = get_segments.get_filter_path(path)
    commandcontroller.move_to_position(destination_position, 2)
    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y
        }), 200)
