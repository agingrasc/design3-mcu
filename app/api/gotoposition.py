from flask import Blueprint, request, make_response, jsonify

from domain.gameboard.position import Position
from mcu.robotcontroller import robot_controller
from mcu.commands import regulator, MoveCommand
from mcu import protocol

go_to_position = Blueprint('go-to-position', __name__)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        req_info = request.json
    except Exception as e:
        return make_response(jsonify(), 400)
    pos_x = req_info['x']
    pos_y = req_info['y']
    theta = req_info['theta']

    pos = Position(pos_x, pos_y, theta)
    regulator.setpoint = pos

    return make_response(jsonify({'x': int(pos.pos_x), 'y': int(pos_y)}), 200)


