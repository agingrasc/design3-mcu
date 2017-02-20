import csv
import time
import sys

import protocol
from encodeur import read_encoder
from util import *


IDENTIFICATION_TIME = 0.5
STEP = 0.030
COMMANDS = [20, 30, 40, 60, 70, 80]
COMPANION_COMMAND = 40


motors = {"frontx": (protocol.Motors.FRONT_X, protocol.Motors.REAR_X),
          "rearx": (protocol.Motors.REAR_X, protocol.Motors.FRONT_X),
          "fronty": (protocol.Motors.FRONT_Y, protocol.Motors.REAR_Y),
          "reary": (protocol.Motors.REAR_Y, protocol.Motors.FRONT_Y)}

ser = serial.Serial("/dev/ttySTM32")


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
                    speed = read_encoder(main_id)
                    if dir_sign == '+':
                        consigne.append(cmd)
                    else:
                        consigne.append(-cmd)
                    retroaction.append(speed)
                    print("({}) val: {}".format(delta_t, speed))
                id_time = now - begin
    print("{}\n{}".format(consigne, retroaction))


def set_consigne(cmd, companion_id, direction, main_id):
    ser.write(protocol.generate_manual_speed_command(main_id, cmd, direction))
    ser.read(2)
    ser.write(protocol.generate_manual_speed_command(companion_id, COMPANION_COMMAND, direction))
    ser.read(2)


def main(motors_id: tuple):
    ser.write(protocol.generate_toggle_pid())
    ser.read()
    consigne = []
    retroaction = []
    direction_test(motors_id, consigne, retroaction)
    ser.write(protocol.generate_toggle_pid())

    with open(fname+'.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(consigne)
        writer.writerow(retroaction)

    print("Finish")


if __name__ == "__main__":
    fname = sys.argv[1]
    main(motors[sys.argv[1]])

