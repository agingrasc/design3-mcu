import unittest

from .commands import regulator
from domain.gameboard.position import Position


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.null_position = Position()

    def tearDown(self):
        pass

    def test_zero_regulator(self):
        regulator.set_point = self.null_position
        exp_cmd = [0, 0, 0]
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)

    def test_deadzone_regulator(self):
        regulator.set_point = Position(10, 10, 0)
        exp_cmd = [0, 0, 0]
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)

    def test_saturation_regulator(self):
        regulator.set_point = Position(200, 200, 0)
        exp_cmd = [80, 80, 0]
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)

    def test_negative_saturation_regulator(self):
        regulator.set_point = Position(-200, 0, 0)
        exp_cmd = [-80, 0, 0]
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)