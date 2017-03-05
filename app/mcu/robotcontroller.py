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


class SerialMock:
    """" SerialMock permet de remplacer le lien serie si ce dernier n'est pas disponible."""
    def write(self, arg, byteorder='little'):
        print("Serial mock: {} -- ".format(arg, byteorder))
        return -1

    def read(self, nbr_byte):
        print("Serial mock reading! ({})".format(nbr_byte))
        return b'\x00'


class RobotController(object):
    """" Controleur du robot, permet d'envoyer les commandes et de recevoir certaines informations du MCU."""
    def __init__(self):
        """" Si aucun lien serie n'est disponible, un SerialMock est instancie."""
        try:
            self.ser = serial.Serial("/dev/{}".format(SERIAL_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link!")
            self.ser = SerialMock()

    def send_command(self, cmd: Command):
        """"
        Prend une commande et s'occupe de l'envoyer au MCU.
        Args:
            :cmd: La commande a envoyer
        Returns:
            None
        """
        self.ser.write(cmd.pack_command())
        ret_code = self._get_return_code()
        while ret_code != 0:
            self.ser.write(cmd.pack_command())

    def _startup_test(self):
        """ Effectue un test de base pour s'assurer que le MCU repond et met le MCU en mode de debogage."""
        print("startup test")
        cmd = Led(Leds.UP_GREEN)
        self.send_command(cmd)
        time.sleep(1)
        cmd = Led(Leds.DOWN_GREEN)
        self.send_command(cmd)
        self.ser.write(protocol.generate_toggle_pid())

    def _get_return_code(self):
        return int.from_bytes(self.ser.read(1), byteorder='little')

""" Instance persistante du Controler."""
robot_controller = RobotController()

if __name__ == "__main__":
    robot_controller._startup_test()