import sys
import collections
from enum import Enum
from . import position

ObstacleValueObject = collections.namedtuple('ObstacleValueObject',
                                             'pos_x pos_y radius tag')


class Tag(Enum):
    OBSTACLE = 'X'
    CAN_PASS = ' '
    ROBOT = 'R'
    CANT_PASS_RIGHT = "OCPR"
    CANT_PASS_LEFT = "OCPL"
    PATH = 'O'


class GameBoard:
    def __init__(self, width, length, obstacles):
        self.width = width
        self.length = length
        self.robot_coordinate = Coordinate(0, 0)
        self.game_board = []
        self.__build_board()
        for obstacle in obstacles:
            self.__add_obstacle(obstacle)

    def set_robot_position(self, pos_x, pos_y):
        self.robot_coordinate.set_tag(Tag.CAN_PASS)
        self.robot_coordinate = self.game_board[pos_x][pos_y]
        self.robot_coordinate.set_tag(Tag.ROBOT)

    def print_game_board(self):
        for i in range(0, self.width):
            line = ""
            for j in range(0, self.length):
                line += self.game_board[i][j].get_tag().value
            print(line)

    def print_game_board_weight(self):
        for i in range(0, self.width):
            line = ""
            for j in range(0, self.length):
                if self.game_board[i][j].weight >= (sys.maxsize):
                    line += " X "
                else:
                    line += " " + str(self.game_board[i][j].weight) + " "
            print(line)

    def __build_board(self):
        for i in range(0, self.width):
            row = []
            for j in range(0, self.length):
                coord = Coordinate(i, j)
                if i == 0 or (i == self.width - 1) or j == 0 or (
                        j == self.length - 1):
                    coord.set_tag(Tag.OBSTACLE)
                row.append(coord)
            self.game_board.append(row)

    def __add_obstacle(self, obstacle_value_object):
        obstacles = build_obstacle(obstacle_value_object, self.width,
                                   self.length)
        for obstacle in obstacles:
            self.game_board[obstacle.pos_x][obstacle.pos_y] = obstacle


def build_obstacle(obstacle, width, length):
    obstacle_coord = []
    startx_pos = __verify_start_x(obstacle)
    starty_pos = __verify_start_y(obstacle)
    endx_pos = __verify_end_x(obstacle, width)
    endy_pos = __verify_end_y(obstacle, length)
    for i in range(startx_pos, endx_pos):
        for j in range(starty_pos, endy_pos):
            new_obstacle_coord = Coordinate(i, j)
            new_obstacle_coord.set_tag(Tag.OBSTACLE)
            new_obstacle_coord.set_weight(sys.maxsize)
            obstacle_coord.append(new_obstacle_coord)
    return obstacle_coord


def __verify_start_x(obstacle):
    startx_pos = obstacle.pos_x - obstacle.radius
    if startx_pos < 0 or obstacle.tag == Tag.CANT_PASS_LEFT:
        startx_pos = 0
    return startx_pos


def __verify_end_x(obstacle, width):
    endx_pos = obstacle.pos_x + obstacle.radius
    if endx_pos > width - 1 or obstacle.tag == Tag.CANT_PASS_RIGHT:
        endx_pos = width - 1
    return endx_pos


def __verify_end_y(obstacle, length):
    endy_pos = obstacle.pos_y + obstacle.radius
    if endy_pos > length - 1:
        endy_pos = length - 1
    return endy_pos


def __verify_start_y(obstacle):
    starty_pos = obstacle.pos_y - obstacle.radius
    if starty_pos < 0:
        starty_pos = 0
    return starty_pos


class Coordinate(position.Position):
    def __init__(self, pos_x, pos_y):
        position.Position.__init__(self, pos_x, pos_y)
        self.tag = Tag.CAN_PASS
        self.weight = -1

    def set_tag(self, new_tag):
        self.tag = new_tag
        if self.tag == Tag.OBSTACLE:
            self.weight = sys.maxsize

    def set_weight(self, weight):
        if self.tag == Tag.OBSTACLE:
            self.weight = sys.maxsize
        else:
            self.weight = weight

    def set_path(self):
        self.tag = Tag.PATH

    def get_tag(self):
        return self.tag
