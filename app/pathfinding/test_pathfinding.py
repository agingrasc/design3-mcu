import unittest
import math
from unittest.mock import MagicMock
from app.gameboard.position import Position
from . import pathfinding


class PathFindingTest(unittest.TestCase):
    def setUp(self):
        self.begin_position = Position(0, 0)
        self.end_position = Position(0, 0)
        self.pathfinding = pathfinding.PathFinding(8)

    def test_define_intervals(self):
        self.begin_position.get_distance_with = MagicMock(return_value=16)
        self.begin_position.get_angle = MagicMock(return_value=40)
        self.end_position.get_angle = MagicMock(return_value=90)

        actual = self.pathfinding.define_intervals(self.begin_position, self.end_position)

        expected = 25
        self.assertEqual(expected, actual)

    def test_check_intervale(self):
        self.end_position.get_distance = MagicMock(return_value=13)
        self.begin_position.get_angle = MagicMock(return_value=(40/360)*(2*math.pi))
        self.end_position.get_angle = MagicMock(return_value=(90/360)*(2*math.pi))
        deltat_1 = (31/360)*(2*math.pi)
        print(deltat_1)
        print(deltat_1*360/(2*math.)

        actual = self.pathfinding.check_intervale(self.begin_position, self.end_position, deltat_1)



