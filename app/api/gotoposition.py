from flask import Blueprint, request, make_response, jsonify

from ..mcu.robotcontroller import robot_controller
from ..mcu.commands import regulator, Move
from ..mcu import protocol

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

    print("Reception (theta actuel): {}, {}".format(pos_x, pos_y, theta))
    regulator.set_point(tuple(pos_x, pos_y, 0))
    x, y, t = regulator.next_speed_command(tuple(0, 0, theta))
    set_motor_speed(x, y)
    print("Vitesse calcule: {}, {}".format(x, y))
    return make_response(jsonify({'x': pos_x, 'y': pos_y}), 200)


def set_motor_speed(speed_x, speed_y):
    x_motors = (protocol.Motors.FRONT_X, protocol.Motors.REAR_X)
    y_motors = (protocol.Motors.FRONT_Y, protocol.Motors.REAR_Y)
    if speed_x < 0:
        dir_x = protocol.MotorsDirection.BACKWARD
    else:
        dir_x = protocol.MotorsDirection.FORWARD
    if speed_y < 0:
        dir_y = protocol.MotorsDirection.BACKWARD
    else:
        dir_y = protocol.MotorsDirection.FORWARD
    for motor_id in x_motors:
        robot_controller.ser.write(protocol.generate_manual_speed_command(motor_id, speed_x, dir_x))
    for motor_id in y_motors:
        robot_controller.ser.write(protocol.generate_manual_speed_command(motor_id, speed_y, dir_y))


