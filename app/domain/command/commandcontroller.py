from domain.gameboard.position import Position


class CommandController:
    def __init__(self, robot_controller):
        self.robot_controller = robot_controller

    def move_to_position(self, angle, position):
        x = position.pos_x
        y = position.pos_y
        pos = Position(x, y, 0)
        self.robot_controller.send_move_command(pos)
