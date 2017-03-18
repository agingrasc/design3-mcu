import sys
import queue
from domain.gameboard.position import Position
from domain.gameboard.gameboard import Tag
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
    neighbors = queue.Queue()
    neighbors.put(begin_position)
    while not neighbors.empty():
        neighbor = neighbors.get()
        new_neighbors = grid.neighbors(neighbor)
        for new_neighbor in new_neighbors:
            if new_neighbor.weight == -1:
                new_neighbor.set_weight(neighbor.weight + 1)
                neighbors.put(new_neighbor)
