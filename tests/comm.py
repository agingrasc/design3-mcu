import serial
import time

ser = serial.Serial("/dev/ttyACM5")

# test allumer led verte (bleu)
ser.write(b'\x03\x01')
print(ser.read(1))
ser.write(b'\x01')
print(ser.read(1))

# wait
time.sleep(1)

# test éteindre led verte (bleu)
ser.write(b'\x03\x01')
print(ser.read(1))
ser.write(b'\x03')
print(ser.read(1))

# test led innexistante
ser.write(b'\x03\x01')
print(ser.read(1))
ser.write(b'\x05')
print(ser.read(1))
ser.close()
