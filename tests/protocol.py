"""" Ce module expose les fonctions d'un driver qui permet de generer un paquet valide pour le protocole de
communication."""
from enum import Enum

import struct
from typing import List

import numpy as np

PID_SCALING = 100000
JACOBIAN_MATRIX = np.array([[0, 1, 120],
                            [-1, 0, 120],
                            [0, -1, 120],
                            [1, 0, 120]])


class PayloadLength(Enum):
    MOVE = 8
    LED = 2
    PENCIL = 2
    CAMERA = 4
    MANUAL_SPEED = 4
    READ_ENCODER = 2
    TOGGLE_PID = 2
    SET_PID_CONSTANTS = 10
    TEST_PID = 6
    READ_PID_LAST_CMD = 2
    READ_LAST_ADC = 2

class CommandType(Enum):
    MOVE = 0x00
    CAMERA = 0x01
    PENCIL = 0x02
    LED = 0x03
    SET_PID_CONSTANTS = 0x04
    MANUAL_SPEED = 0xa0
    READ_ENCODER = 0xa1
    TOGGLE_PID = 0xa2
    TEST_PID = 0xa3
    READ_PID_LAST_CMD = 0xa4
    READ_LAST_ADC = 0xa5

class Leds(Enum):
    UP_RED = 0
    UP_GREEN = 1
    DOWN_RED = 2
    DOWN_GREEN = 3
    BLINK_RED = 4
    BLINK_GREEN = 5

class Adc(Enum):
    ADC_MANCHESTER_CODE_POWER = 1
    ADC_MANCHESTER_CODE = 2
    ADC_PENCIL = 3

class PencilStatus(Enum):
    RAISED = 0
    LOWERED = 1


class Motors(Enum):
    REAR_X = 1 - 1
    FRONT_Y = 2 - 1
    FRONT_X = 3 - 1
    REAR_Y = 4 - 1


class PIDStatus(Enum):
    OFF = 0
    ON = 1


class MotorsDirection(Enum):
    FORWARD = 0
    BACKWARD = 1


class MotorsRotation(Enum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1


def generate_move_command(x, y, theta) -> bytes:
    speeds = compute_wheels_speed(x, y, theta)
    header = _generate_header(CommandType.MOVE, PayloadLength.MOVE)
    payload = _generate_payload(speeds)
    return header + payload


def generate_led_command(led: Leds) -> bytes:
    assert isinstance(led, Leds), "La led selectionne doit etre dans Leds."

    header = _generate_header(CommandType.LED, PayloadLength.LED)
    payload = _generate_payload([led.value])
    return header + payload


def generate_pencil_command(status: PencilStatus) -> bytes:
    assert isinstance(status, PencilStatus), "Le status doit etre dans PencilStatus."

    header = _generate_header(CommandType.PENCIL, PayloadLength.PENCIL)
    payload = _generate_payload([status.value])
    return header + payload


def generate_camera_command(x_theta: int, y_theta: int) -> bytes:
    header = _generate_header(CommandType.CAMERA, PayloadLength.CAMERA)
    payload = _generate_payload([x_theta, y_theta])
    return header + payload


def generate_manual_speed_command(motor: Motors, pwm_percentage: int, direction: MotorsDirection = None):
    """"
    Genere une commande directe en pourcentage de PWM pour un moteur
    Args:
        :motor: Identifiant du moteur
        :pwm_percentage [0, 100]: Pourcentage du PWM
        :direction: Direction du moteur
    Return:
        :cmd bytes: La commande serialise
    """
    if direction and direction == MotorsDirection.BACKWARD:
        # legacy code, avant la direction etait precise, on se contente de rendre negatif le pourcentage, le mcu
        # s'occupe de choisir la bonne direction
        pwm_percentage = -pwm_percentage

    header = _generate_header(CommandType.MANUAL_SPEED, PayloadLength.MANUAL_SPEED)
    payload = _generate_payload([motor.value, pwm_percentage])
    return header + payload

def generate_read_last_adc(adc: Adc):
    """
    Genere une commande qui effectue une lecture d'une valeur d'un des ADC.
    Args:
        :motor [0, 3]: Identifiant de l'ADC
    Return:
        :cmd bytes: La commande serialise
    """
    header = _generate_header(CommandType.READ_LAST_ADC, PayloadLength.READ_LAST_ADC)
    payload = _generate_payload([adc.value])
    return header + payload


def generate_read_encoder(motor: Motors):
    """
    Genere une commande qui effectue une lecture d'un encodeur.
    Args:
        :motor [0, 3]: Identifiant du moteur
    Return:
        :cmd bytes: La commande serialise
    """
    header = _generate_header(CommandType.READ_ENCODER, PayloadLength.READ_ENCODER)
    payload = _generate_payload([motor.value])
    return header + payload


def generate_set_pid_mode(mode: PIDStatus):
    header = _generate_header(CommandType.TOGGLE_PID, PayloadLength.TOGGLE_PID)
    payload = _generate_payload([mode.value])
    return header + payload


def generate_set_pid_constant(motor: Motors, ki: float, kp: float, kd: float, dz: int):
    """"
    Args:
        :ki: gain integral
        :kp: gain proportionnel
        :kd: gain differentiel
        :dz: deadzone
    """
    header = _generate_header(CommandType.SET_PID_CONSTANTS, PayloadLength.SET_PID_CONSTANTS)
    payload = _generate_payload([motor.value] + [int(ki*PID_SCALING), int(kp*PID_SCALING), int(kd*PID_SCALING)] + [dz])
    return header + payload


def generate_test_pid(motor: Motors, delta_t: int, current_speed: int):
    header = _generate_header(CommandType.TEST_PID, PayloadLength.TEST_PID)
    payload = _generate_payload([motor.value, delta_t, current_speed])
    return header + payload


def generate_read_pid_last_cmd(motor: Motors):
    header = _generate_header(CommandType.READ_PID_LAST_CMD, PayloadLength.READ_PID_LAST_CMD)
    payload = _generate_payload([motor.value])
    return header + payload


def _generate_payload(payload: list) -> bytes:
    """"
    Retourne la representation en bytes du payload
    Args:
        :payload: Une liste d'entiers
    Returns:
        La liste des arguments en representations binaires
    """
    assert isinstance(payload, list), "Le payload doit etre une liste"
    byte_payload = b''
    for arg in payload:
        assert arg < 32768, "L'argument dans un payload doit etre inferieur a 32768"
        assert arg >= -32768, "L'argument dans un payload doit etre superieur ou egal a -32768"
        byte_payload += struct.pack('>h', arg)
    return byte_payload


def _generate_header(cmd_type: CommandType, payload_len: PayloadLength) -> bytes:
    """"
    Genere un header avec le type de commande et la taille du payload
    Args:
        :cmd_type: le type de la commande
        :payload_len: le nombre d'octet qui suit dans le payload
    Returns:
        La representation binaire d'un header pour le type de commande et la taille de payload
    """
    assert isinstance(cmd_type, CommandType), "Le cmd_type doit être dans l'enum CommandType"
    assert isinstance(payload_len, PayloadLength), "Le payload_len doit etre dans PayloadLength"
    assert payload_len.value < 256, "Le payload_len doit etre inferieur a 256"
    assert payload_len.value >= 0, "Le payload_len doit etre signe"
    checksum = (256 - (cmd_type.value + payload_len.value)) % 256

    return bytes([cmd_type.value, payload_len.value, checksum])


def compute_wheels_speed(x: float, y: float, theta: float) -> List[int]:
    """
    Implemente le calcul du papier: 'Holonomic Omni-Directional Vehicle with New Omni-Wheel Mechanism'
    Permet de calculer la vitesse individuelle de chaque roue selon les vitesses x, y et theta en entree.
    L'algorithme corrige aussi le signe de la vitesse selon le sens de rotation de la roue.
    :param x: Vitesse en x (mm/s)
    :param y: Vitesse en y (mm/s)
    :param theta: Vitesse angulaire
    :return: La liste des vitesses des moteurs en mm/s (meme ordre que l'enum Motors)
    """
    return [int(x[0]) for x in JACOBIAN_MATRIX.dot(np.array([x, y, theta]).reshape((3, 1)))]
