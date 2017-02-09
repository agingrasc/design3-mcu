import collections


class Node:

    def __init__(self, pos_x, pos_y, weight, heuristic):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.weight = weight
        self.heuristic = heuristic
        self.accessible_node = []

    def has_bigger_heuristic(self, node):
        if self.heuristic < node.heuristic:
            return True
        return False

    def has_same_heuristic(self, node):
        if self.heuristic == node.heuristic:
            return True
        return False

    def get_accessible_nodes(self):
        return self.accessible_node

    def add_accessible_node(self, node):
        self.accessible_node.append(node)


def astar(begin_node, end_node):
    frontier = collections.deque()
    frontier.append(begin_node)
    visited = {}
    visited[begin_node] = True
    while not (len(frontier) == 0):
        current = frontier.popleft()
        if current == end_node:
            return visited
        for next_node in current.get_accessible_nodes():
            if next_node not in visited:
                frontier.append(next_node)
                visited[next_node] = True
    return visited
