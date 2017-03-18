import serial
import time

import protocol
from util import *

HEADER_W = "Ecriture header: {}"
PAYLOAD_W = "Ecriture payload: {}"

ser = serial.Serial("/dev/ttySTM32")


def main():
    # test allumer led verte
    ser.write(protocol.generate_led_command(protocol.Leds.UP_GREEN))
    print_code(HEADER_W, ser)
    print_code(PAYLOAD_W, ser)

    # wait
    time.sleep(0.5)

    # test éteindre led verte
    ser.write(protocol.generate_led_command(protocol.Leds.DOWN_GREEN))
    print_code(HEADER_W, ser)
    print_code(PAYLOAD_W, ser)

    # wait
    time.sleep(0.5)

    # test led verte 1 seconde sur mcu
    ser.write(protocol.generate_led_command(protocol.Leds.BLINK_GREEN))
    print_code(HEADER_W, ser)
    print_code(PAYLOAD_W, ser)

    # test allumer led rouge 
    ser.write(protocol.generate_led_command(protocol.Leds.UP_RED))
    print_code(HEADER_W, ser)
    print_code(PAYLOAD_W, ser)

    # wait
    time.sleep(0.5)

    # test éteindre led rouge 
    ser.write(protocol.generate_led_command(protocol.Leds.DOWN_RED))
    print_code(HEADER_W, ser)
    print_code(PAYLOAD_W, ser)

    # wait
    time.sleep(0.5)

    # test led rouge 1 seconde sur mcu
    ser.write(protocol.generate_led_command(protocol.Leds.BLINK_RED))
    print_code(HEADER_W, ser)
    print_code(PAYLOAD_W, ser)

    # test led innexistante
    ser.write(b'\x03\x02\xfb')
    print_code(HEADER_W, ser)
    ser.write(b'\x00\xff')
    print_expect(32)
    print_code(PAYLOAD_W, ser)

    # test checksum incorrecte
    ser.write(b'\x03\x01')
    print_expect(17)
    print_code(HEADER_W, ser)

    # femerture du port
    ser.close()

if __name__ == "__main__":
    main()
