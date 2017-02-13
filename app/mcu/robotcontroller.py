"""" Interface entre le système de prise de décision et le MCU. Se charge d'envoyer les commandes. """
import serial

from .commands import Command

SERIAL_DEV_NAME = "ttySTM32"


class RobotController(object):

    def __init__(self):
        self.ser = serial.Serial("/dev/{}".format(SERIAL_DEV_NAME))

    def send_command(self, cmd: Command):
        self.ser.write(cmd.pack_command())
        ret_code = self.ser.read(1)
        while ret_code != 0:
            self.ser.write(cmd.pack_command())
