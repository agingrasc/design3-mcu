import unittest
from app.gameboard import gameboard

VALID_ROBOT_X_POSITION = 11
VALID_ROBOT_Y_POSITION = 22
VALID_OBSTACLE_X_POSITION = 7
VALID_OBSTACLE_Y_POSITION = 15
VALID_MAX_X = 15
VALID_MAX_Y = 30
VALID_RADIUS = 3


class GameBoardTest(unittest.TestCase):

    def setUp(self):
        self.obstacle_builder = gameboard.ObstacleBuilder()

    def test_init_pos_unique(self):
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, self.obstacle_builder)

        for i in range(0, VALID_MAX_X):
            for j in range(0, VALID_MAX_Y):
                coord = board.game_board[i][j]
                self.assertEqual(i, coord.pos_x)
                self.assertEqual(j, coord.pos_y)

    def test_set_robot_pos(self):
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, self.obstacle_builder)
        board.set_robot_position(VALID_ROBOT_X_POSITION, VALID_ROBOT_Y_POSITION)

        self.assertEqual(VALID_ROBOT_X_POSITION,
                         board.robot_coordinate.pos_x)
        self.assertEqual(VALID_ROBOT_Y_POSITION,
                         board.robot_coordinate.pos_y)

    def test_set_robot_unique(self):
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, self.obstacle_builder)
        board.set_robot_position(VALID_ROBOT_X_POSITION, VALID_ROBOT_Y_POSITION)

        for i in range(0, VALID_MAX_X):
            for j in range(0, VALID_MAX_Y):
                if i != VALID_ROBOT_X_POSITION or j != VALID_ROBOT_Y_POSITION:
                    self.assertNotEqual(board.game_board[i][j].tag, gameboard.Tag.ROBOT)

    def test_set_notag_obstacle(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS,
            tag='')
        self.obstacle_builder.add_obtacle(obstacle)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, self.obstacle_builder)

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
        self.obstacle_builder.add_obtacle(obstacle)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, self.obstacle_builder)

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
        self.obstacle_builder.add_obtacle(obstacle)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, self.obstacle_builder)

        max_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS - 1
        min_x = VALID_OBSTACLE_X_POSITION - VALID_RADIUS - 1
        lim_x = VALID_OBSTACLE_X_POSITION + VALID_RADIUS

        coord_max_x = board.game_board[max_x][VALID_OBSTACLE_Y_POSITION]
        coord_min_x = board.game_board[min_x][VALID_OBSTACLE_Y_POSITION]
        coord_lim_x = board.game_board[lim_x][VALID_OBSTACLE_Y_POSITION]

        self.assertEqual(gameboard.Tag.CAN_PASS, coord_min_x.get_signe())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_x.get_signe())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_lim_x.get_signe())
