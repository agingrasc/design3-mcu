"""" Interface entre le système de prise de décision et le MCU. Se charge d'envoyer les commandes. """
import serial

from mcu.commands import Command

SERIAL_DEV_NAME = "ttyDesign3"


class RobotController(object):

    def __init__(self):
        self.ser = serial.Serial("/dev/{}".format(SERIAL_DEV_NAME))

    def send_command(self, cmd: Command):
        self.ser.write(cmd.pack_command())
