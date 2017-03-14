import math


class Position:
    def __init__(self, pos_x = 0, pos_y = 0, theta = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.theta = theta

    def __str__(self):
        return "(" + str(self.pos_x) + ", " + str(self.pos_y) + ")"

    def get_norm(self):
        return math.sqrt(float(self.pos_x**2) + float(self.pos_y**2))

    def get_angle(self):
        return math.atan(float(self.pos_y) / float(self.pos_x))

    def str(self):
        print("x: " + str(self.pos_x) + " y : " + str(self.pos_y))
