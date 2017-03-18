#!/usr/bin/python3.4

import serial
import struct

# Serial device
ser = serial.Serial('/dev/ttyPololu')
 
# Pololu default device ID
POL_DEVICE_ID = 0x0C

# Pololu commands
POL_CMD_SET_TARGET = 0x84 #0x04
POL_CMD_GET_TARGET = 0x90 #0x10
POL_START_CMD = 0xAA

commands = {1: POL_CMD_SET_TARGET,
            2: POL_CMD_GET_TARGET}

# Servos channel number
CHN_CAMERA_X = 0x0
CHN_CAMERA_Y = 0x1
CHN_PENCIL = 0x2

def _send_cmd(cmd, channel, payload):
    ser.write(bytes([cmd, channel]) + payload)

def set_target(channel):
    target = int(input('Target position: '))
    target *= 4 # Expects target in quarter-microseconds unit
    payload = bytes([target & 0x7F, target >> 7 & 0x7F])

    _send_cmd(POL_CMD_SET_TARGET, channel, payload)

def get_target(channel):
    payload = bytes([])
    _send_cmd(POL_CMD_GET_TARGET, channel, payload)
    
    res = ser.read(2)

    tgt = (res[1] << 8) + res[0]

    # Returns tgt in quarter-microseconds unit
    tgt /= 4

    return tgt

def main():
    run = True
    while run:
        cmd = input('Command to exec ("q" to quit): ')
        if cmd == 'q':
            run = False
        else:
            ch = int(input('Channel: '))
            ncmd = int(cmd)
            if commands[ncmd] == POL_CMD_SET_TARGET:
                set_target(ch)
            elif commands[ncmd] == POL_CMD_GET_TARGET:
                tgt = get_target(ch)
                print(tgt)

if __name__ == "__main__":
    main()
