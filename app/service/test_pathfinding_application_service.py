from unittest import TestCase
from unittest.mock import Mock
from . import pathfinding_application_service
from domain.gameboard.position import Position


class PathFindingApplicationServiceTest(TestCase):
    def test_speed(self):
        robot_position = Position(10, 20)
        destination_position = Position(79, 150)
        pathfinding_application_service.find([], 100, 200, robot_position,
                                             destination_position)
