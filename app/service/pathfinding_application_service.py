from domain.pathfinding.grid import Grid
from domain.pathfinding.pathfinding import PathFinding
from domain.gameboard.gameboard import GameBoard


def find(obstacles, width, length, robot_position, destination):
    game_board = GameBoard(width, length, [])
    grid = Grid(game_board)

    robot_coordinate = grid.game_board[robot_position.pos_x][robot_position.pos_y]
    destination_coordinate = grid.game_board[destination.pos_x][destination.pos_y]
    pathfinder = PathFinding(grid, robot_coordinate,
                             destination_coordinate)
    return pathfinder.find_path()
