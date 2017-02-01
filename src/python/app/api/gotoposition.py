import json
from flask import Blueprint

goto_position = Blueprint('goto_position', __name__)


@goto_position.route('/goto-position', methods=['POST'])
def goto_position_():
    print("goto_position")
    return json.dumps("Goto position"), 200
