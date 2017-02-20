


class PathFinding:
    def __init__(self):
        pass

    def build_grid(self, grid, begin_position, end_position):
        initialise_weight(grid, begin_position)

def initialise_weight(grid, begin_position):
    neighbors = grid.neighbors(begin_position)
    next_weight = begin_position.weight +1
    next_neighbors = []
    while len(neighbors) > 0:
        for neighbor in neighbors:
            if neighbor.weight == -1:
                neighbor.set_weight(next_weight)
                next_neighbors.append(neighbor)
        neighbors = []
        for next_neighbor in next_neighbors:
            new_neighbors = [x for x in grid.neighbors(next_neighbor) if x.weight == -1]
            neighbors += new_neighbors
        next_weight += 1
        neighbors = set(neighbors)
