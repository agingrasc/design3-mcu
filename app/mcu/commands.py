"""" Module contenant les commandes valident que l'IA peut envoyer au robot. """
from abc import abstractmethod, ABCMeta
from collections import namedtuple

import math

from app.mcu import protocol
from app.mcu.protocol import PencilStatus, Leds


PIDConstants = namedtuple("PIDConstatns", 'k_gain i_gain d_gain max_cmd min_cmd')
DEADZONE = 100
DEFAULT_DELTA_T = 0.030 # 30ms, a modifier


class PositionRegulator(object):
    """ Implémente un régulateur PI qui agit avec une rétroaction en position et génère une commande de vitesse."""

    def __init__(self):
        self.set_point = 0, 0, 0
        self.accumulator = 0, 0, 0
        self.constants = PIDConstants(1, 0, 0, 125, 0)

    @property
    def set_point(self):
        return self.set_point

    @set_point.setter
    def set_poit(self, set_point):
        if self.set_point != set_point:
            self.accumulator = 0, 0, 0
            self.set_point = set_point

    def next_speed_command(self, actual_position, delta_t=DEFAULT_DELTA_T):
        actual_x, actual_y, actual_theta = actual_position
        dest_x, dest_y, dest_theta = self.set_point
        err_x, err_y, err_theta = dest_x - actual_x, dest_y - actual_y, dest_theta - actual_theta

        # Proportionnel 1:1 (completement inutile)
        command = err_x, err_y, err_theta
        saturated_command = self._saturate_command(command)
        # TODO: ajuster le x et y en fonction de l'orientation

        if math.sqrt(err_x**2 + err_y**2) > DEADZONE:
            saturated_command = 0, 0, 0
        return saturated_command

    def _saturate_command(self, command):
        """"
        S'assure que chaque composante de la commande est dans l'interval [-max_cmd, -min_cmd] or [min_cmd, max_cmd]
        Args:
            :command tuple(x, y, t): composantes de la commande
        Returns:
            La commande saturée
        """
        saturated_command = command
        for idx,cmd_part in enumerate(command):
            if cmd_part < -self.constants.max_cmd:
                saturated_command[idx] = -self.constants.max_cmd
            elif cmd_part > self.constants.max_cmd:
                saturated_command[idx] = self.constants.max_cmd
            elif -self.constants.min_cmd < cmd_part < self.constants.min_cmd:
                # FIXME: il faudra probablement relineariser si la commande n'est pas au minimum
                saturated_command[idx] = 0
        return saturated_command


# regulator static et persistent
regulator = PositionRegulator()


class Command(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def pack_command(self) -> bytes:
        pass


class Move(Command):
    def __init__(self, x, y, theta):
        super().__init__()
        self.x = x
        self.y = y
        self.theta = theta

    def pack_command(self) -> bytes:
        regulator.set_point = self.x, self.y, self.theta
        position = 0, 0, 0 # TODO: obtenir la retroaction de la camera
        regulated_command = regulator.next_speed_command(position)
        return protocol.generate_move_command(*regulated_command)


class Camera(Command):
    def __init__(self, x_theta, y_theta):
        super().__init__()
        self.x_theta = x_theta
        self.y_theta = y_theta

    def pack_command(self) -> bytes:
        return protocol.generate_camera_command(self.x_theta, self.y_theta)


class Pencil(Command):
    def __init__(self, status: PencilStatus):
        super().__init__()
        self.status = status

    def pack_command(self) -> bytes:
        return protocol.generate_pencil_command(self.status)


class Led(Command):
    def __init__(self, led: Leds):
        super().__init__()
        self.led = led

    def pack_command(self) -> bytes:
        return protocol.generate_led_command(self.led)
