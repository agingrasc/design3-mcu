import serial

HEADER_W = "Ecriture header: {}"
PAYLOAD_W = "Ecriture payload: {}"


def get_code(ser: serial.Serial):
    return int.from_bytes(ser.read(1), byteorder='little')


def print_code(msg, ser: serial.Serial):
    code = get_code(ser)
    print(msg.format(code))


def print_expect(val):
    print("Expect value: {}".format(val))

