import unittest
from app.domain.gameboard import gameboard

VALID_ROBOT_X_POSITION = 11
VALID_ROBOT_Y_POSITION = 22
VALID_OBSTACLE_X_POSITION = 7
VALID_OBSTACLE_Y_POSITION = 15
VALID_MAX_X = 15
VALID_MAX_Y = 30
VALID_RADIUS = 3


class GameBoardTest(unittest.TestCase):
    def test_init_pos_unique(self):
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [])

        for i in range(0, VALID_MAX_X):
            for j in range(0, VALID_MAX_Y):
                coord = board.game_board[i][j]
                self.assertEqual(i, coord.pos_x)
                self.assertEqual(j, coord.pos_y)

    def test_set_notag_obstacle(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS,
            tag='')
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle])

        max_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS - 1
        min_x = VALID_OBSTACLE_X_POSITION - VALID_RADIUS - 1
        lim_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS

        coord_max_x = board.game_board[max_x][VALID_OBSTACLE_Y_POSITION]
        coord_min_x = board.game_board[min_x][VALID_OBSTACLE_Y_POSITION]
        coord_lim_x = board.game_board[lim_x][VALID_OBSTACLE_Y_POSITION]

        self.assertEqual(gameboard.Tag.CAN_PASS, coord_min_x.get_signe())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_x.get_signe())
        self.assertEqual(gameboard.Tag.CAN_PASS, coord_lim_x.get_signe())

    def test_set_left_obstacle(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS,
            tag=gameboard.Tag.CANT_PASS_LEFT)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle])

        max_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS - 1
        min_x = VALID_OBSTACLE_X_POSITION - VALID_RADIUS - 1
        lim_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS

        coord_max_x = board.game_board[max_x][VALID_OBSTACLE_Y_POSITION]
        coord_min_x = board.game_board[min_x][VALID_OBSTACLE_Y_POSITION]
        coord_lim_x = board.game_board[lim_x][VALID_OBSTACLE_Y_POSITION]

        self.assertEqual(gameboard.Tag.OBSTACLE, coord_min_x.get_signe())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_x.get_signe())
        self.assertEqual(gameboard.Tag.CAN_PASS, coord_lim_x.get_signe())

    def test_set_right_obstacle(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS,
            tag=gameboard.Tag.CANT_PASS_RIGHT)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle])

        max_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS - 1
        min_x = VALID_OBSTACLE_X_POSITION - VALID_RADIUS - 1
        lim_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS

        coord_max_x = board.game_board[max_x][VALID_OBSTACLE_Y_POSITION]
        coord_min_x = board.game_board[min_x][VALID_OBSTACLE_Y_POSITION]
        coord_lim_x = board.game_board[lim_x][VALID_OBSTACLE_Y_POSITION]

        self.assertEqual(gameboard.Tag.CAN_PASS, coord_min_x.get_signe())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_x.get_signe())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_lim_x.get_signe())
