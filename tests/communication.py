import serial
import time

import protocol

HEADER_W = "Ecriture header: {}"
PAYLOAD_W = "Ecriture payload: {}"

ser = serial.Serial("/dev/ttySTM32")


def get_code():
    return int.from_bytes(ser.read(1), byteorder='little')


def print_code(msg):
    code = get_code()
    print(msg.format(code))


def print_expect(val):
    print("Expect value: {}".format(val))


def main():
    # test allumer led verte (bleu)
    ser.write(protocol.generate_led_command(protocol.Leds.UP_GREEN))
    print_code(HEADER_W)
    print_code(PAYLOAD_W)

    # wait
    time.sleep(0.5)

    # test éteindre led verte (bleu)
    ser.write(protocol.generate_led_command(protocol.Leds.DOWN_GREEN))
    print_code(HEADER_W)
    print_code(PAYLOAD_W)

    # wait
    time.sleep(0.5)

    # test led 1 seconde sur mcu
    ser.write(protocol.generate_led_command(protocol.Leds.BLINK_GREEN))
    print_code(HEADER_W)
    print_code(PAYLOAD_W)

    # test led innexistante
    ser.write(b'\x03\x02\xfb')
    print_code(HEADER_W)
    ser.write(b'\x00\xff')
    print_expect(32)
    print_code(PAYLOAD_W)

    # test checksum incorrecte
    ser.write(b'\x03\x01')
    print_expect(17)
    print_code(HEADER_W)

    # femerture du port
    ser.close()

if __name__ == "__main__":
    main()
