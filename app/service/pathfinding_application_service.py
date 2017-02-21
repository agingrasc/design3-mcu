from app.gameboard import gameboard
from app.pathfinding import grid
from app.pathfinding import pathfinding

class PathFindingApplicationService:
    def __init__(self):
        pass

    def find(self, robot_position, obstacles, width, length):
        obstacle_builder = gameboard.ObstacleBuilder()
        for obstacle in obstacles:
            obstacle_builder.add_obtacle(obstacle)
        game_board = gameboard.GameBoard(width, length, obstacle_builder)

