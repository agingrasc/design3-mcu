"""" Sanity test des encodeurs """
import serial

import protocol as protocol
from util import *

ser = serial.Serial("/dev/ttySTM32")

def main():
    ser.write(protocol.generate_read_encoder(protocol.Motors.FRONT_X))
    print_code(HEADER_W, ser)
    read_encoder("motor front X")
    print_code(PAYLOAD_W, ser)
    print('\n')

    ser.write(protocol.generate_read_encoder(protocol.Motors.REAR_X))
    print_code(HEADER_W, ser)
    read_encoder("motor rear X")
    print_code(PAYLOAD_W, ser)
    print('\n')

    ser.write(protocol.generate_read_encoder(protocol.Motors.FRONT_Y))
    print_code(HEADER_W, ser)
    read_encoder("motor front Y")
    print_code(PAYLOAD_W, ser)
    print('\n')

    ser.write(protocol.generate_read_encoder(protocol.Motors.REAR_Y))
    print_code(HEADER_W, ser)
    read_encoder("motor rear Y")
    print_code(PAYLOAD_W, ser)
    print('\n')


def read_encoder(msg: str) -> int:
    speed = ser.read(2)
    print("Expected: 0")
    print("Speed of {}: {}".format(msg, int.from_bytes(speed, byteorder='big')))

if __name__ == "__main__":
    main()