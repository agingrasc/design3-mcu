"""" Sanity test des lectures des adc """
import serial
import time
import curses

import protocol as protocol
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

def main(screen):
    screen.clear()
    screen.nodelay(True)

    speed_x = 0
    speed_y = 0

    target_changed = False
    sub_run = True
    while sub_run:
        time.sleep(0.060)
        ser.read(ser.inWaiting())

        try:
            user_key = screen.getkey()
        except curses.error:
            user_key = -1

        if user_key in ['q', 'Q']:
            sub_run = False

        adc_val = read_last_adc(protocol.Adc.ADC_PENCIL)
        adc_volt = convert_adc_value_to_voltage(adc_val)
        rfsr = convert_voltage_to_force_sensor_resistance(adc_volt)

        screen.clear()
        screen.addstr(0, 0, "ADC pencil value: ADC={}, Vadc={:0.2f}, Rfsr={:0.2f}".format(adc_val, adc_volt, rfsr))
        #screen.addstr(1, 0, "Speed in y: {}mm/s ({:0.0f} tick/s)".format(speed_y, convert_to_tick(speed_y)))

        display_busy_wait(screen, 1)
        screen.move(3, 0)

    screen.nodelay(False)
    ser.write(protocol.generate_set_pid_mode(protocol.PIDStatus.OFF))
    return None

def display_busy_wait(screen, row):
    global last_wait_update
    now = time.time()
    if now - last_wait_update > WAIT_DELTA:
        global wait_idx
        screen.addstr(row, 0, wait[wait_idx])
        wait_idx = (wait_idx + 1) % len(wait)
        last_wait_update = now


def read_last_adc(adc_id: protocol.Adc, ser=ser) -> int:
    ser.read(ser.inWaiting())
    ser.write(protocol.generate_read_last_adc(adc_id))
    ser.read(1)
    ser.read(1) # Number of vaues
    val = ser.read(2)
    return int.from_bytes(val, byteorder='big')

if __name__ == "__main__":
    curses.wrapper(main)