class Grid:
    def __init__(self, game):
        self.game_board = game.game_board
        self.width = game.width
        self.length = game.length

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
