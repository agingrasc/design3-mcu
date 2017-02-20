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


def initialise_weight(grid, begin_position, increment_size):
    neighbors = set(grid.neighbors(begin_position))
    next_weight = begin_position.weight + increment_size
    next_neighbors = []
    while len(neighbors) > 0:
        for neighbor in neighbors:
            if neighbor.weight == -1:
                neighbor.set_weight(next_weight)
                next_neighbors.append(neighbor)
        neighbors = []
        for next_neighbor in next_neighbors:
            new_neighbors = [
                x for x in grid.neighbors(next_neighbor) if x.weight == -1
            ]
            neighbors += new_neighbors
        next_weight += increment_size
        neighbors = set(neighbors)

def ajust_left_obstacle(grid, position, radius, width, length):
    x_position = position.pos_x + radius
    y_min_position = position.pos_y - radius
    y_max_position = position.pos_y + radius
    for x in range(x_position):
        increment = x_position - x
        for y in range(y_max_position, y_max_position + x_position - x):
            if y >= 0 and x >= 0 and x < width and y <length:
                node = grid.game_board[x][y]
                node.set_weight(node.weight + increment)
                increment -= 1
        increment = x_position - x
        for y in range(y_min_position, y_min_position - x_position + x, -1):
            if y >= 0 and x >= 0 and x < width and y <length:
                node = grid.game_board[x][y]
                ajust_one_node(node, increment)
                increment -= 1

def ajust_right_obstacle(grid, position, radius, width, length):
    x_position = position.pos_x - radius-1
    y_min_position = position.pos_y - radius
    y_max_position = position.pos_y + radius
    for x in range(width, x_position, -1):
        increment = x - x_position
        for y in range(y_max_position, y_max_position + x - x_position):
            print(y)
            if y >= 0 and x >= 0 and x < width and y <length:
                node = grid.game_board[x][y]
                ajust_one_node(node, increment)
                increment -= 1
        increment = x - x_position
        for y in range(y_min_position, y_min_position - x + x_position, -1):
            if y >= 0 and x >= 0 and x < width and y <length:
                node = grid.game_board[x][y]
                ajust_one_node(node, increment)
                increment -= 1

def ajust_one_node(node, ajustement):
    if node.weight != 0:
        node.set_weight(node.weight + ajustement)

