from unittest import TestCase
from app.gameboard.gameboard import GameBoard
from app.gameboard.gameboard import Coordinate
from app.gameboard.gameboard import ObstacleBuilder
from app.gameboard.gameboard import ObstacleValueObject
from app.gameboard.gameboard import Tag
from app.pathfinding.graph import Grid
from . import pathfinding

class PathFindingTest(TestCase):
    def test_already_visited_neighbors(self):
        coord1 = Coordinate(1, 0)
        coord2 = Coordinate(2, 0)
        coord3 = Coordinate(3, 0)
        coord4 = Coordinate(4, 0)
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

    def test_initialise_weight_one_obstacle(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(pos_x=4, pos_y=9, radius=1, tag='')
        obstacle_builder.add_obtacle(obstacle)
        board = GameBoard(13, 13, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        end_position = grid.game_board[1][1]
        end_position.set_weight(0)

        pathfinding.initialise_weight(grid, end_position, 1)
        board.print_game_board_weight()

    def test_initialise_weight_no_obstacle(self):
        obstacle_builder = ObstacleBuilder()
        board = GameBoard(6, 6, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        end_position = grid.game_board[2][2]
        end_position.set_weight(0)

        pathfinding.initialise_weight(grid, end_position, 1)
        board.print_game_board_weight()

    def test_find_no_obstacle(self):
        obstacle_builder = ObstacleBuilder()
        board = GameBoard(6, 6, obstacle_builder)

        grid = Grid(board)
        board.print_game_board()
        end_position = grid.game_board[2][2]
        begin_position = grid.game_board[5][5]
        end_position.set_weight(0)

        pathfinding.initialise_weight(grid, end_position, 5)
        pathfinding.find(grid, begin_position, end_position)
        board.print_game_board_weight()
        board.print_game_board()

    def test_find_ajust_obstacle(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(
            pos_x=14, pos_y=19, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle_builder.add_obtacle(obstacle)
        board = GameBoard(30, 55, obstacle_builder)

        grid = Grid(board)
        end_position = grid.game_board[8][50]
        begin_position = grid.game_board[2][2]
        end_position.set_weight(0)

        pathfinding.initialise_weight(grid, end_position, 55)
        pathfinding.ajust_left_obstacle(grid, Coordinate(14,19), 3,30 ,55)
        pathfinding.find(grid, begin_position, end_position)
        board.print_game_board()
        board.print_game_board_weight()

    def test_find_1_obstacle(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(
            pos_x=14, pos_y=19, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle_builder.add_obtacle(obstacle)
        board = GameBoard(30, 55, obstacle_builder)

        grid = Grid(board)
        end_position = grid.game_board[8][50]
        begin_position = grid.game_board[2][2]
        end_position.set_weight(0)

        pathfinding.initialise_weight(grid, end_position, 55)
        pathfinding.find(grid, begin_position, end_position)
        board.print_game_board()
        board.print_game_board_weight()

    def test_find_2_obstacle(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(
            pos_x=14, pos_y=19, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle_builder.add_obtacle(obstacle)
        obstacle2 = ObstacleValueObject(
            pos_x=5, pos_y=39, radius=3, tag=Tag.CANT_PASS_RIGHT)
        obstacle_builder.add_obtacle(obstacle2)
        board = GameBoard(30, 55, obstacle_builder)

        grid = Grid(board)
        end_position = grid.game_board[8][50]
        begin_position = grid.game_board[2][2]
        end_position.set_weight(0)

        pathfinding.initialise_weight(grid, end_position, 55)
        pathfinding.find(grid, begin_position, end_position)
        board.print_game_board()
        board.print_game_board_weight()

    def test_find_ajust_2_obstacle(self):
        obstacle_builder = ObstacleBuilder()
        obstacle = ObstacleValueObject(
            pos_x=14, pos_y=19, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle_builder.add_obtacle(obstacle)
        obstacle2 = ObstacleValueObject(
            pos_x=5, pos_y=39, radius=3, tag=Tag.CANT_PASS_RIGHT)
        obstacle_builder.add_obtacle(obstacle2)
        board = GameBoard(30, 55, obstacle_builder)

        grid = Grid(board)
        end_position = grid.game_board[8][50]
        begin_position = grid.game_board[2][2]
        end_position.set_weight(0)

        pathfinding.initialise_weight(grid, end_position, 55)
        pathfinding.ajust_left_obstacle(grid, Coordinate(14,19), 3,30 ,55)
        pathfinding.ajust_right_obstacle(grid, Coordinate(5,39), 3,30 ,55)
        pathfinding.find(grid, begin_position, end_position)
        board.print_game_board()
        board.print_game_board_weight()
