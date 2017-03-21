import serial

from util import *
import protocol

ser: serial.Serial = serial.Serial("/dev/ttySTM32")

def main():
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.OFF))
    ser.read(1)

    motorx = protocol.Motors.FRONT_X
    pwm = 50
    motor_dir = protocol.MotorsDirection.FORWARD
    ser.write(protocol.generate_manual_speed_command(motorx, pwm, motor_dir))
    print_code(HEADER_W, ser)
    print_code(PAYLOAD_W, ser)
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.OFF))
    ser.read(ser.in_waiting())


if __name__ == "__main__":
    main()