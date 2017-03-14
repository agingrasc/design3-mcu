from app.mcu.commands import Move


class CommandController:
    def __init__(self, robot_controller):
        self.robot_controller = robot_controller

    def move_to_position(self, angle, position):
        x = position.pos_x
        y = position.pos_y
        command = Move(x, y, angle)
        self.robot_controller.send_command(command)
