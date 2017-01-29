from gameboard import position


TAG_ROBOT = 'R'
TAG_PICTURE = 'P'
TAG_OBSTACLE = 'X'
TAG_CAN_PASS = ' '
TAG_CANT_PASS_RIGHT = "OCPR"
TAG_CANT_PASS_LEFT = "OCPL"

class GameBoard:

    def __init__(self, max_x, max_y):
        self.__max_x = max_x
        self.__max_y = max_y
        self.__world_board = []
        self.robot_coordonate = Coordonate(0, 0)
        for i in range(0, max_x):
            row = []
            for j in range(0, max_y):
                coord = Coordonate(i, j)
                row.append(coord)
                if i == 0 or (i == self.__max_x - 1) or j == 0 or (j == self.__max_y - 1):
                    coord.set_obstacle()
            self.__world_board.append(row)

        self.__pos_pictures = []

    def set_position_robot(self, pos_x, pos_y):
        self.robot_coordonate.set_robot(False)
        self.robot_coordonate = self.__world_board[pos_x][pos_y]
        self.robot_coordonate.set_robot(True)

    def get_position_robot(self):
        return self.robot_coordonate

    def get_coordonate(self, pos_x, pos_y):
        return self.__world_board[pos_x][pos_y]

    def set_obstacle(self, pos_x, pos_y, rayon, tab=""):
        rayon += 1
        startx_pos = pos_x - rayon
        endx_pos = pos_x + rayon
        starty_pos = pos_y - rayon
        endy_pos = pos_y + rayon

        if startx_pos < 0 or tab == TAG_CANT_PASS_LEFT:
            startx_pos = 0
        if endx_pos > self.__max_x - 1 or tab == TAG_CANT_PASS_RIGHT:
            endx_pos = self.__max_x - 1

        if starty_pos < 0:
            starty_pos = 0
        if endy_pos > self.__max_y - 1:
            endy_pos = self.__max_y - 1

        for i in range(startx_pos, endx_pos):
            for j in range(starty_pos, endy_pos):
                obj = self.__world_board[i][j]
                obj.set_obstacle()

    def print_game_board(self):
        for i in range(0, self.__max_x):
            line = ""
            for j in range(0, self.__max_y):
                line += self.__world_board[i][j].get_signe()
            print(line)


class Coordonate(position.Position):

    def __init__(self, pos_x, pos_y):
        position.Position.__init__(self, pos_x, pos_y)
        self.__is_obstacle = False
        self.__is_robot = False
        self.__is_picture = False

    def is_robot(self):
        return self.__is_robot

    def set_robot(self, is_robot):
        self.__is_robot = is_robot
        self.__is_picture = False
        self.__is_obstacle = False

    def set_obstacle(self):
        self.__is_obstacle = True
        self.__is_robot = False
        self.__is_picture = False

    def get_signe(self):
        if self.__is_robot:
            return TAG_ROBOT
        elif self.__is_picture:
            return TAG_PICTURE
        elif self.__is_obstacle:
            return TAG_OBSTACLE
        else:
            return TAG_CAN_PASS
