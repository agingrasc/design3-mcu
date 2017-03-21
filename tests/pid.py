import serial
import time

import protocol
from util import *

ser = serial.Serial("/dev/ttySTM32")

# kp, ki, kd
constants = [(0.027069, 0.040708, 0),  # REAR X
             (0.0095292, 0.029466, 0),  # FRONT Y
             (0.015431, 0.042286, 0),  # FRONT X
             (0.030357, 0.02766, 0)  # REAR Y
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
    current_speed = -3000
    target_speed = -220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Normal negative test\n", -54)


def accumulator_zeroed_on_new_target_test(motor):
    """"
    Test d'envoi de 2 consignes successive avec update du pid.
    S'assure que l'accumulateur d'un meme pid est remis a zero si la consigne change.
    """
    # on reinit a zero l'etat pour ne pas dependre de l'ordre de test
    target_speed = 0

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)

    # on effectue une update de pid avec un premier set de donnee
    delta_t = 30
    current_speed = 3000
    target_speed = 220
    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    # on effectue une seconde update de pid avec une consigne qui a change
    delta_t = 30
    current_speed = -3000
    target_speed = -220
    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Zeroed accumulator test\n", -54)


def delta_t_impact_test(motor):
    """" Test que le delta_t a un impact sur la sortie. """
    delta_t = 60
    current_speed = 3000
    target_speed = 220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("delta_t impact test\n", 63)


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

    print_result("Positive upper saturation test\n", 85)


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

    print_result("Negative upper saturation test\n", -85)


def positive_lower_saturation_test(motor):
    """" Test une commande qui resulte en une saturation en-deca de la commande minimale (positive). """
    delta_t = 30
    current_speed = 6000
    target_speed = 220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Positive lower saturation test\n", 35)


def negative_lower_saturation_test(motor):
    """" Test une commande qui resulte en une saturation au-dela de la commande minimale (negative). """
    delta_t = 30
    current_speed = -6000
    target_speed = -220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Negative lower saturation test\n", -35)


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


def accumulator_impact_test(motor):
    """" Test 2 update sucessive du pid et verifie que la seconde sortie correspond (en considerant l'impact du I). """
    delta_t = 30
    current_speed = 3000
    target_speed = 220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Accumulator impact test\n", 57)


def reverse_direction_positive_to_negative_test(motor):
    """" Test la sortie lorsque les roues ont une vitesse positive et qu'une vitesse negative est demandee. """
    delta_t = 30
    current_speed = 3000
    target_speed = -220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Reverse direction positive -> negative test\n", -85)


def reverse_direction_negative_to_positive_test(motor):
    """" Test la sortie lorsque les roues ont une vitesse negative et qu'une vitesse positive est demandee. """
    delta_t = 30
    current_speed = -3000
    target_speed = 220

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)

    print_result("Reverse direction negative -> positive test\n", 85)


def precise_test(motor):
    """"
    La sortie a ete calculee manuellement, on valide si le PID donne la reponse theorique attendu.
    Trois iterations sont calculees.
    La vitesse courante est augmentee a des valeurs arbitraires entre chaque calcul.
    """
    delta_t = 30
    current_speed = 1000
    target_speed = 220

    # reinit
    cmd_set_speed = protocol.generate_move_command(0, 0, 0)
    ser.write(cmd_set_speed)

    cmd_set_speed = protocol.generate_move_command(target_speed, 0, 0)
    ser.write(cmd_set_speed)
    ser.read(1)
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)
    print_result("Precise test (iter 1)\n", 85)

    current_speed = 2500
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)
    print_result("Precise test (iter 2)\n", 66)

    current_speed = 3000
    cmd = protocol.generate_test_pid(motor, delta_t, current_speed)
    ser.read(ser.inWaiting())
    ser.write(cmd)
    print_result("Precise test (iter 3)\n", 62)


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
    accumulator_zeroed_on_new_target_test(motor)
    positive_upper_saturation_test(motor)
    negative_upper_saturation_test(motor)
    positive_lower_saturation_test(motor)
    negative_lower_saturation_test(motor)
    positive_zero_test(motor)
    negative_zero_test(motor)
    accumulator_impact_test(motor)
    delta_t_impact_test(motor)
    reverse_direction_positive_to_negative_test(motor)
    reverse_direction_negative_to_positive_test(motor)
    precise_test(motor)

    deinit()
    exit(0)


if __name__ == "__main__":
    main()
