from flask import Blueprint, request, make_response, jsonify

from mcu.robotcontroller import robot_controller
from mcu.commands import regulator, Move
from mcu import protocol

go_to_position = Blueprint('go-to-position', __name__)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        pos_x = request.json["x"]
        pos_y = request.json["y"]
        theta = request.json['theta']
    except Exception as e:
        return make_response(jsonify(), 400)

    regulator.set_point = pos_x, pos_y, 0
    x, y, t = regulator.next_speed_command([0, 0, theta])
    _set_motor_speed(x, y)
    return make_response(jsonify({'x': int(x), 'y': int(y)}), 200)


def _set_motor_speed(speed_x: int, speed_y: int):
    """"
    Methode utilitaire pour activer manuellement les moteur dans la bonne orientation.
    Args:
        :speed_x: Vitesse dans l'axe x en pourcentage de PWM [-100, 100], doit etre un entier
        :speed_y: Vitesse dans l'axe y ...
    Returns:
        None
    """
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
        robot_controller.ser.write(protocol.generate_manual_speed_command(motor_id, abs(speed_x), dir_x))
    for motor_id in y_motors:
        robot_controller.ser.write(protocol.generate_manual_speed_command(motor_id, abs(speed_y), dir_y))


