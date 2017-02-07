import unittest
from src.python.app.mcu import protocol
from src.python.app.mcu.protocol import Leds, PencilStatus


class ProtocolTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_zero_move(self):
        expected_cmd = b'\x00\x03\x00\x00\x00'
        packed_cmd = protocol.generate_move_command(0, 0, 0)
        self.assertEqual(expected_cmd, packed_cmd)

    def test_basic_move(self):
        expected_cmd = b'\x00\x03\x0a\x0a\x0a'
        packed_cmd = protocol.generate_move_command(10, 10, 10)
        self.assertEqual(expected_cmd, packed_cmd)

    def test_bad_arg_move(self):
        self.assertRaises(AssertionError, protocol.generate_move_command, 256, 0, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, -1, 0, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, 256, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, -1, 0)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, 0, 256)
        self.assertRaises(AssertionError, protocol.generate_move_command, 0, 0, -1)

    def test_multiple_bad_args_move(self):
        self.assertRaises(AssertionError, protocol.generate_move_command, 256, 256, 0)

    def test_basic_camera(self):
        expected = b'\x01\x02\x0f\x0f'
        actual = protocol.generate_camera_command(15, 15)
        self.assertEqual(expected, actual)

    def test_basic_pencil(self):
        expected = b'\x02\x01\x00'
        actual = protocol.generate_pencil_command(PencilStatus.RAISED)
        self.assertEqual(expected, actual)

    def test_invalid_pencil_status(self):
        self.assertRaises(AssertionError, protocol.generate_pencil_command, 0)

    def test_basic_led(self):
        expected_red = b'\x03\x01\x00'
        actual_red = protocol.generate_led_command(Leds.RED)
        self.assertEqual(expected_red, actual_red)

        expected_green = b'\x03\x01\x01'
        actual_green = protocol.generate_led_command(Leds.GREEN)
        self.assertEqual(expected_green, actual_green)

    def test_invalid_led(self):
        self.assertRaises(AssertionError, protocol.generate_led_command, 0)
