from domain.pathfinding.grid import Grid
from domain.pathfinding.pathfinding import PathFinding


def find(obstacles, width, length, robot_position, destination):
    grid = Grid(width, length)

    for obstacle in obstacles:
        grid.add_obstacle(obstacle)

    robot_coordinate = grid.game_board[robot_position.x][robot_position.y]
    destination_coordinate = grid.game_board[destination.x][destination.y]
    pathfinder = PathFinding(grid, robot_coordinate,
                             destination_coordinate)
    return pathfinder.find_path()
