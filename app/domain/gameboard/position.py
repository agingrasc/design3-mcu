import math


class Position:
    def __init__(self, pos_x = 0, pos_y = 0, theta = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.theta = theta

    def __str__(self):
        return "x: {} -- y: {} -- theta: {}".format(self.pos_x, self.pos_y, self.theta)

    def get_norm(self):
        return math.sqrt(float(self.pos_x**2) + float(self.pos_y**2))

    def get_angle(self):
        return math.atan(float(self.pos_y) / float(self.pos_x))

