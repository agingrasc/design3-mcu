"""" Sanity test des encodeurs """
import serial

import protocol as protocol
from util import *

ser = serial.Serial("/dev/ttySTM32")

def main():
    print_encoder("motor front X", protocol.Motors.FRONT_X)
    print_code(PAYLOAD_W, ser)
    print('\n')

    print_encoder("motor rear X", protocol.Motors.REAR_X)
    print_code(PAYLOAD_W, ser)
    print('\n')

    print_encoder("motor front Y", protocol.Motors.FRONT_Y)
    print_code(PAYLOAD_W, ser)
    print('\n')

    print_encoder("motor rear Y", protocol.Motors.REAR_Y)
    print_code(PAYLOAD_W, ser)
    print('\n')


def print_encoder(msg: str, motor_id: protocol.Motors):
    speed = read_encoder(motor_id)
    print("Expected: 0")
    print("Speed of {} ({}): {}".format(msg, motor_id.value + 1, speed))


def read_encoder(motor_id: protocol.Motors, ser=ser) -> int:
    ser.write(protocol.generate_read_encoder(motor_id))
    ser.read(1)
    speed = ser.read(2)
    return int.from_bytes(speed, byteorder='big')

if __name__ == "__main__":
    main()