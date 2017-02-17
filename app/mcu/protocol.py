"""" Ce module expose les fonctions d'un driver qui permet de generer un paquet valide pour le protocole de
communication."""
from enum import Enum

import struct


class PayloadLength(Enum):
    MOVE = 6
    LED = 2
    PENCIL = 2
    CAMERA = 4


class CommandType(Enum):
    MOVE = 0x0
    CAMERA = 0x1
    PENCIL = 0x2
    LED = 0x3


class Leds(Enum):
    UP_RED = 0
    UP_GREEN = 1
    DOWN_RED = 2
    DOWN_GREEN = 3


class PencilStatus(Enum):
    RAISED = 0
    LOWERED = 1


def generate_move_command(x, y, theta) -> bytes:
    header = _generate_header(CommandType.MOVE, PayloadLength.MOVE)
    payload = _generate_payload([x, y, theta])
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

