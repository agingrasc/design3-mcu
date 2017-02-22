import time
import sys

from util import *
import protocol

ser = serial.Serial("/dev/ttySTM32")

DEFAULT_SPEED = 40


def init():
    ser.write(protocol.generate_toggle_pid())
    ser.write(protocol.generate_led_command(protocol.Leds.UP_GREEN))


def deinit():
    ser.write(protocol.generate_toggle_pid())
    ser.write(protocol.generate_led_command(protocol.Leds.DOWN_GREEN))


def keyboard():
    print("Not implemented!")
    pass


def motor():
    motors_id = {1: protocol.Motors.REAR_X,
                 2: protocol.Motors.FRONT_Y,
                 3: protocol.Motors.FRONT_X,
                 4: protocol.Motors.REAR_Y}
    motor_id = 0

    try:
        motor_id = motors_id[int(sys.argv[2])]
    except IndexError:
        print("You need to input the motor id [1, 4].")
        exit()

    speed = DEFAULT_SPEED
    try:
        speed = int(sys.argv[3])
    except IndexError:
        pass

    print("Setting motor {} speed to {}".format(motor_id.value + 1, speed))
    ser.write(protocol.generate_manual_speed_command(motor_id, speed, protocol.MotorsDirection.FORWARD))
    input("Press 'Enter' to exit.")
    print("Stopping motor {}.".format(motor_id.value + 1))
    ser.write(protocol.generate_manual_speed_command(motor_id, 0, protocol.MotorsDirection.FORWARD))


def all_motors():
    speed = DEFAULT_SPEED
    try:
        speed = int(sys.argv[2])
    except IndexError:
        pass

    for idx in protocol.Motors:
        print("Setting motor {} speed to {}.".format(idx.value + 1, speed))
        ser.write(protocol.generate_manual_speed_command(idx, speed, protocol.MotorsDirection.FORWARD))

    input("Press 'Enter' to exit.")

    for idx in protocol.Motors:
        print("Stopping motor {}.".format(idx.value + 1))
        ser.write(protocol.generate_manual_speed_command(idx, 0, protocol.MotorsDirection.FORWARD))


dispatch = {'keyboard': keyboard,
            'motor': motor,
            'all-motors': all_motors}


def print_help():
    help_msg = """cmd extra-parameters
    motor idx [speed]
    all-motors [speed]
    keyboard [max-speed]"""
    print(help_msg)


def main():
    init()
    dispatch[sys.argv[1]]()
    deinit()


if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
        if cmd == "-h" or cmd == "--help":
            print_help()
            exit()
    except IndexError:
        print_help()
        exit()
    main()
