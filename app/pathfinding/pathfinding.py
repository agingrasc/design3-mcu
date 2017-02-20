


class PathFinding:
    def __init__(self):
        pass

    def find(self, grid, begin_position, end_position):
        initialise_weight(grid, end_position)
        path = []
        current_neighbor = begin_position
        while current_neighbor.weight > 0:
            print("x: " + str(current_neighbor.pos_x) + " y : " + str(current_neighbor.pos_y))
            neighbors = grid.neighbors(current_neighbor)
            new_neighbors = removed_already_visited_neighbors(neighbors, path)
            current_neighbor = find_minimum(new_neighbors)
            current_neighbor.set_path()
            path.append(current_neighbor)
        return path


def find_minimum(neighbors):
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

def compare_coord(coord1, coord2):
    if coord1.pos_x != coord2.pos_x:
        return False
    if coord2.pos_y != coord2.pos_y:
        return False

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
