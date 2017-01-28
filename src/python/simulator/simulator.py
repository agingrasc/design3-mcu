from map.position import Position
from robot.robot import Robot
from robot.task.task import Task
from simulator.mockrobot.task.mockmovingrobotaction import MockMovingRobotAction
from simulator.mockrobot.wheel.wheelservice import MockWheelService


class Simulator:

    def __init__(self):
        pass

    def start(self):
        print("Starting simulator...")
        wheel_service = MockWheelService()
        robot = Robot()

        task = Task()
        next_position = Position(10, 100)

        task.register(MockMovingRobotAction(next_position, wheel_service))

        robot.execute_task(task)

    def hello(self):
        pass
