import math


class Position:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self):
        return "(" + str(self.pos_x) + ", " + str(self.pos_x) + ")"

    def get_distance(self):
        return math.sqrt(float(self.pos_x**2) + float(self.pos_y**2))

    def get_angle(self):
        return math.atan(float(self.pos_y) / float(self.pos_x))
