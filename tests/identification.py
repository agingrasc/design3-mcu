import time
import sys

import protocol
from encodeur import read_encoder
from util import *


IDENTIFICATION_TIME = 0.5
STEP = 0.030
COMMANDS = [20, 30, 40, 60, 70, 80]


motors = {"frontx": protocol.Motors.FRONT_X,
          "rearx": protocol.Motors.REAR_X,
          "fronty": protocol.Motors.FRONT_Y,
          "reary": protocol.Motors.REAR_Y}

ser = serial.Serial("/dev/ttySTM32")


def direction_test(motor_id: protocol.Motors, consigne, retroaction):
    for direction in protocol.MotorsDirection:
        for cmd in COMMANDS:
            ser.write(protocol.generate_manual_speed_command(motor_id, cmd, direction))
            begin = time.time()
            id_time = time.time() - begin
            last_tick = time.time()
            while id_time < IDENTIFICATION_TIME:
                now = time.time()
                delta_t = now - last_tick
                if delta_t > STEP:
                    last_tick = now
                    speed = read_encoder(motor_id)
                    consigne.append(cmd)
                    retroaction.append(speed)
                    print("({}) val: {}".format(delta_t, speed))
                id_time = now - begin
    print("{}\n{}".format(consigne, retroaction))


def main(motor_id: protocol.Motors):
    ser.write(protocol.generate_toggle_pid())
    ser.read()
    consigne = []
    retroaction = []
    direction_test(motor_id, consigne, retroaction)

    ser.write(protocol.generate_toggle_pid())
    print("finish")


if __name__ == "__main__":
    main(motors[sys.argv[1]])

