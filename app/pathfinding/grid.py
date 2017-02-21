from . import pathfinding
from app.gameboard import gameboard
from app.gameboard import position

class Grid:
    def __init__(self, game, destination):
        destination.set_weight(0)
        self.destination = destination
        self.game_board = game.game_board
        self.game = game
        self.width = game.width
        self.length = game.length
        increment_size = 1
        if self.length > self.width:
            increment_size = self.length
        else:
            increment_size = self.width
        pathfinding.initialise_weight(self, destination, increment_size)

    def add_obstacle(self, obstacle):
        self.game.add_obstacle(obstacle)
        if obstacle.tag == gameboard.Tag.CANT_PASS_LEFT:
            pathfinding.ajust_left_obstacle(self, position.Position(obstacle.pos_x, obstacle.pos_y), obstacle.radius, self.width, self.length)
        elif obstacle.tag == gameboard.Tag.CANT_PASS_RIGHT:
            pathfinding.ajust_right_obstacle(self, position.Position(obstacle.pos_x, obstacle.pos_y), obstacle.radius, self.width, self.length)


    def find_path(self, robot_position):
        return pathfinding.find(self, robot_position, self.destination)

    def neighbors(self, position):
        neighbors = []
        x_max = position.pos_x >= self.width - 1
        y_max = position.pos_y >= self.length - 1
        x_min = position.pos_x <= 0
        y_min = position.pos_y <= 0
        if y_min:
            neighbors.append(self.game_board[position.pos_x][position.pos_y+1])
            if x_max:
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y+1])
            elif x_min:
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y+1])
            else:
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y+1])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y+1])
        elif y_max:
            neighbors.append(self.game_board[position.pos_x][position.pos_y-1])
            if x_max:
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y-1])
            elif x_min:
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y-1])
            else:
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y-1])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y-1])
        elif x_min:
            neighbors.append(self.game_board[position.pos_x+1][position.pos_y])
            if y_max:
                neighbors.append(self.game_board[position.pos_x][position.pos_y-1])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y-1])
            elif y_min:
                neighbors.append(self.game_board[position.pos_x][position.pos_y+1])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y+1])
            else:
                neighbors.append(self.game_board[position.pos_x][position.pos_y-1])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y-1])
                neighbors.append(self.game_board[position.pos_x][position.pos_y+1])
                neighbors.append(self.game_board[position.pos_x+1][position.pos_y+1])
        elif x_max:
            neighbors.append(self.game_board[position.pos_x-1][position.pos_y])
            if y_max:
                neighbors.append(self.game_board[position.pos_x][position.pos_y-1])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y-1])
            elif y_min:
                neighbors.append(self.game_board[position.pos_x][position.pos_y+1])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y+1])
            else:
                neighbors.append(self.game_board[position.pos_x][position.pos_y-1])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y-1])
                neighbors.append(self.game_board[position.pos_x][position.pos_y+1])
                neighbors.append(self.game_board[position.pos_x-1][position.pos_y+1])
        else:
            neighbors.append(self.game_board[position.pos_x][position.pos_y-1])
            neighbors.append(self.game_board[position.pos_x][position.pos_y+1])
            neighbors.append(self.game_board[position.pos_x+1][position.pos_y-1])
            neighbors.append(self.game_board[position.pos_x+1][position.pos_y])
            neighbors.append(self.game_board[position.pos_x+1][position.pos_y+1])
            neighbors.append(self.game_board[position.pos_x-1][position.pos_y-1])
            neighbors.append(self.game_board[position.pos_x-1][position.pos_y])
            neighbors.append(self.game_board[position.pos_x-1][position.pos_y+1])
        return neighbors
