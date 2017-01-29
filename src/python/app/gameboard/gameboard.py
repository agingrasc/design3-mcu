from app.gameboard import position


TAG_ROBOT = 'R'
TAG_PICTURE = 'P'
TAG_OBSTACLE = 'X'
TAG_CAN_PASS = ' '
TAG_CANT_PASS_RIGHT = "OCPR"
TAG_CANT_PASS_LEFT = "OCPL"


class GameBoard:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.robot_coordonate = Coordonate(0, 0)
        self.game_board = []
        self.pos_pictures = []
        self.obtacles = []
        self.__build_board()

    def set_position_robot(self, pos_x, pos_y):
        self.robot_coordonate.set_tag(TAG_CAN_PASS)
        self.robot_coordonate = self.game_board[pos_x][pos_y]
        self.robot_coordonate.set_tag(TAG_ROBOT)

    def set_obstacle(self, pos_x, pos_y, radius, tag=""):
        new_obstacle = Obstacle(pos_x, pos_y, radius)
        new_obstacle.activate(self, tag)
        self.obtacles.append(new_obstacle)

    def print_game_board(self):
        for i in range(0, self.max_x):
            line = ""
            for j in range(0, self.max_y):
                line += self.game_board[i][j].get_signe()
            print(line)

    def __build_board(self):
        for i in range(0, self.max_x):
            row = []
            for j in range(0, self.max_y):
                coord = Coordonate(i, j)
                row.append(coord)
                if i == 0 or (i == self.max_x - 1) or j == 0 or (j == self.max_y - 1):
                    coord.set_tag(TAG_OBSTACLE)
            self.game_board.append(row)


class Obstacle(position.Position):

    def __init__(self, pos_x, pos_y, radius):
        position.Position.__init__(self, pos_x, pos_y)
        self.radius = radius + 1

    def activate(self, board, tag):
        startx_pos = self.__verify_start_x(tag)
        starty_pos = self.__verify_start_y()
        endx_pos = self.__verify_end_x(board, tag)
        endy_pos = self.__verify_end_y(board)

        for i in range(startx_pos, endx_pos):
            for j in range(starty_pos, endy_pos):
                obj = board.game_board[i][j]
                obj.set_tag(TAG_OBSTACLE)

    def __verify_start_x(self, tag):
        startx_pos = self.pos_x - self.radius
        if startx_pos < 0 or tag == TAG_CANT_PASS_LEFT:
            startx_pos = 0
        return startx_pos

    def __verify_end_x(self, board, tag):
        endx_pos = self.pos_x + self.radius
        if endx_pos > board.max_x - 1 or tag == TAG_CANT_PASS_RIGHT:
            endx_pos = board.max_x - 1
        return endx_pos

    def __verify_end_y(self, board):
        endy_pos = self.pos_y + self.radius
        if endy_pos > board.max_y - 1:
            endy_pos = board.max_y - 1
        return endy_pos

    def __verify_start_y(self):
        starty_pos = self.pos_y - self.radius
        if starty_pos < 0:
            starty_pos = 0
        return starty_pos


class Coordonate(position.Position):

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
