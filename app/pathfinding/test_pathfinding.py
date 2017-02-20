import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from . import pathfinding
from app.gameboard.gameboard import GameBoard
from app.gameboard.gameboard import ObstacleBuilder
from app.gameboard.gameboard import ObstacleValueObject
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

    def test_funfun(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(
            pos_x=4,
            pos_y=9,
            radius=1,
            tag='')
        #obstacle_builder.add_obtacle(obstacle)
        board = GameBoard(13, 13, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        begin_position = grid.game_board[0][0]
        begin_position.set_weight(0)
        print("first x " + str(begin_position.pos_x)+" Fist y :"  + str(begin_position.pos_y))
        pathfinding.initialise_weight(grid, begin_position)
        board.print_game_board_weight()
        print("BEGIN" + str(begin_position.weight))






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
