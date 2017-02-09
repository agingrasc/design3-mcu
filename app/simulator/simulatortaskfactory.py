from ..robot.task.task import Task
from .mockrobot.task.fakerobotaction import FakeRobotAction


class SimulatorTaskFactory:

    def create_task_for_competition(self):
        task = Task()

        task.register(FakeRobotAction("find antenna"))
        task.register(FakeRobotAction("mark antenna position"))
        task.register(FakeRobotAction("find drawing"))
        task.register(FakeRobotAction("picture drawing"))
        task.register(FakeRobotAction("go in drawing zone"))
        task.register(FakeRobotAction("draw in zone"))
        task.register(FakeRobotAction("exit drawing zone"))
        task.register(FakeRobotAction("turn red light on"))
        task.register(FakeRobotAction("standby"))

        return task
