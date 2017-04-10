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
COMMANDS = [50, 0]

axis = {"yf": (protocol.Motors.FRONT_X, protocol.Motors.REAR_X, protocol.MotorsDirection.FORWARD),
          "yb": (protocol.Motors.FRONT_X, protocol.Motors.REAR_X, protocol.MotorsDirection.BACKWARD),
          "xf": (protocol.Motors.FRONT_Y, protocol.Motors.REAR_Y, protocol.MotorsDirection.FORWARD),
          "xb": (protocol.Motors.FRONT_Y, protocol.Motors.REAR_Y, protocol.MotorsDirection.BACKWARD)}

ser = serial.Serial("/dev/ttySTM32")

def accel_test(axis_id: tuple, consigne, rep_front, rep_rear):
    front_id, rear_id, axis_direction = axis_id
    front_dir = protocol.MotorsDirection.FORWARD
    rear_dir = protocol.MotorsDirection.BACKWARD

    if axis_direction == protocol.MotorsDirection.BACKWARD:
        front_dir = '-'
        rear_dir = '+'

    for cmd in COMMANDS:
        set_consigne(cmd, front_id, front_dir, rear_id, rear_dir)
        begin = time.time()
        id_time = time.time() - begin
        last_tick = time.time()
        while id_time < IDENTIFICATION_TIME:
            now = time.time()
            delta_t = now - last_tick
            if delta_t > STEP:
                last_tick = now
                consigne.append(cmd)
                ser.read(ser.inWaiting())
                front_speed = read_encoder(front_id)
                rep_front.append(front_speed)
                rear_speed = read_encoder(rear_id)
                rep_rear.append(rear_speed)
                print("(front:{}:{}) val: {}".format(front_id, delta_t, front_speed))
                print("(rear:{}:{}) val: {}".format(rear_id, delta_t, rear_speed))
            id_time = now - begin

    set_consigne(0, front_id, protocol.MotorsDirection.FORWARD, rear_id, protocol.MotorsDirection.FORWARD)
    print("{}\n{}\n{}".format(rep_front, rep_rear))


def set_consigne(cmd, front_id, front_direction, rear_id, rear_direction):
    ser.write(protocol.generate_manual_speed_command(front_id, cmd, front_direction))
    ser.write(protocol.generate_manual_speed_command(rear_id, cmd, rear_direction))


def main(axis_id: tuple):
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.ON))

    for motorx in protocol.Motors:
        ser.write(protocol.generate_manual_speed_command(motorx, 1, protocol.MotorsDirection.FORWARD))
    consigne = []
    rep_front = []
    rep_rear = []
    accel_test(axis_id, consigne, rep_front, rep_rear)
    #ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.ON))

    for motorx in protocol.Motors:
        ser.write(protocol.generate_manual_speed_command(motorx, 1, protocol.MotorsDirection.FORWARD))

    with open(fname+'.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(consigne)
        writer.writerow(rep_front)
        writer.writerow(rep_rear)

    print("Finish")


if __name__ == "__main__":
    if sys.argv[1] == '--help' or sys.argv[1] == '-h' or sys.argc == 1:
        print("yf, yb, xf, fb")
    fname = sys.argv[1]
    main(axis[sys.argv[1]])

