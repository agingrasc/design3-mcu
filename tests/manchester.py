#!/usr/bin/python3.4

import serial
import protocol

from protocol import Adc

ser = serial.Serial("/dev/ttySTM32")

LOGICAL_THRESHOLD = 500
SAMPLE_NUMBER_PER_TRANSITION = 11 # This is the sampling count of the ADC for one logic level

signal = [3076, 3075, 0, 7, 0, 1, 5, 4, 6, 0, 6, 0, 8, 3086, 3076, 3075, 3076, 3076, 3076, 3077, 3076, 3076, 3077, 4095, 1, 4, 8, 0, 0, 4, 2, 0, 4, 0, 3083, 3077, 3075, 3075, 3075, 3075, 3077, 3076, 3076, 3076, 3076, 4, 0, 0, 1, 7, 1, 3, 0, 0, 5, 4095, 3085, 3075, 3074, 3075, 3076, 3076, 3076, 3075, 3076, 3076, 9, 5, 4, 0, 4, 0, 4, 3, 0, 1, 5, 3089, 3074, 3076, 3076, 3074, 3076, 3077, 3076, 3076, 3076, 3076, 0, 5, 8, 2, 0, 0, 0, 0, 0, 5, 3083, 3077, 3075, 3075, 3076, 3077, 3076, 3076, 3075, 3076, 3075, 0, 2, 7, 10, 3, 6, 0, 2, 0, 5, 3662, 3085, 3075, 3076, 3075, 3077, 3076, 3076, 3076, 3075, 3076, 6, 4, 0, 6, 0, 1, 0, 4, 8, 0, 0, 4, 0, 0, 0, 1, 6, 2, 4, 0, 0, 4, 3085, 3077, 3076, 3076, 3075, 3076, 3076, 3076, 3077, 3076, 0, 0, 0, 5, 1, 0, 0, 6, 0, 2, 0, 3101, 3076, 3075, 3076, 3075, 3075, 3075, 3075, 3077, 3075, 3077, 4, 0, 0, 2, 1, 0, 3, 1, 5, 2, 4095, 3079, 3074, 3075, 3075, 3076, 3076, 3076, 3077, 3077, 3075, 4, 0, 0, 0, 4, 1, 0, 0, 3, 0, 4, 3086, 3077, 3075, 3076, 3076, 3075, 3076, 3076, 3076, 3075, 6, 0, 0, 0, 0, 14, 2, 0, 2, 2, 0, 3104, 3075, 3076, 3076, 3076, 3076, 3076, 3076, 3077, 3075, 3077, 8, 0, 0, 6, 2, 0, 2, 0, 2, 6, 4095, 3083, 3076, 3077, 3074, 3077, 3077, 3076, 3076, 3076, 3076, 0, 0, 0, 6, 2, 0, 0, 6, 5, 2, 2, 3085, 3076, 3075, 3076, 3075, 3076, 3081, 3075, 3076, 3076, 6, 4, 1, 0, 2, 3076, 3076, 3075, 3076, 3077, 3076, 2, 0, 0, 4, 0, 4, 7, 0, 0, 1, 1, 2, 5, 5, 0, 0, 4, 0, 8, 0, 1, 3074, 3075, 3076, 3076, 3076, 3074, 3076, 3076, 3076, 3078, 3076, 0, 4, 0, 0, 0, 0, 0, 1, 2, 0, 4095, 3084, 3077, 3076, 3076, 3076, 3077, 3077, 3077, 3076, 3076, 0, 0, 6, 2, 4, 8, 1, 0, 4, 4, 6, 3087, 3076, 3074, 3076, 3076, 3076, 3076, 3076, 3076, 3076, 0, 0, 0, 5, 0, 0, 4, 0, 0, 8, 8, 3085, 3076, 3074, 3076, 3076, 3075, 3076, 3077, 3076, 3076, 3076, 0, 7, 1, 2, 8, 2, 0, 2, 0, 0, 4095, 3085, 3076, 3075, 3075, 3074, 3076, 3075, 3076, 3076, 3076, 5, 5, 4, 3, 1, 0, 2, 1, 0, 6, 10, 3088, 3077, 3074, 3075, 3076, 3076, 3076, 3076, 3076, 3077, 8, 8, 5, 1, 0, 0, 0, 5, 0, 3, 13, 3086, 3075, 3074, 3075, 3076, 3076, 3076, 3076, 3076, 3077, 3077, 1, 0, 0, 0, 0, 1, 0, 9, 0, 0, 4095, 3087, 3076, 3076, 3073, 3075, 3075, 3076, 3076, 3076, 3077, 3076, 3076, 3076, 3075, 3076, 3076, 3075, 3076, 3076, 3076, 3076, 3, 0, 0, 0, 0, 5, 3, 5, 1, 8, 4095, 3086, 3076, 3074, 3075, 3075, 3074]

def manchester_decode(input_signal: list):
    # Step 1: convert the input to logical 0 and 1
    for i in range(0, len(input_signal)):
        if input_signal[i] < LOGICAL_THRESHOLD:
            input_signal[i] = 0
        else:
            input_signal[i] = 1

    # Step 2: find the first valid logic level index in buffer
    count = 0
    current_level = input_signal[0]
    buffer = []
    idx = 0
    last_idx = 0
    for i in range(0, len(input_signal)):
        if input_signal[i] == current_level:
            count += 1
        else: # Level changed
            if count >= SAMPLE_NUMBER_PER_TRANSITION/2:
                while input_signal[i] == current_level:
                    i += 1

                idx = i
                print("thats it idx is {}".format(idx))
                break
            else:
                print("i is {}".format(i))
                last_idx = i
                count = 1
                current_level = input_signal[i]
                print("curr level is now {}".format(current_level))

    # Step 3: Process the logic levels and isolate each bit
    current_bit = input_signal[last_idx]
    current_level = current_bit
    count = 0
    print("idx is {}".format(idx))
    i = last_idx
    while i < len(input_signal):
        if input_signal[i] == current_level:
            count += 1
        else:
            if count >= (SAMPLE_NUMBER_PER_TRANSITION + (SAMPLE_NUMBER_PER_TRANSITION/2)):
                count = 0
                buffer.append(current_level)
                buffer.append(current_level)
                while input_signal[i] == current_level:
                    i += 1
                current_level = input_signal[i]
            elif count >= SAMPLE_NUMBER_PER_TRANSITION/2:
                count = 0
                buffer.append(current_level)
                while input_signal[i] == current_level:
                    i += 1
                current_level = input_signal[i]

        i += 1

    # Step 4: Search for valid token (start bit (LOW) + 8 stop bits (HIGH))
    startBit = ['']
    validToken = ['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '1', '1', '1', ]
    # Manchester:
    # Low = LOW + HIGH
    # High = HIGH + LOW
    i = len(input_signal)
    while i >= 0:

        i -= 1

    return buffer


def read_last_adc(adc_id: protocol.Adc, ser=ser) -> tuple:
    ser.read(ser.inWaiting())
    ser.write(protocol.generate_read_last_adc(adc_id))
    ser.read(1)
    nbytes = int.from_bytes(ser.read(2), byteorder='big') # Number of values
    values = []
    for i in range(1,nbytes-1):
        val = ser.read(2)
        values.append(int.from_bytes(val, byteorder='big'))
    return (nbytes, values) #int.from_bytes(val, byteorder='big')

def main():
    run = True
    while run:
        cmd = input('Command to exec ("q" to quit): ')
        if cmd == 'q':
            run = False
        else:
            ch = int(input('Channel: '))
            ncmd = int(cmd)
            (n, values) = read_last_adc(Adc.ADC_MANCHESTER_CODE)
            print(n)
            print(values)

if __name__ == "__main__":
    #main()
    buf = manchester_decode(signal)
    print(buf)
