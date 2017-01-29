from app.gameboard import position


TAG_ROBOT = 'R'
TAG_PICTURE = 'P'
TAG_OBSTACLE = 'X'
TAG_CAN_PASS = ' '
TAG_CANT_PASS_RIGHT = "OCPR"
TAG_CANT_PASS_LEFT = "OCPL"


class GameBoard:

    def __init__(self, width, length, obstacle_builder):
        self.width = width
        self.length = length
        self.robot_coordinate = Coordinate(0, 0)
        self.pos_pictures = []
        self.game_board = []
        self.__build_board()
        self.__add_obstacles(obstacle_builder)

    def set_robot_position(self, pos_x, pos_y):
        self.robot_coordinate.set_tag(TAG_CAN_PASS)
        self.robot_coordinate = self.game_board[pos_x][pos_y]
        self.robot_coordinate.set_tag(TAG_ROBOT)

    def print_game_board(self):
        for i in range(0, self.width):
            line = ""
            for j in range(0, self.length):
                line += self.game_board[i][j].get_signe()
            print(line)

    def __build_board(self):
        for i in range(0, self.width):
            row = []
            for j in range(0, self.length):
                coord = Coordinate(i, j)
                if i == 0 or (i == self.width - 1) or j == 0 or (j == self.length - 1):
                    coord.set_tag(TAG_OBSTACLE)
                row.append(coord)
            self.game_board.append(row)

    def __add_obstacles(self, obstacle_builder):
        obstacles = obstacle_builder.build(self.width, self.length)
        for obstacle in obstacles:
            self.game_board[obstacle.pos_x][obstacle.pos_y] = obstacle


class ObstacleBuilder:

    def __init__(self):
        self.obstacles = []

    def add_obtacle(self, obstacle_value_object):
        self.obstacles.append(obstacle_value_object)

    def build(self, width, length):
        obstacle_coord = []
        for obstacle in self.obstacles:
            startx_pos = self.__verify_start_x(obstacle)
            starty_pos = self.__verify_start_y(obstacle)
            endx_pos = self.__verify_end_x(obstacle, width)
            endy_pos = self.__verify_end_y(obstacle, length)
            for i in range(startx_pos, endx_pos):
                for j in range(starty_pos, endy_pos):
                    new_obstacle_coord = Coordinate(i, j)
                    new_obstacle_coord.set_tag(TAG_OBSTACLE)
                    obstacle_coord.append(new_obstacle_coord)

        return obstacle_coord

    def __verify_start_x(self, obstacle):
        startx_pos = obstacle.pos_x - obstacle.radius
        if startx_pos < 0 or obstacle.tag == TAG_CANT_PASS_LEFT:
            startx_pos = 0
        return startx_pos

    def __verify_end_x(self, obstacle, width):
        endx_pos = obstacle.pos_x + obstacle.radius
        if endx_pos > width - 1 or obstacle.tag == TAG_CANT_PASS_RIGHT:
            endx_pos = width - 1
        return endx_pos

    def __verify_end_y(self, obstacle, length):
        endy_pos = obstacle.pos_y + obstacle.radius
        if endy_pos > length - 1:
            endy_pos = length - 1
        return endy_pos

    def __verify_start_y(self, obstacle):
        starty_pos = obstacle.pos_y - obstacle.radius
        if starty_pos < 0:
            starty_pos = 0
        return starty_pos


class ObstacleValueObject:

    def __init__(self, pos_x, pos_y, radius, tag=''):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius + 1
        self.tag = tag


class Coordinate(position.Position):

    def __init__(self, pos_x, pos_y):
        position.Position.__init__(self, pos_x, pos_y)
        self.tag = TAG_CAN_PASS

    def set_tag(self, new_tag):
        self.tag = new_tag

    def get_signe(self):
        if self.tag == TAG_ROBOT:
            return TAG_ROBOT
        elif self.tag == TAG_PICTURE:
            return TAG_PICTURE
        elif self.tag == TAG_OBSTACLE:
            return TAG_OBSTACLE
        else:
            return TAG_CAN_PASS
