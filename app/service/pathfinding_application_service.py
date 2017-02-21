from app.gameboard import gameboard
from app.pathfinding import grid
from app.pathfinding import pathfinding

class PathFindingApplicationService:
    def __init__(self):
        pass

    def find(self, obstacles, width, length, robot_position, destination):
        board = gameboard.GameBoard(width, length)
        robot_coordinate = board.game_board[robot_position.x][robot_position.y]
        destination_coordinate = board.game_board[destination.x][destination.y]
        grid = grid.Grid(board, destination_coordinate)
        for obstacle in obstacles:
            grid.add_obstacle(obstacle)
        return grid.find_path(robot_position)
