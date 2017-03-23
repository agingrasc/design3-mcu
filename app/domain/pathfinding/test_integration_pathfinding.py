import sys
from unittest import TestCase
from domain.gameboard.gameboard import Coordinate
from domain.gameboard.gameboard import ObstacleValueObject
from domain.gameboard.gameboard import Tag
from domain.gameboard.gameboard import GameBoard
from . import pathfinding
from .grid import Grid
from domain.pathfinding import get_segments


class PathFindingITest(TestCase):
    def test_initialise_weight_one_obstacle(self):
        obstacle = ObstacleValueObject(
            pos_x=4, pos_y=9, radius=2, tag=Tag.CANT_PASS_LEFT)
        game_board = GameBoard(13, 13, [obstacle])
        grid = Grid(game_board)

        end_position = grid.game_board[1][1]
        begin_position = grid.game_board[10][10]

        pathfinder = pathfinding.PathFinding(grid, begin_position,
                                             end_position)
        pathfinding.initialise_weight(grid, end_position)
        game_board.print_game_board_weight()

    def test_initialise_weight_no_obstacle(self):
        game_board = GameBoard(6, 6, [])
        grid = Grid(game_board)

        end_position = grid.game_board[1][1]
        begin_position = grid.game_board[2][2]
        pathfinder = pathfinding.PathFinding(grid, begin_position,
                                             end_position)

        pathfinding.initialise_weight(grid, end_position)
        game_board.print_game_board_weight()

    def test_find_no_obstacle(self):
        game_board = GameBoard(6, 6, [])

        end_position = game_board.game_board[2][2]
        begin_position = game_board.game_board[5][5]
        game_board.print_game_board()

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)
        self.validate_path(pathfinder.find_path())
        game_board.print_game_board_weight()
        game_board.print_game_board()

    def test_find_obstacle(self):
        obstacle = ObstacleValueObject(pos_x=5, pos_y=19, radius=3, tag='')
        game_board = GameBoard(30, 55, [obstacle])

        end_position = game_board.game_board[8][50]
        begin_position = game_board.game_board[2][2]

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)
        pathfinder.find_path()
        self.validate_path(pathfinder.find_path())
        game_board.print_game_board()

    def test_find_left_obstacle(self):
        obstacle = ObstacleValueObject(
            pos_x=14, pos_y=19, radius=3, tag=Tag.CANT_PASS_LEFT)
        game_board = GameBoard(30, 55, [obstacle])

        end_position = game_board.game_board[8][50]
        begin_position = game_board.game_board[2][2]

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)
        self.validate_path(pathfinder.find_path())
        game_board.print_game_board()

    def test_find_extrem_left_right_obstacles(self):
        obstacle1 = ObstacleValueObject(
            pos_x=25, pos_y=19, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle2 = ObstacleValueObject(
            pos_x=5, pos_y=39, radius=3, tag=Tag.CANT_PASS_RIGHT)
        game_board = GameBoard(30, 55, [obstacle1, obstacle2])

        end_position = game_board.game_board[8][50]
        begin_position = game_board.game_board[2][2]

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)
        self.validate_path(pathfinder.find_path())
        game_board.print_game_board()

    def test_find_left_rightx2_obstacles(self):
        obstacle1 = ObstacleValueObject(
            pos_x=25, pos_y=8, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle2 = ObstacleValueObject(
            pos_x=5, pos_y=39, radius=3, tag=Tag.CANT_PASS_RIGHT)
        obstacle3 = ObstacleValueObject(
            pos_x=5, pos_y=19, radius=3, tag=Tag.CANT_PASS_RIGHT)
        game_board = GameBoard(30, 55, [obstacle1, obstacle2, obstacle3])

        end_position = game_board.game_board[8][50]
        begin_position = game_board.game_board[2][2]

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)
        self.validate_path(pathfinder.find_path())
        game_board.print_game_board()

    def validate_path(self, path):
        new_path = get_segments.get_filter_path(path)
        for pp in new_path:
            print(pp)
        previous_weight = sys.maxsize
        for position in path:
            self.assertTrue(previous_weight > position.weight)
        self.assertTrue(path[len(path) - 1].weight == 0)
