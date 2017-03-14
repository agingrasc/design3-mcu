import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
from app.domain.pathfinding import get_segments


class GetSegmentsTest(unittest.TestCase):
    def test_no_corner_path(self):
        path = []
        path.append(Mock(pos_x=4, pos_y=4))
        path.append(Mock(pos_x=4, pos_y=5))
        path.append(Mock(pos_x=4, pos_y=6))
        path.append(Mock(pos_x=4, pos_y=7))
        path.append(Mock(pos_x=4, pos_y=8))

        filter_path = get_segments.get_filter_path(path)
        self.assertEqual(len(filter_path), 2)

        self.assertEqual(filter_path[0].pos_y, 4)
        self.assertEqual(filter_path[0].pos_x, 4)

        self.assertEqual(filter_path[1].pos_y, 8)
        self.assertEqual(filter_path[1].pos_x, 4)

    def test_diagonal_corner_path(self):
        path = []
        path.append(Mock(pos_x=4, pos_y=4))
        path.append(Mock(pos_x=4, pos_y=5))
        path.append(Mock(pos_x=5, pos_y=6))
        path.append(Mock(pos_x=6, pos_y=7))
        path.append(Mock(pos_x=7, pos_y=8))

        filter_path = get_segments.get_filter_path(path)
        self.assertEqual(len(filter_path), 3)

        self.assertEqual(filter_path[0].pos_y, 4)
        self.assertEqual(filter_path[0].pos_x, 4)

        self.assertEqual(filter_path[1].pos_y, 6)
        self.assertEqual(filter_path[1].pos_x, 5)

        self.assertEqual(filter_path[2].pos_y, 8)
        self.assertEqual(filter_path[2].pos_x, 7)
