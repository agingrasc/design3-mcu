import math


class Position:

    def __init__(self, pos_x, pos_y):
        self.__pos_x = pos_x
        self.__pos_y = pos_y

    def to_string(self):
        return "(" + str(self.__pos_x) + ", " + str(self.__pos_y) + ")"

    def get_pos_x(self):
        return self.__pos_x

    def get_pos_y(self):
        return self.__pos_y

    def get_distance(self):
        return math.sqrt(float(self.__pos_x**2) + float(self.__pos_y**2))

    def get_angle(self):
        return math.atan(float(self.__pos_y) / float(self.__pos_x))

    def set_pos_x(self, pos_x):
        self.__pos_x = pos_x

    def set_pos_y(self, pos_y):
        self.__pos_y = pos_y
