import serial
import time

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


# test allumer led verte (bleu)
ser.write(b'\x03\x01\xfc')
print_code(HEADER_W)
ser.write(b'\x01')
print_code(PAYLOAD_W)

# wait
time.sleep(1)

# test éteindre led verte (bleu)
ser.write(b'\x03\x01\xfc')
print_code(HEADER_W)
ser.write(b'\x03')
print_code(PAYLOAD_W)

# test led innexistante
ser.write(b'\x03\x01\xfc')
print_code(HEADER_W)
ser.write(b'\x05')
print_expect(32)
print_code(PAYLOAD_W)

# test checksum incorrecte
ser.write(b'\x03\x01')
print_expect(17)
print_code(HEADER_W)

# femerture du port
ser.close()
