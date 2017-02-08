from flask import Blueprint, request, make_response, jsonify

go_to_position = Blueprint('go-to-position', __name__)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    pos_x = request.json["x"]
    pos_y = request.json["y"]
    print(pos_x)
    print(pos_y)
    return make_response(jsonify({'x': pos_x, 'y': pos_y}), 200)
