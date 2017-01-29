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

    def test_init_pos_unique(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)

        for i in range(0, self.valid_max_x):
            for j in range(0, self.valid_max_y):
                coord = board.get_coordonate(i, j)
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
                    self.assertNotEqual(board.get_coordonate(i, j).tag, gameboard.TAG_ROBOT)

    def test_set2_obstacle_x(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        rayon = 2

        board.set_obstacle(self.valid_obstacle_x_position, self.valid_obstacle_y_position, rayon)

        obj_max_x = board.get_coordonate(self.valid_obstacle_x_position + rayon,
                                         self.valid_obstacle_y_position)
        obj_min_x = board.get_coordonate(1,
                                         self.valid_obstacle_y_position)
        obj_lim_x = board.get_coordonate(self.valid_obstacle_x_position + rayon + 1,
                                         self.valid_obstacle_y_position)
        self.assertEqual(gameboard.TAG_CAN_PASS, obj_min_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_max_x.get_signe())
        self.assertEqual(gameboard.TAG_CAN_PASS, obj_lim_x.get_signe())

    def test_set3_left_obstacle_x(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        rayon = 3

        board.set_obstacle(
            self.valid_obstacle_x_position,
            self.valid_obstacle_y_position,
            rayon,
            gameboard.TAG_CANT_PASS_LEFT)

        obj_max_x = board.get_coordonate(self.valid_obstacle_x_position + rayon,
                                         self.valid_obstacle_y_position)
        obj_min_x = board.get_coordonate(1,
                                         self.valid_obstacle_y_position)
        obj_lim_x = board.get_coordonate(self.valid_obstacle_x_position + rayon + 1,
                                         self.valid_obstacle_y_position)
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_min_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_max_x.get_signe())
        self.assertEqual(gameboard.TAG_CAN_PASS, obj_lim_x.get_signe())

    def test_set3_right_obstacle_y(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        rayon = 3

        board.set_obstacle(
            self.valid_obstacle_x_position,
            self.valid_obstacle_y_position,
            rayon,
            gameboard.TAG_CANT_PASS_RIGHT)

        obj_max_y = board.get_coordonate(self.valid_obstacle_x_position,
                                         self.valid_obstacle_y_position + rayon)
        obj_min_y = board.get_coordonate(self.valid_max_x - 1,
                                         self.valid_obstacle_y_position - rayon)
        obj_lim_y = board.get_coordonate(self.valid_obstacle_x_position,
                                         self.valid_obstacle_y_position + rayon + 1)
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_min_y.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_max_y.get_signe())
        self.assertEqual(gameboard.TAG_CAN_PASS, obj_lim_y.get_signe())
