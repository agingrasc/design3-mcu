from src.python.robot.task.robotaction import IRobotAction


class FakeRobotAction(IRobotAction):
    def __init__(self, name):
        self.name = name

    def execute(self):
        print("Executing action: " + self.name)
