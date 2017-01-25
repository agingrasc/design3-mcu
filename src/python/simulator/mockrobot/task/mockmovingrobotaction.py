from src.python.robot.task.robotaction import IRobotAction


class MockMovingRobotAction(IRobotAction):
    def __init__(self, to_position, wheel_service):
        self.wheel_service = wheel_service
        self.to_position = to_position

    def execute(self):
        self.wheel_service.go_to(self.to_position)
