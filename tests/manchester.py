import serial
import protocol

from typing import List

from protocol import Adc

LOGICAL_THRESHOLD = 500
SAMPLE_NUMBER_PER_TRANSITION = 11 # This is the sampling count of the ADC for one logic level

ser = serial.Serial("/dev/ttySTM32")

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
    last_idx = 0
    for i in range(0, len(input_signal)):
        if input_signal[i] == current_level:
            count += 1
        else: # Level changed
            if count >= SAMPLE_NUMBER_PER_TRANSITION/2:
                while input_signal[i] == current_level:
                    i += 1

                #print("thats it idx is {}".format(idx))
                break
            else:
                #print("i is {}".format(i))
                last_idx = i
                count = 1
                current_level = input_signal[i]
                #print("curr level is now {}".format(current_level))

    # Step 3: Process the logic levels and isolate each bitT t
    current_level = input_signal[last_idx]
    count = 0
    #print("idx is {}".format(idx))
    buffer = []
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

    #print('buffer is')
    #print(buffer)
    #print('\n')

    # Step 4: Search for valid token (start bit (LOW) + 8 stop bits (HIGH))
    stopBits = [1, 0] * 8
    startBit = stopBits + [0, 1]
    data = [-1] * 14 # -1 means don't care (there are 7 data bits)
    validToken = startBit + data + stopBits

    #print('valid token is ')
    #print(validToken)
    #print('\n')

    dataBits = []
    # Manchester:
    # Low = LOW + HIGH
    # High = HIGH + LOW
    i = len(buffer) - 1
    valid = False
    #it = 0
    while i >= 0 or not valid:
        dataBits = []
        #print('## it no {}'.format(it))
        #print('i = {}'.format(i))
        validn = 0
        if i < len(buffer)-len(validToken):
            #print('i < len(validToken): {} < {}'.format(i, len(buffer)-len(validToken)))
            valid = False
            break

        t = i
        j = len(validToken) - 1
        print('len(validToken) is {}'.format(len(validToken)))
        while (buffer[t] == validToken[j] or validToken[j] == -1) and (t >= 0 and j >= 0):
            if validToken[j] == -1:
                dataBits.append(buffer[t])

            t -= 1
            j -= 1
            validn += 1

        #print('validn == len(validToken) ? {} == {}'.format(validn, len(validToken)))
        if validn == len(validToken):
            #print("Found something valid")
            valid = True
            break

        i -= 1
        #it += 1


    if not valid: return None

    #print('data bits: ')
    #print(dataBits)
    #print('\n')

    # Step 5: return real data bits

    i = 0
    retval = []
    while i < len(dataBits):
        if dataBits[i] == 0 and dataBits[i+1] == 1:
            retval.append(0)
        elif dataBits[i] == 1 and dataBits[i+1] == 0:
            retval.append(1)

        i += 2

    return retval

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

def get_manchester_code_power(ser=ser) -> tuple:
    ser.read(ser.inWaiting())
    ser.write(protocol.generate_get_manchester_power_cmd())
    ser.read(1)

    pow = int.from_bytes(ser.read(2), byteorder='big')

    return pow

def manchester_decode_cmd(ser=ser) -> tuple:
    ser.read(ser.inWaiting())
    ser.write(protocol.generate_decode_manchester())
    ser.read(1)
    res = int.from_bytes(ser.read(1), byteorder='big') # Decode result (success or error)
    figNo = int.from_bytes(ser.read(1), byteorder='big')
    orien = int.from_bytes(ser.read(1), byteorder='big')
    scale = int.from_bytes(ser.read(1), byteorder='big')
    #val = int.from_bytes(ser.read(2), byteorder='big') # Code packed into uint8

    return (res, [figNo, orien, scale])

def main():
    run = True
    while run:
        print('Commands: "a" = read adc, "d" = decode manchester, "p" = get manchester code power)')
        cmd = input('Command to exec ("q" to quit): ')
        if cmd == 'q':
            run = False
        elif cmd == 'd':
            (res, minfos) = manchester_decode_cmd()
            print('command result is {}'.format(res))
            if res == 0:
                print("figure # = {}, orientation = {}, scale = {}".format(minfos[0], protocol.ManchesterOrientation(minfos[1]), protocol.ManchesterScale(minfos[2])))
        elif cmd == 'a':
            ch = int(input('Channel: '))
            (n, values) = read_last_adc(Adc.ADC_MANCHESTER_CODE)
            decoded = manchester_decode(values)
            if decoded != None:
                print('decoded:')
                print(decoded)
        elif cmd == 'p':
            pow = get_manchester_code_power()
            print('Last manchester signal voltage sampled: {}'.format(pow))

if __name__ == "__main__":
    main()
