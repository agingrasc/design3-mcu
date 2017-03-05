import serial

import protocol
from util import *

ser = serial.Serial("/dev/ttySTM32")

if __name__ == "__main__":
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.OFF))
    print_code("cmd status: ", ser)

    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.ON))
    print_code("cmd status: ", ser)
    ser.close()
