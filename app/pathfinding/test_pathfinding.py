import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from . import pathfinding
from app.gameboard.gameboard import GameBoard
from app.gameboard.gameboard import ObstacleBuilder
from app.gameboard.gameboard import ObstacleValueObject
from app.gameboard.gameboard import Tag
from app.pathfinding.graph import Grid

WIDTH = 4
LENGHT = 4


class PathFindingTest(unittest.TestCase):
    def test_initialize_weight(self):
        grid = create_grid(2, 2)
        neighbors = []
        neighbors.append(Mock(pos_x=0, pos_y=0, weight=1))
        neighbors.append(Mock(pos_x=0, pos_y=1, weight=1))
        neighbors.append(Mock(pos_x=1, pos_y=0, weight=1))
        neighbors.append(Mock(pos_x=1, pos_y=1, weight=1))
        begin_position = Mock(pos_x=1, pos_y=1, weight=-1)
        grid.neighbors = MagicMock(return_value=neighbors)
        pathfinding.initialise_weight(grid, begin_position)

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
        begin_position = grid.game_board[0][0]
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
        board = GameBoard(50, 55, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        end_position = grid.game_board[8][45]
        begin_position = grid.game_board[0][0]
        end_position.set_weight(0)

        pathfinder = pathfinding.PathFinding()
        pathfinder.find(grid, begin_position, end_position)
        board.print_game_board()

def create_grid(width, length):
    table = []
    for i in range(0, width):
        row = []
        for j in range(0, length):
            coord = Mock(pos_x=i, pos_y=j, weight=-1)
            row.append(coord)
        table.append(row)
    game_board = Mock(width=width, length=length, game_board=table)
    grid = MagicMock(game_board=game_board)
    return grid
