from unittest import TestCase
from . import pathfinding
from app.domain.gameboard.gameboard import Coordinate


class PathFindingITest(TestCase):
    def test_already_visited_neighbors(self):
        coord1 = Coordinate(1, 0)
        coord2 = Coordinate(2, 0)
        coord3 = Coordinate(3, 0)
        coord4 = Coordinate(4, 0)
        array1 = []
        array1.append(coord1)
        array1.append(coord2)
        array1.append(coord3)
        array1.append(coord4)

        array2 = []
        array2.append(coord1)
        array2.append(coord2)

        array3 = pathfinding.removed_already_visited_neighbors(array1, array2)
        self.assertEqual(array3[0], coord3)
        self.assertEqual(array3[1], coord4)
