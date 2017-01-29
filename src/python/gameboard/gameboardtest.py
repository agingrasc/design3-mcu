import unittest
from . import gameboard


class GameBoardTest(unittest.TestCase):

    def setUp(self):
        self.valid_robot_x_position = 11
        self.valid_robot_y_position = 22
        self.valid_obstacle_x_position = 7
        self.valid_obstacle_y_position = 15
        self.valid_max_x = 15
        self.valid_max_y = 30

    def test_set_robot(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        board.set_position_robot(self.valid_robot_x_position, self.valid_robot_y_position)
        self.assertEqual(self.valid_robot_x_position,
                         board.get_position_robot().get_pos_x())
        self.assertEqual(self.valid_robot_y_position,
                         board.get_position_robot().get_pos_y())

    def test_set2_obstacle(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        rayon = 2
        board.set_obstacle(self.valid_obstacle_x_position, self.valid_obstacle_y_position, rayon)
        obj_max_x = board.get_coordonate(self.valid_obstacle_x_position + rayon,
                                         self.valid_obstacle_y_position)
        obj_min_x = board.get_coordonate(1,
                                         self.valid_obstacle_y_position)
        obj_lim_x = board.get_coordonate(self.valid_obstacle_x_position + rayon + 1,
                                         self.valid_obstacle_y_position)
        board.print_game_board()
        self.assertEqual(gameboard.TAG_CAN_PASS, obj_min_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_max_x.get_signe())
        self.assertEqual(gameboard.TAG_CAN_PASS, obj_lim_x.get_signe())

    def test_set3_left_obstacle(self):
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
        board.print_game_board()
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_min_x.get_signe())
        self.assertEqual(gameboard.TAG_OBSTACLE, obj_max_x.get_signe())
        self.assertEqual(gameboard.TAG_CAN_PASS, obj_lim_x.get_signe())

    def test_just_for_fun(self):
        board = gameboard.GameBoard(self.valid_max_x, self.valid_max_y)
        rayon = 1
        board.set_obstacle(5, 26, rayon, gameboard.TAG_CANT_PASS_LEFT)
        board.set_obstacle(12, 16, rayon, gameboard.TAG_CANT_PASS_RIGHT)
        board.print_game_board()
