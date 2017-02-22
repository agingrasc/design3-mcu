import time
import sys

from util import *
import protocol

ser = serial.Serial("/dev/ttySTM32")

TEST_VAL = 40

def main():
    ser.write(protocol.generate_toggle_pid())
    ser.write(protocol.generate_led_command(protocol.Leds.UP_GREEN))
    for idx in protocol.Motors:
        print("idx: {}".format(idx))
        ser.write(protocol.generate_manual_speed_command(idx, TEST_VAL, protocol.MotorsDirection.FORWARD))

    input()

    ser.write(protocol.generate_toggle_pid())
    ser.write(protocol.generate_led_command(protocol.Leds.DOWN_GREEN))
    for idx in protocol.Motors:
        print("idx: {}".format(idx))
        ser.write(protocol.generate_manual_speed_command(idx, 0, protocol.MotorsDirection.FORWARD))


if __name__ == "__main__":
    main()
