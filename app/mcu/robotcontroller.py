"""" Interface entre le système de prise de décision et le MCU. Se charge d'envoyer les commandes. """
import serial
import time

from mcu import protocol

if __name__ == "__main__":
    from mcu.protocol import Leds
    from mcu.commands import Command, Led
else:
    from mcu.protocol import Leds
    from .commands import Command, Led

SERIAL_DEV_NAME = "ttySTM32"

class SerialMock():

    def write(self, arg, byteorder='little'):
        print("Serial mock: {} -- ".format(arg, byteorder))
        return -1

    def read(self, nbr_byte):
        print("Serial mock reading! ({})".format(nbr_byte))
        return b'\x00'

class RobotController(object):

    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/{}".format(SERIAL_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link!")
            self.ser = SerialMock()

    def send_command(self, cmd: Command):
        self.ser.write(cmd.pack_command())
        ret_code = self._get_return_code()
        while ret_code != 0:
            self.ser.write(cmd.pack_command())

    def startup_test(self):
        print("startup test")
        cmd = Led(Leds.UP_GREEN)
        self.send_command(cmd)
        time.sleep(1)
        cmd = Led(Leds.DOWN_GREEN)
        self.send_command(cmd)
        self.ser.write(protocol.generate_toggle_pid())

    def _get_return_code(self):
        return int.from_bytes(self.ser.read(1), byteorder='little')

robot_controller = RobotController()

if __name__ == "__main__":
    robot_controller.startup_test()