from flask import Blueprint, request, make_response, jsonify

from mcu.robotcontroller import robot_controller

led_ok = Blueprint('led-ok', __name__)


@led_ok.route('/led-ok', methods=['POST'])
def go_to_position_():
    robot_controller.startup_test()
    return make_response(jsonify({'result': 'ok'}), 200)

