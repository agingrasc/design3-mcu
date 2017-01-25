from src.python.map.position import Position
from src.python.robot.robot import Robot
from src.python.robot.task.task import Task
from src.python.simulator.mockrobot.task.mockmovingrobotaction import MockMovingRobotAction
from src.python.simulator.mockrobot.wheel.wheelservice import MockWheelService


class Simulator:
    def start(self):
        print("Starting simulator...")
        wheel_service = MockWheelService()
        robot = Robot()

        task = Task()
        next_position = Position(10, 100)

        task.register(MockMovingRobotAction(next_position, wheel_service))

        robot.execute_task(task)
