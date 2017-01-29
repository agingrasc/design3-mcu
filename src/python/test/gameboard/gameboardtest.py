import unittest
from app.gameboard import gameboard


class GameBoardTest(unittest.TestCase):

    def setUp(self):
        self.valid_robot_x_position = 11
        self.valid_robot_y_position = 22
        self.valid_obstacle_x_position = 7
        self.valid_obstacle_y_position = 15
        self.valid_max_x = 15
        self.valid_max_y = 30
        self.valid_radius = 3

    def test_init_pos_unique(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)

        for i in range(0, self.valid_max_x):
            for j in range(0, self.valid_max_y):
                coord = board.game_board[i][j]
                self.assertEqual(i, coord.pos_x)
                self.assertEqual(j, coord.pos_y)

    def test_set_robot_pos(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        board.set_position_robot(self.valid_robot_x_position, self.valid_robot_y_position)

        self.assertEqual(self.valid_robot_x_position,
                         board.robot_coordonate.pos_x)
        self.assertEqual(self.valid_robot_y_position,
                         board.robot_coordonate.pos_y)

    def test_set_robot_unique(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        board.set_position_robot(self.valid_robot_x_position, self.valid_robot_y_position)

        for i in range(0, self.valid_max_x):
            for j in range(0, self.valid_max_y):
                if i != self.valid_robot_x_position or j != self.valid_robot_y_position:
                    self.assertNotEqual(board.game_board[i][j].tag, gameboard.TAG_ROBOT)

    def test_set_notag_obstacle(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        board.set_obstacle(self.valid_obstacle_x_position,
                           self.valid_obstacle_y_position, self.valid_radius)

        max_x = self.valid_obstacle_x_position + self.valid_radius
        min_x = 1
        lim_x = self.valid_obstacle_x_position + self.valid_radius + 1

        coord_max_x = board.game_board[max_x][self.valid_obstacle_y_position]
        coord_min_x = board.game_board[min_x][self.valid_obstacle_y_position]
        coord_lim_x = board.game_board[lim_x][self.valid_obstacle_y_position]

        self.assertEqual(gameboard.TAG_CAN_PASS, coord_min_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, coord_max_x.get_signe())
        self.assertEqual(gameboard.TAG_CAN_PASS, coord_lim_x.get_signe())

    def test_set_left_obstacle(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        board.set_obstacle(
            self.valid_obstacle_x_position,
            self.valid_obstacle_y_position,
            self.valid_radius,
            gameboard.TAG_CANT_PASS_LEFT)

        max_x = self.valid_obstacle_x_position + self.valid_radius
        min_x = 1
        lim_x = self.valid_obstacle_x_position + self.valid_radius + 1

        coord_max_x = board.game_board[max_x][self.valid_obstacle_y_position]
        coord_min_x = board.game_board[min_x][self.valid_obstacle_y_position]
        coord_lim_x = board.game_board[lim_x][self.valid_obstacle_y_position]

        self.assertEqual(gameboard.TAG_OBSTACLE, coord_min_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, coord_max_x.get_signe())
        self.assertEqual(gameboard.TAG_CAN_PASS, coord_lim_x.get_signe())

    def test_set_right_obstacle(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        board.set_obstacle(
            self.valid_obstacle_x_position,
            self.valid_obstacle_y_position,
            self.valid_radius,
            gameboard.TAG_CANT_PASS_RIGHT)

        max_x = self.valid_obstacle_x_position + self.valid_radius
        min_x = 1
        lim_x = self.valid_obstacle_x_position + self.valid_radius + 1

        coord_max_x = board.game_board[max_x][self.valid_obstacle_y_position]
        coord_min_x = board.game_board[min_x][self.valid_obstacle_y_position]
        coord_lim_x = board.game_board[lim_x][self.valid_obstacle_y_position]

        self.assertEqual(gameboard.TAG_CAN_PASS, coord_min_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, coord_max_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, coord_lim_x.get_signe())
