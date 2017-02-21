from app.pathfinding.grid import Grid
from app.pathfinding.pathfinding import PathFinding


def find(obstacles, width, length, robot_position, destination):
    grid = Grid(width, length)
    robot_coordinate = grid.game_board[robot_position.x][robot_position.y]
    destination_coordinate = grid.game_board[destination.x][destination.y]
    pathfinder = PathFinding(grid, robot_coordinate,
                             destination_coordinate)
    for obstacle in obstacles:
        pathfinder.add_obstacle(obstacle)
    return pathfinder.find_path()
