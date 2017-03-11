import csv
import time
import sys

import protocol
from encodeur import read_encoder
from util import *

# Deadzone id
#  - without charge
#    - forward
#      frontx: 8%
#      rearx: 8%
#      fronty: 8%
#      reary: 9%    *
#    - backward
#      frontx: -8%
#      rearx: -8%
#      fronty: -8%
#      reary: -9%   *
#  - with charge
#    - forward
#      frontx: 31%
#      rearx: 27%
#      fronty: 26%
#      reary: 26%
#    - backward
#      frontx: 30%
#      rearx: 29%
#      fronty: 27%
#      reary: 25%

IDENTIFICATION_TIME = 1.5
STEP = 0.030
COMMANDS = [30, 80]
COMPANION_COMMAND = 60

ROTATION_TEST = False # Rotation id tests

motors = {"frontx": (protocol.Motors.FRONT_X, protocol.Motors.REAR_X),
          "rearx": (protocol.Motors.REAR_X, protocol.Motors.FRONT_X),
          "fronty": (protocol.Motors.FRONT_Y, protocol.Motors.REAR_Y),
          "reary": (protocol.Motors.REAR_Y, protocol.Motors.FRONT_Y)}

ser = serial.Serial("/dev/ttySTM32")

def rotation_test(motors_id: tuple, consigne, retroaction):
    main_id, companion_id = motors_id
    companion_sign = '+'
    main_sign = '-';
    for direction in protocol.MotorsRotation:
        if direction == protocol.MotorsDirection.CLOCKWISE:
            companion_sign = '+'
            main_sign = '-'
        else:
            companion_sign = '-'
            main_sign = '+'

        for cmd in COMMANDS:
            set_consigne(cmd, companion_id, companion_sign, main_id)
            begin = time.time()
            id_time = time.time() - begin
            last_tick = time.time()
            while id_time < IDENTIFICATION_TIME:
                now = time.time()
                delta_t = now - last_tick
                if delta_t > STEP:
                    last_tick = now
                    ser.read(ser.inWaiting())
                    speed = read_encoder(main_id)
                    if main_sign == '+':
                        consigne.append(cmd)
                    else:
                        consigne.append(-cmd)
                    retroaction.append(speed)
                    print("({}) val: {}".format(delta_t, speed))
                id_time = now - begin

    set_consigne(0, companion_id, protocol.MotorsDirection.FORWARD, main_id)
    print("{}\n{}".format(consigne, retroaction))

def direction_test(motors_id: tuple, consigne, retroaction):
    main_id, companion_id = motors_id
    dir_sign = '+'
    for direction in protocol.MotorsDirection:
        if direction == protocol.MotorsDirection.FORWARD:
            dir_sign = '+'
        else:
            dir_sign = '-'
        for cmd in COMMANDS:
            set_consigne(cmd, companion_id, direction, main_id)
            begin = time.time()
            id_time = time.time() - begin
            last_tick = time.time()
            while id_time < IDENTIFICATION_TIME:
                now = time.time()
                delta_t = now - last_tick
                if delta_t > STEP:
                    last_tick = now
                    ser.read(ser.inWaiting())
                    speed = read_encoder(main_id)
                    if dir_sign == '+':
                        consigne.append(cmd)
                    else:
                        consigne.append(-cmd)
                    retroaction.append(speed)
                    print("({}) val: {}".format(delta_t, speed))
                id_time = now - begin

    set_consigne(0, companion_id, protocol.MotorsDirection.FORWARD, main_id)
    print("{}\n{}".format(consigne, retroaction))


def set_consigne(cmd, companion_id, direction, main_id):
    ser.write(protocol.generate_manual_speed_command(main_id, cmd, direction))
    ser.read(2)
    ser.write(protocol.generate_manual_speed_command(companion_id, COMPANION_COMMAND, direction))
    ser.read(2)


def main(motors_id: tuple):
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.OFF))
    ser.read()
    for motorx in protocol.Motors:
        ser.write(protocol.generate_manual_speed_command(motorx, 1, protocol.MotorsDirection.FORWARD))
    consigne = []
    retroaction = []
    if ROTATION_TEST == True:
        rotation_test(motors_id, consigne, retroaction)
    else:
        direction_test(motors_id, consigne, retroaction)
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.ON))

    for motorx in protocol.Motors:
        ser.write(protocol.generate_manual_speed_command(motorx, 1, protocol.MotorsDirection.FORWARD))

    with open(fname+'.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(consigne)
        writer.writerow(retroaction)

    print("Finish")


if __name__ == "__main__":
    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print("frontx, fronty, rearx, reary")
    fname = sys.argv[1]
    main(motors[sys.argv[1]])

