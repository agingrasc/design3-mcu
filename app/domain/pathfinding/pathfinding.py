import sys
from app.domain.gameboard.position import Position
from app.domain.gameboard.gameboard import Tag
from .grid import Grid


class PathFinding:
    def __init__(self, game_board, begin_position, end_position):
        self.grid = Grid(game_board)
        self.begin_position = begin_position
        self.end_position = end_position
        self.end_position.set_weight(0)

    def find_path(self):
        initialise_weight(self.grid, self.end_position)
        return find(self.grid, self.begin_position, self.end_position)


def find(grid, begin_position, end_position):
    path = []
    current_neighbor = begin_position
    while current_neighbor.weight > 0:
        neighbors = grid.neighbors(current_neighbor)
        new_neighbors = removed_already_visited_neighbors(neighbors, path)
        current_neighbor = find_minimum(new_neighbors)
        current_neighbor.set_path()
        path.append(current_neighbor)
    return path


def find_minimum(neighbors):
    if len(neighbors) <= 0:
        raise Exception("Cannot find path")
    current_neighbor = neighbors[0]
    for neighbor in neighbors:
        if neighbor.weight < current_neighbor.weight:
            current_neighbor = neighbor
    return current_neighbor


def removed_already_visited_neighbors(neighbors, path):
    new_neighbors = []
    for neighbor in neighbors:
        if neighbor not in path:
            new_neighbors.append(neighbor)
    return new_neighbors


def initialise_weight(grid, begin_position):
    neighbors = set(grid.neighbors(begin_position))
    next_neighbors = []
    while len(neighbors) > 0:
        for neighbor in neighbors:
            if neighbor.weight == -1:
                tmp_neibhbors = [
                    x for x in grid.neighbors(neighbor)
                    if x.weight != -1 and x.weight != sys.maxsize
                ]
                new_weight = find_minimum(tmp_neibhbors).weight + 1
                neighbor.set_weight(new_weight)
                next_neighbors.append(neighbor)
        neighbors = []
        for next_neighbor in next_neighbors:
            new_neighbors = [
                x for x in grid.neighbors(next_neighbor) if x.weight == -1
            ]
            neighbors += new_neighbors
        neighbors = set(neighbors)
