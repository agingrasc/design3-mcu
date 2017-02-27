"""" Module contenant les commandes valident que l'IA peut envoyer au robot. """
from abc import abstractmethod, ABCMeta
from collections import namedtuple

import math

from . import protocol
from .protocol import PencilStatus, Leds


PIDConstants = namedtuple("PIDConstatns", 'kp ki kd max_cmd deadzone_cmd min_cmd')
DEADZONE = 15
DEFAULT_DELTA_T = 0.067  # 30ms, a modifier
MAX_X = 200
MAX_Y = 100

DEFAULT_KP = 100
DEFAULT_KI = 0
DEFAULT_KD = 0
DEFAULT_MAX_CMD = 80
DEFAULT_DEADZONE_CMD = 40
DEFAULT_MIN_CMD = 10


class PositionRegulator(object):
    """ Implémente un régulateur PI qui agit avec une rétroaction en position et génère une commande de vitesse."""

    def __init__(self, kp=DEFAULT_KP, ki=DEFAULT_KI, kd=DEFAULT_KD, max_cmd=DEFAULT_MAX_CMD,
                 deadzone_cmd=DEFAULT_DEADZONE_CMD, min_cmd=DEFAULT_MIN_CMD):
        self._set_point = 0, 0, 0
        self.accumulator = 0, 0, 0
        self.constants = PIDConstants(kp, ki, kd, max_cmd, deadzone_cmd, min_cmd)

    @property
    def set_point(self):
        return self._set_point

    @set_point.setter
    def set_point(self, set_point):
        if self._set_point != set_point:
            self.accumulator = 0, 0, 0
            self._set_point = set_point

    def next_speed_command(self, actual_position, delta_t=DEFAULT_DELTA_T):
        actual_x, actual_y, actual_theta = actual_position
        dest_x, dest_y, dest_theta = self.set_point
        err_x, err_y, err_theta = dest_x - actual_x, dest_y - actual_y, dest_theta - actual_theta

        cmd_x = err_x / MAX_X * self.constants.kp
        cmd_y = err_y / MAX_Y * self.constants.kp
        cmd_x = self._relinearize(cmd_x)
        cmd_y = self._relinearize(cmd_y)
        cmd_x, cmd_y = _correct_for_referential_frame(cmd_x, cmd_y, actual_theta)
        saturated_cmd = []
        for cmd in [cmd_x, cmd_y, err_theta]:
            saturated_cmd.append(self._saturate_cmd(cmd))

        if math.sqrt(err_x**2 + err_y**2) < DEADZONE:
            saturated_cmd = 0, 0, 0
        return saturated_cmd

    def _relinearize(self, cmd):
        """" Force la valeur de cmd dans [deadzone_cmd, max_cmd] ou 0 si dans [-min_cmd, min_cmd]"""
        if self.constants.min_cmd < cmd < self.constants.deadzone_cmd:
            return self.constants.deadzone_cmd
        elif -self.constants.deadzone_cmd < cmd < -self.constants.min_cmd:
            return -self.constants.deadzone_cmd
        elif -self.constants.min_cmd <= cmd <= self.constants.min_cmd:
            return 0
        else:
            return cmd

    def _saturate_cmd(self, cmd):
        if cmd > self.constants.max_cmd:
            return self.constants.max_cmd
        elif cmd < -self.constants.max_cmd:
            return -self.constants.max_cmd
        else:
            return cmd


def _correct_for_referential_frame(x, y, t):

    cos = math.cos(t)
    sin = math.sin(t)

    corrected_x = (x * cos - y * sin)
    corrected_y = (y * cos + x * sin)
    return corrected_x, corrected_y


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
        position = 0, 0, 0  # TODO: obtenir la retroaction de la camera
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
