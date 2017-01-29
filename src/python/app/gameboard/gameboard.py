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
        self.__world_board = []
        for i in range(0, max_x):
            row = []
            for j in range(0, max_y):
                coord = Coordonate(i, j)
                row.append(coord)
                if i == 0 or (i == self.max_x - 1) or j == 0 or (j == self.max_y - 1):
                    coord.set_tag(TAG_OBSTACLE)
            self.__world_board.append(row)

        self.__pos_pictures = []

    def set_position_robot(self, pos_x, pos_y):
        self.robot_coordonate.set_tag(TAG_CAN_PASS)
        self.robot_coordonate = self.__world_board[pos_x][pos_y]
        self.robot_coordonate.set_tag(TAG_ROBOT)

    def get_coordonate(self, pos_x, pos_y):
        return self.__world_board[pos_x][pos_y]

    def set_obstacle(self, pos_x, pos_y, rayon, tag=""):
        rayon += 1
        startx_pos = pos_x - rayon
        endx_pos = pos_x + rayon
        starty_pos = pos_y - rayon
        endy_pos = pos_y + rayon

        if startx_pos < 0 or tag == TAG_CANT_PASS_LEFT:
            startx_pos = 0
        if endx_pos > self.max_x - 1 or tag == TAG_CANT_PASS_RIGHT:
            endx_pos = self.max_x - 1

        if starty_pos < 0:
            starty_pos = 0
        if endy_pos > self.max_y - 1:
            endy_pos = self.max_y - 1

        for i in range(startx_pos, endx_pos):
            for j in range(starty_pos, endy_pos):
                obj = self.__world_board[i][j]
                obj.set_tag(TAG_OBSTACLE)

    def print_game_board(self):
        for i in range(0, self.max_x):
            line = ""
            for j in range(0, self.max_y):
                line += self.__world_board[i][j].get_signe()
            print(line)


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
