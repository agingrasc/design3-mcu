import unittest
import math
from . import position


class PositionTest(unittest.TestCase):

    def setUp(self):
        self.a_valid_x = 5
        self.a_valid_y = 27
        self.a_valid_angle = math.pi

    def test_samexy_init(self):
        pos = position.Position(self.a_valid_x, self.a_valid_x)

        angle = math.atan(1.0)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_x**2))
        self.assertEqual(distance, pos.get_distance())
        self.assertEqual(angle, pos.get_angle())

    def test_differentxy_init(self):
        pos = position.Position(self.a_valid_x, self.a_valid_y)

        angle = math.atan(self.a_valid_y/self.a_valid_x)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_y**2))
        self.assertEqual(distance, pos.get_distance())
        self.assertEqual(angle, pos.get_angle())

    def test_samexy_setcartesian(self):
        pos = position.Position(self.a_valid_x, self.a_valid_x)

        pos.set_pos_y(self.a_valid_y)

        angle = math.atan(self.a_valid_y/self.a_valid_x)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_y**2))
        self.assertEqual(distance, pos.get_distance())
        self.assertEqual(angle, pos.get_angle())

    def test_samexy_setpolar(self):
        pos = position.Position(self.a_valid_x, self.a_valid_x)

        pos.set_angle(self.a_valid_angle)

        pos_x = self.calculate_pos_x(pos)
        pos_y = self.calculate_pos_y(pos)
        self.assertEqual(pos_x, pos.get_pos_x())
        self.assertEqual(pos_y, pos.get_pos_y())

    def test_differentxy_setcartesian(self):
        pos = position.Position(self.a_valid_x, self.a_valid_y)

        pos.set_pos_y(self.a_valid_x)

        angle = math.atan(1.0)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_x**2))
        self.assertEqual(distance, pos.get_distance())
        self.assertEqual(angle, pos.get_angle())

    def test_differentxy_setpolar(self):
        pos = position.Position(self.a_valid_x, self.a_valid_y)

        pos.set_angle(self.a_valid_angle)

        pos_x = self.calculate_pos_x(pos)
        pos_y = self.calculate_pos_y(pos)
        self.assertEqual(pos_x, pos.get_pos_x())
        self.assertEqual(pos_y, pos.get_pos_y())

    def calculate_pos_x(self, pos):
        return int(pos.get_distance() * math.cos(self.a_valid_angle))

    def calculate_pos_y(self, pos):
        return int(pos.get_distance() * math.sin(self.a_valid_angle))
