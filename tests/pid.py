import serial

import protocol

ser = serial.Serial("/dev/ttySTM32")

if __name__ == "__main__":
    cmd = protocol.generate_set_pid_constant(protocol.Motors.FRONT_X, 0.016877, 0.03873, 0)
    ser.write(cmd)
    print(ser.read(1))