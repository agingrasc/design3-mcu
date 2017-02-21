import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
from app.pathfinding.grid import Grid
from app.gameboard.gameboard import Coordinate
from app.gameboard.gameboard import GameBoard

WIDTH = 50
LENGHT = 25

class GridTest(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(WIDTH, LENGHT)

    def test_no_extremity(self):
        test_position_x = 4
        test_position_y = 4
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y+1))
        self.assertEqual(8, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

    def test_top_left_corner(self):
        test_position_x = 0
        test_position_y = 0
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y+1))
        self.assertEqual(3, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

    def test_bottom_left_corner(self):
        test_position_x = 0
        test_position_y = LENGHT-1 
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y))
        self.assertEqual(3, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))


    def test_left_middle(self):
        test_position_x = 0
        test_position_y = 4
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y+1))
        self.assertEqual(5, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

    def test_top_right_corner(self):
        test_position_x = WIDTH -1
        test_position_y = 0
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y+1))
        self.assertEqual(3, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

    def test_top_middle(self):
        test_position_x = 4
        test_position_y = 0
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y+1))
        self.assertEqual(5, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

    def test_bottom_right_corner(self):
        test_position_x = WIDTH-1
        test_position_y = LENGHT-1
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y))
        self.assertEqual(3, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

    def test_right_middle(self):
        test_position_x = WIDTH-1
        test_position_y = 4
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y+1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y+1))
        self.assertEqual(5, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

    def test_bottom_middle(self):
        test_position_x = 4
        test_position_y = LENGHT-1
        position = Mock(pos_x=test_position_x, pos_y=test_position_y)
        neighbors = self.grid.neighbors(position)

        expected = []
        expected.append(Mock(pos_x=test_position_x, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x-1, pos_y=test_position_y))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y-1))
        expected.append(Mock(pos_x=test_position_x+1, pos_y=test_position_y))
        self.assertEqual(5, len(neighbors))
        self.assertTrue(containt_coord(expected, neighbors))

def compare_coord(coord1, coord2):
    if coord1.pos_x != coord2.pos_x:
        return False
    if coord2.pos_y != coord2.pos_y:
        return False
    return True

def containt_coord(coords1, coords2):
    for coord1 in coords1:
        containt = False
        for coord2 in coords2:
            if compare_coord(coord1, coord2):
                containt = True
        if not containt:
            return False
    return True
