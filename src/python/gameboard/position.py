import math


class Position:

    def __init__(self, pos_x, pos_y):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__angle = 0
        self.__distance = 0
        self.__to_polar()

    def __str__(self):
        return "(" + str(self.__pos_x) + ", " + str(self.__pos_y) + ")"

    def get_pos_x(self):
        return self.__pos_x

    def get_pos_y(self):
        return self.__pos_y

    def get_distance(self):
        return self.__distance

    def get_angle(self):
        return self.__angle

    def set_distance(self, distance):
        self.__distance = distance
        self.__to_cartesian()

    def set_angle(self, angle):
        self.__angle = angle
        self.__to_cartesian()

    def set_pos_x(self, pos_x):
        self.__pos_x = pos_x
        self.__to_polar()

    def set_pos_y(self, pos_y):
        self.__pos_y = pos_y
        self.__to_polar()

    def __to_polar(self):
        self.__distance = math.sqrt(float(self.__pos_x**2) + float(self.__pos_y**2))
        self.__angle = math.atan(float(self.__pos_y) / float(self.__pos_x))

    def __to_cartesian(self):
        self.__pos_x = int(self.__distance * math.cos(self.__angle))
        self.__pos_y = int(self.__distance * math.sin(self.__angle))
