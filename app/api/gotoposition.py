from flask import Blueprint, request, make_response, jsonify

from ..mcu.robotcontroller import robot_controller
from ..mcu.commands import regulator, Move

go_to_position = Blueprint('go-to-position', __name__)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        pos_x = request.json["x"]
        pos_y = request.json["y"]
        theta = request.json['theta']
    except KeyError:
        print("mauvais payload")
        return make_response(jsonify(), 400)

    print(pos_x)
    print(pos_y)
    print(theta)
    regulator.set_point(tuple(pos_x, pos_y, 0))
    x, y, t = regulator.next_speed_command(tuple(0, 0, theta))
    move = Move(x, y, t)
    robot_controller.send_command(move)
    return make_response(jsonify({'x': pos_x, 'y': pos_y}), 200)
