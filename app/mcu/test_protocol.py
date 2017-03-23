import unittest
from . import protocol
from .protocol import Leds, PencilStatus


class ProtocolTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_zero_move(self):
        expected_cmd = b'\x00\x06\xfa\x00\x00\x00\x00\x00\x00'
        packed_cmd = protocol.generate_move_command(0, 0, 0)
        self.assertEqual(expected_cmd, packed_cmd)

    def test_basic_move(self):
        expected_cmd = b'\x00\x06\xfa\x00\x0a\x00\x0a\x00\x0a'
        packed_cmd = protocol.generate_move_command(10, 10, 10)
        self.assertEqual(expected_cmd, packed_cmd)

    def test_one_arg_over_255(self):
        self.assertRaises(AssertionError, protocol.generate_move_command, 32768, 0, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, 32768, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, 0, 32768)

    def test_one_arg_under_0(self):
        self.assertRaises(AssertionError, protocol.generate_move_command, -32769, 0, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, -32769, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, 0, -32769)

    def test_multiple_bad_args_move(self):
        self.assertRaises(AssertionError, protocol.generate_move_command, 32768, 32768, 0)

    def test_basic_camera(self):
        expected = b'\x01\x04\xfb\x00\x0f\x00\x0f'
        actual = protocol.generate_camera_command(15, 15)
        self.assertEqual(expected, actual)

    def test_basic_pencil(self):
        expected_pencil_cmd = b'\x02\x02\xfc\x00\x00'
        actual_pencil_cmd = protocol.generate_pencil_command(PencilStatus.RAISED)
        self.assertEqual(expected_pencil_cmd, actual_pencil_cmd)

    def test_invalid_pencil_status(self):
        self.assertRaises(AssertionError, protocol.generate_pencil_command, 0)

    def test_red_led(self):
        expected_red = b'\x03\x02\xfb\x00\x00'
        actual_red = protocol.generate_led_command(Leds.UP_RED)
        self.assertEqual(expected_red, actual_red)

    def test_green_led(self):
        expected_green = b'\x03\x02\xfb\x00\x01'
        actual_green = protocol.generate_led_command(Leds.UP_GREEN)
        self.assertEqual(expected_green, actual_green)

    def test_invalid_led(self):
        self.assertRaises(AssertionError, protocol.generate_led_command, 0)
