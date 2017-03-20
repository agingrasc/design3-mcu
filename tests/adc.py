"""" Sanity test des lectures des adc """
import serial
import time
import curses

import protocol as protocol
from protocol import Adc
from util import *

WAIT_DELTA = 0.100
wait = ['|', '/', '-', '\\', '|', '/', '-', '\\']
wait_idx = 0
last_wait_update = time.time()

ser = serial.Serial("/dev/ttySTM32")

force_sensor_resistor_m_value = 1000
force_sensor_voltage = 5
adc_voltage = 3
adc_max_val = 4095

def init():
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.OFF))
    ser.write(protocol.generate_led_command(protocol.Leds.UP_GREEN))


def deinit():
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.ON))
    ser.write(protocol.generate_led_command(protocol.Leds.DOWN_GREEN))

def convert_adc_value_to_voltage(adc_value):
    return (adc_voltage*adc_value)/adc_max_val

def convert_voltage_to_force_sensor_resistance(voltage):
    if voltage == 0: return 9999999 # No division by default
    return ((force_sensor_voltage*force_sensor_resistor_m_value)/voltage) - force_sensor_resistor_m_value

def continuous(screen):
    screen.clear()
    screen.nodelay(True)

    sub_run = True
    while sub_run:
        time.sleep(0.060)
        ser.read(ser.inWaiting())

        try:
            user_key = screen.getstr(3)
        except curses.error:
            user_key = -1

        if user_key in ['q', 'Q']:
            sub_run = False

        (n, adc_vals) = read_last_adc(protocol.Adc.ADC_PENCIL)
        adc_val = adc_vals[0]
        adc_volt = convert_adc_value_to_voltage(adc_val)
        rfsr = convert_voltage_to_force_sensor_resistance(adc_volt)

        screen.clear()
        screen.addstr(0, 0, "ADC pencil value: ADC={}, Vadc={:0.2f}, Rfsr={:0.2f}".format(adc_val, adc_volt, rfsr))

        display_busy_wait(screen, 1)
        screen.move(3, 0)

    screen.nodelay(False)
    return None

def display_busy_wait(screen, row):
    global last_wait_update
    now = time.time()
    if now - last_wait_update > WAIT_DELTA:
        global wait_idx
        screen.addstr(row, 0, wait[wait_idx])
        wait_idx = (wait_idx + 1) % len(wait)
        last_wait_update = now


def read_last_adc(adc_id: protocol.Adc, ser=ser) -> tuple:
    ser.read(ser.inWaiting())
    ser.write(protocol.generate_read_last_adc(adc_id))
    ser.read(1)
    nbytes = int.from_bytes(ser.read(2), byteorder='big') # Number of values
    values = []
    values = []
    for i in range(1,nbytes-1):
        bval = ser.read(2)
        val = int.from_bytes(bval, byteorder='big')
        if val > 1000:
            values.append(1)
        else:
            values.append(0)
        #values.append()

    return (nbytes, values) #int.from_bytes(val, byteorder='big')

def oneshot(screen):

    run = True
    lastval = ""
    while run:
        screen.clear()
        screen.nodelay(False)
        curses.echo()

        screen.addstr(1, 0, "ADC channels: 1 = manchester power, 2 = manchester code, 3 = force sensor output")
        screen.addstr(2, 0, "ADC channel ['q' to quit]: ")
        screen.addstr(3, 0, "")
        screen.addstr(4, 0, "ADC samples:")
        screen.addstr(5, 0, lastval)

        cmd = screen.getkey()

        screen.nodelay(True)
        curses.noecho()
        if cmd == 'q':
            run = False
        elif cmd != -1:
            (n, values) = read_last_adc(Adc.ADC_MANCHESTER_CODE)
            lastval = str(values).strip('[]')

def display_menu(screen):
    screen.clear()
    screen.addstr("Continuous|One-shot")
    screen.move(1, 0)

def main(screen):
    init()
    run = True
    screen.nodelay(True)
    display_menu(screen)
    while run:
        display_busy_wait(screen, 2)
        screen.move(1, 0)
        try:
            user_input = screen.getkey()
        except curses.error:
            user_input = -1

        if user_input in ['q', 'Q']:
            run = False
        elif user_input == 'C':
            continuous(screen)
            display_menu(screen)
        elif user_input == 'O':
            oneshot(screen)
            display_menu(screen)

    deinit()

if __name__ == "__main__":
    curses.wrapper(main)