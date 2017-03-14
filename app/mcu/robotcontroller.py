"""" Interface entre le système de prise de décision et le MCU. Se charge d'envoyer les commandes. """
import serial
import time

from domain.gameboard.position import Position
from mcu import protocol

if __name__ == "__main__":
    from mcu.protocol import Leds
    from mcu.commands import ICommand, LedCommand, MoveCommand, regulator
else:
    from mcu.protocol import Leds
    from .commands import ICommand, LedCommand

SERIAL_MCU_DEV_NAME = "ttySTM32"
SERIAL_POLULU_DEV_NAME = "ttyPolulu"


constants = [(0.027069, 0.040708, 0, 14),  # REAR X
             (0.0095292, 0.029466, 0, 13),  # FRONT Y
             (0.015431, 0.042286, 0, 15),  # FRONT X
             (0.030357, 0.02766, 0, 13)]  # REAR Y


class SerialMock:
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
            self.ser_mcu = serial.Serial("/dev/{}".format(SERIAL_MCU_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link for mcu!")
            self.ser_mcu = SerialMock()

        try:
            self.ser_polulu = serial.Serial("/dev/{}".format(SERIAL_POLULU_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link for polulu!")
            self.ser_polulu = SerialMock()

        self._init_mcu_pid()
        self._startup_test()

    def send_command(self, cmd: ICommand):
        """"
        Prend une commande et s'occupe de l'envoyer au MCU.
        Args:
            :cmd: La commande a envoyer
        Returns:
            None
        """
        self.ser_mcu.write(cmd.pack_command())
        ret_code = self._get_return_code()
        while ret_code != 0:
            self.ser_mcu.write(cmd.pack_command())

    def send_move_command(self, robot_position: Position):
        cmd = MoveCommand(robot_position)
        self.send_command(cmd)

    def lower_pencil(self):
        pass

    def raise_pencil(self):
        pass

    def _init_mcu_pid(self):
        for motor in protocol.Motors:
            kp, ki, kd, dz = constants[motor.value]
            cmd = protocol.generate_set_pid_constant(motor, kp, ki, kd, dz)
            self.ser_mcu.write(cmd)

    def _startup_test(self):
        """ Effectue un test de base pour s'assurer que le MCU repond et met le MCU en mode de debogage."""
        print("startup test")
        cmd = LedCommand(Leds.UP_GREEN)
        self.send_command(cmd)
        time.sleep(1)
        cmd = LedCommand(Leds.DOWN_GREEN)
        self.send_command(cmd)
        self.ser_mcu.write(protocol.generate_toggle_pid())

    def _get_return_code(self):
        return int.from_bytes(self.ser_mcu.read(1), byteorder='little')

""" Instance persistante du Controler."""
robot_controller = RobotController()


def set_move_destination(move_destination: Position):
    regulator.setpoint = move_destination


if __name__ == "__main__":
    robot_controller._startup_test()