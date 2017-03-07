import serial
import time

import protocol
from util import *

ser = serial.Serial("/dev/ttySTM32")

# kp, ki, kd
constants = [(0.014279, 0.03122, 0),  # REAR X
             (0.016946, 0.033344, 0),  # FRONT Y
             (0.016877, 0.03873, 0),  # FRONT X
             (0.01679, 0.035129, 0)  # REAR Y
             ]


def set_pid_constants(kp=0.015, ki=0.030, kd=0):
    for motor in protocol.Motors:
        cmd = protocol.generate_set_pid_constant(motor, kp, ki, kd)
        ser.write(cmd)


def init():
    ser.read(ser.inWaiting())
    cmd_disable_pid = protocol.generate_set_pid_mode(protocol.PIDStatus.OFF)
    ser.write(cmd_disable_pid)
    set_pid_constants()


def normal_positive_test(motor):
    """" Test l'envoi d'une commande generique au pid pour une sortie raisonnable. """
    delta_t = 30  # ms
    current_speed = 3000  # tick/s
    target_speed = 220  # ms/s

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Normal positive test\n", 54)


def normal_negative_test(motor):
    """" Test l'envoi d'une commande generique au pid pour une sortie raisonnable. """
    delta_t = 30
    current_speed = 3000
    target_speed = -220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Normal negative test\n", -54)


def positive_upper_saturation_test(motor):
    """" Test une commande qui resulte en une saturation au-delà de la commande maximale (positive). """
    delta_t = 30
    current_speed = 0
    target_speed = 220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Positive saturation test\n", 85)


def negative_upper_saturation_test(motor):
    """" Test une commande qui resulte en une saturation en-deça de la commande maximale (negative). """
    delta_t = 30
    current_speed = 0
    target_speed = -220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Negative saturation test\n", -85)


"""
Les deux tests suivant s'assurent que le regulateur puisse generer une sortie nulle si la commande est tres basse.
"""
def positive_zero_test(motor):
    """" Test une commande insuffisante qui retourne une sortie 0 (commande positive). """
    delta_t = 30
    current_speed = 0
    target_speed = 1

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Positive zero test\n", 0)


def negative_zero_test(motor):
    """" Test une commande insuffisante qui retourne une sortie 0 (commande negative). """
    delta_t = 30
    current_speed = 0
    target_speed = -1

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Negative zero test\n", 0)


def print_result(msg_header, expected):
    ser.read(1)  # dump useless header confirmation
    actual = int.from_bytes(ser.read(1), byteorder='big', signed=True)
    print(msg_header + "expected: {} -- actual: {}\n".format(expected, actual))
    ser.read(1)


def deinit():
    cmd_reset_move = protocol.generate_move_command(0, 0, 0)
    ser.write(cmd_reset_move)
    cmd_enable_pid = protocol.generate_set_pid_mode(protocol.PIDStatus.ON)
    ser.write(cmd_enable_pid)


def main():
    init()
    motor = protocol.Motors.FRONT_X

    normal_positive_test(motor)
    normal_negative_test(motor)
    positive_upper_saturation_test(motor)
    negative_upper_saturation_test(motor)
    positive_zero_test(motor)
    negative_zero_test(motor)

    deinit()
    exit(0)


if __name__ == "__main__":
    main()
