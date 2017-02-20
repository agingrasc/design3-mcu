import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from . import pathfinding
from app.gameboard.gameboard import GameBoard
from app.gameboard.gameboard import Coordinate
from app.gameboard.gameboard import ObstacleBuilder
from app.gameboard.gameboard import ObstacleValueObject
from app.gameboard.gameboard import Tag
from app.pathfinding.graph import Grid

WIDTH = 4
LENGHT = 4


class PathFindingTest(unittest.TestCase):

    def test_already_visited_neighbors(self):
        coord1 = Coordinate(1,0)
        coord2 = Coordinate(2,0)
        coord3 = Coordinate(3,0)
        coord4 = Coordinate(4,0)
        array1 = []
        array1.append(coord1)
        array1.append(coord2)
        array1.append(coord3)
        array1.append(coord4)
        
        array2 = []
        array2.append(coord1)
        array2.append(coord2)
        
        array3 = pathfinding.removed_already_visited_neighbors(array1, array2)
        self.assertEqual(array3[0], coord3)
        self.assertEqual(array3[1], coord4)


    def test_integration1(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(
            pos_x=4,
            pos_y=9,
            radius=1,
            tag='')
        obstacle_builder.add_obtacle(obstacle)
        board = GameBoard(13, 13, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        begin_position = grid.game_board[1][1]
        begin_position.set_weight(0)
        
        pathfinding.initialise_weight(grid, begin_position)
        board.print_game_board_weight()



    def test_integration2(self):
        obstacle_builder = ObstacleBuilder()
        board = GameBoard(6, 6, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        begin_position = grid.game_board[2][2]
        begin_position.set_weight(0)

        pathfinding.initialise_weight(grid, begin_position)
        board.print_game_board_weight()


    def test_integration3(self):
        obstacle_builder = ObstacleBuilder()
        board = GameBoard(6, 6, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        end_position = grid.game_board[2][2]
        begin_position = grid.game_board[5][5]
        end_position.set_weight(0)

        pathfinder = pathfinding.PathFinding()
        path =pathfinder.find(grid, begin_position, end_position)
        board.print_game_board_weight()
        board.print_game_board()


    def test_integration4(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(
            pos_x=14,
            pos_y=19,
            radius=3,
            tag=Tag.CANT_PASS_LEFT)
        obstacle_builder.add_obtacle(obstacle)
        obstacle2 = ObstacleValueObject(
            pos_x=5,
            pos_y=39,
            radius=3,
            tag=Tag.CANT_PASS_RIGHT)
        obstacle_builder.add_obtacle(obstacle2)
        board = GameBoard(30, 55, obstacle_builder)

        grid = Grid(board)
        end_position = grid.game_board[8][50]
        begin_position = grid.game_board[2][2]
        end_position.set_weight(0)

        pathfinder = pathfinding.PathFinding()
        pathfinder.find(grid, begin_position, end_position)
        board.print_game_board()

