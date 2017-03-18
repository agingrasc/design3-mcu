"""" Module contenant les commandes valident que l'IA peut envoyer au robot. """
from abc import abstractmethod, ABCMeta
from collections import namedtuple

import math
from typing import List, Tuple

from domain.gameboard.position import Position
from . import protocol
from .protocol import PencilStatus, Leds


PIDConstants = namedtuple("PIDConstants", 'kp ki kd max_cmd deadzone_cmd min_cmd')
DEADZONE = 50
DEFAULT_DELTA_T = 0.100  # en secondes
MAX_X = 200
MAX_Y = 100

DEFAULT_KP = 1
DEFAULT_KI = 0
DEFAULT_KD = 0
DEFAULT_MAX_CMD = 80
DEFAULT_DEADZONE_CMD = 20
DEFAULT_MIN_CMD = 20


class PIPositionRegulator(object):
    """ Implémente un régulateur PI qui agit avec une rétroaction en position et génère une commande de vitesse."""

    def __init__(self, kp=DEFAULT_KP, ki=DEFAULT_KI, kd=DEFAULT_KD, max_cmd=DEFAULT_MAX_CMD,
                 deadzone_cmd=DEFAULT_DEADZONE_CMD, min_cmd=DEFAULT_MIN_CMD):
        self._setpoint: Position = Position()
        self.accumulator = 0, 0, 0
        self.constants = PIDConstants(kp, ki, kd, max_cmd, deadzone_cmd, min_cmd)

    @property
    def setpoint(self):
        return self._setpoint

    @setpoint.setter
    def setpoint(self, new_setpoint):
        """" Assigne une consigne au regulateur. Effet de bord: reinitialise les accumulateurs. """
        if self._setpoint != new_setpoint:
            self.accumulator = 0, 0, 0
            self._setpoint = new_setpoint

    def next_speed_command(self, actual_position: Position, delta_t: float=DEFAULT_DELTA_T) -> List[int]:
        """"
        Calcul une iteration du PID.
        Args:
            :actual_position: Retroaction de la position du robot.
            :delta_t: Temps ecoule depuis le dernier appel ou la derniere assignation de consigne en secondes.
        Returns:
            La vitesse en x, y et en theta.
        """
        actual_x = actual_position.pos_x
        actual_y = actual_position.pos_y
        actual_theta = actual_position.theta
        dest_x = self.setpoint.pos_x
        dest_y = self.setpoint.pos_y
        dest_theta = self.setpoint.theta
        err_x, err_y, err_theta = dest_x - actual_x, dest_y - actual_y, dest_theta - actual_theta

        cmd_x = err_x * self.constants.kp
        cmd_y = err_y * self.constants.kp
        cmd_x = self._relinearize(cmd_x)
        cmd_y = self._relinearize(cmd_y)
        cmd_x, cmd_y = _correct_for_referential_frame(cmd_x, cmd_y, actual_theta)
        saturated_cmd = []
        for cmd in [cmd_x, cmd_y, err_theta]:
            saturated_cmd.append(self._saturate_cmd(cmd))

        if self.is_arrived(actual_position, DEADZONE):
            saturated_cmd = 0, 0, 0

        command = []
        for cmd in saturated_cmd:
            command.append(int(cmd))
        return command

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

    def is_arrived(self, robot_position: Position, deadzone = DEADZONE):
        err_x = robot_position.pos_x - self.setpoint.pos_x
        err_y = robot_position.pos_y - self.setpoint.pos_y
        return math.sqrt(err_x**2 + err_y**2) < deadzone


def _correct_for_referential_frame(x: float, y: float, t: float) -> Tuple[float]:
    """"
    Rotation du vecteur (x, y) dans le plan monde pour l'orienter avec l'angle t du robot.
    Args:
        :x: Composante x du vecteur, dans le plan monde
        :y: Composante y du vecteur, dans le plan monde
        :t: Orientation du robot en radians dans le plan monde
    Returns:
        Un tuple contenant les composantes x et y selon le plan du robot.
    """
    cos = math.cos(t)
    sin = math.sin(t)

    corrected_x = (x * cos - y * sin)
    corrected_y = (y * cos + x * sin)
    return corrected_x, corrected_y


""" Regulateur de position persistent."""
regulator = PIPositionRegulator()


class ICommand(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def pack_command(self) -> bytes:
        """" Indique comment prendre les informations de l'objet et des serialiser pour l'envoyer au robot."""
        pass


class MoveCommand(ICommand):
    def __init__(self, robot_position):
        """"
        Args:
            :x: Position x sur le plan monde
            :y: Position y sur le plan monde
            :theta: Orientation du robot en radians
        """
        super().__init__()
        self.robot_position = robot_position

    def pack_command(self) -> bytes:
        regulated_command = regulator.next_speed_command(self.robot_position)
        return protocol.generate_move_command(*regulated_command)


class CameraOrientationCommand(ICommand):
    def __init__(self, x_theta, y_theta):
        """"
        Args:
            :x_theta: Orientation horizontale en radians.
            :y_theta: Orientation verticale en radians.
        """
        super().__init__()
        self.x_theta = x_theta
        self.y_theta = y_theta

    def pack_command(self) -> bytes:
        return protocol.generate_camera_command(self.x_theta, self.y_theta)


class PencilRaiseLowerCommand(ICommand):
    """" Une commande Pencil permet de controler le status du prehenseur."""
    def __init__(self, status: PencilStatus):
        super().__init__()
        self.status = status

    def pack_command(self) -> bytes:
        return protocol.generate_pencil_command(self.status)


class LedCommand(ICommand):
    def __init__(self, led: Leds):
        super().__init__()
        self.led = led

    def pack_command(self) -> bytes:
        return protocol.generate_led_command(self.led)
