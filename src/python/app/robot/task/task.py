from robot.task.robotaction import IRobotAction


class Task:
    def __init__(self):
        self.actions = []

    def execute(self):
        for action in self.actions:
            action.execute()

    def register(self, action):
        if not isinstance(action, IRobotAction):
            raise TypeError("You need to pass a mockrobot action")

        self.actions.append(action)
