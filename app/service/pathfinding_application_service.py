from app.gameboard import gameboard
from app.pathfinding import grid
from app.pathfinding import pathfinding

class PathFindingApplicationService:
    def __init__(self):
        pass

    def find(self, robot_position, obstacles, width, length):
        board = gameboard.GameBoard(width, length)
        grid = grid.Grid(board)
        for obstacle in obstacles:
            board.add_obstacle
        game_board = gameboard.GameBoard(width, length, obstacle_builder)

