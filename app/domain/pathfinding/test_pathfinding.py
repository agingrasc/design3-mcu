from unittest import TestCase
from . import pathfinding
from app.domain.gameboard.gameboard import Coordinate
from unittest.mock import Mock


class PathFindingTest(TestCase):
    def test_already_visited_neighbors(self):
        coord1 = Mock(pos_x=1, pos_y=0)
        coord2 = Mock(pos_x=2, pos_y=0)
        coord3 = Mock(pos_x=3, pos_y=0)
        coord4 = Mock(pos_x=4, pos_y=0)
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

    def test_find_minimum(self):
        coord1 = Mock(weight=1)
        coord2 = Mock(weight=8)
        coord3 = Mock(weight=3)
        coord4 = Mock(weight=5)
        array1 = []
        array1.append(coord1)
        array1.append(coord2)
        array1.append(coord3)
        array1.append(coord4)
        minimum = pathfinding.find_minimum(array1)
        self.assertEqual(coord1, minimum)
