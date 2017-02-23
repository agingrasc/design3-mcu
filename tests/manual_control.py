import curses
import sys
import time

import protocol
from encodeur import read_encoder
from util import *

ser = serial.Serial("/dev/ttySTM32")

DEFAULT_SPEED = 40
DEFAULT_DIRECTION = protocol.MotorsDirection.FORWARD
DEFAULT_COMM_SLEEP = 0.050
WAIT_DELTA = 0.100

motors_id = {1: protocol.Motors.REAR_X,
             2: protocol.Motors.FRONT_Y,
             3: protocol.Motors.FRONT_X,
             4: protocol.Motors.REAR_Y}

directions = {'f': protocol.MotorsDirection.FORWARD,
              'b': protocol.MotorsDirection.BACKWARD}

wait = ['|', '/', '-', '\\', '|', '/', '-', '\\']
wait_idx = 0
last_wait_update = time.time()


def init():
    ser.write(protocol.generate_toggle_pid())
    ser.write(protocol.generate_led_command(protocol.Leds.UP_GREEN))


def deinit():
    ser.write(protocol.generate_toggle_pid())
    ser.write(protocol.generate_led_command(protocol.Leds.DOWN_GREEN))


def keyboard(screen):
    screen.clear()
    screen.nodelay(True)

    speed_x = 0
    speed_y = 0

    sub_run = True
    while sub_run:
        time.sleep(0.060)
        ser.read(ser.inWaiting())

        try:
            user_key = screen.getkey()
        except curses.error:
            user_key = -1

        set_motor_to_keyboard_speed(speed_x, speed_y)

        if user_key in ['q', 'Q']:
            sub_run = False
        elif user_key == 'w':
            speed_x += 5
        elif user_key == 's':
            speed_x -= 5
        elif user_key == 'd':
            speed_y += 5
        elif user_key == 'a':
            speed_y -= 5
        elif user_key in ['c']:
            speed_x = 0
            speed_y = 0

        speed_x, speed_y = cap_speed(speed_x, speed_y)

        screen.clear()
        screen.addstr(0, 0, "Speed in x: {}".format(speed_x))
        screen.addstr(1, 0, "Speed in y: {}".format(speed_y))
        display_busy_wait(screen, 2)
        screen.move(3, 0)

    screen.nodelay(False)
    return None


def cap_speed(speed_x, speed_y):
    if speed_x > 100:
        speed_x = 100
    elif speed_x < -100:
        speed_x = -100
    if speed_y > 100:
        speed_y = 100
    elif speed_y < -100:
        speed_y = -100
    return speed_x, speed_y


def set_motor_to_keyboard_speed(speed_x, speed_y):
    x_motors = (protocol.Motors.FRONT_X, protocol.Motors.REAR_X)
    y_motors = (protocol.Motors.FRONT_Y, protocol.Motors.REAR_Y)
    if speed_x < 0:
        dir_x = protocol.MotorsDirection.BACKWARD
    else:
        dir_x = protocol.MotorsDirection.FORWARD
    if speed_y < 0:
        dir_y = protocol.MotorsDirection.BACKWARD
    else:
        dir_y = protocol.MotorsDirection.FORWARD
    for motor_id in x_motors:
        ser.write(protocol.generate_manual_speed_command(motor_id, speed_x, dir_x))
    for motor_id in y_motors:
        ser.write(protocol.generate_manual_speed_command(motor_id, speed_y, dir_y))


def motor(screen):
    global directions
    screen.nodelay(False)
    screen.clear()
    curses.echo()
    screen.addstr("ID du moteur [1-4]: ")
    motor_id = int(screen.getkey())
    motor_id = motors_id[motor_id]
    screen.addstr(1, 0, "Vitesse du moteur [0-100]: ")
    try:
        speed = int(screen.getstr(3))
    except ValueError:
        speed = DEFAULT_SPEED
    screen.addstr(2, 0, "Direction [f|b]: ")
    try:
        dir_key = screen.getkey()
        direction = directions[dir_key]
    except KeyError:
        direction = DEFAULT_DIRECTION

    curses.noecho()
    screen.clear()
    screen.nodelay(True)

    ser.write(protocol.generate_manual_speed_command(motor_id, speed, direction))
    sub_run = True
    while sub_run:
        ser.read(ser.inWaiting())
        time.sleep(0.050)
        screen.clear()
        motor_speed = read_encoder(motor_id, ser)
        draw_motor_menu(direction, motor_speed, screen, speed)
        try:
            user_key = screen.getkey()
        except curses.error:
            user_key = -1

        if user_key in ['c', 'C', 'q', 'Q']:
            sub_run = False
        elif user_key in ['s', 'S']:
            screen.nodelay(False)
            screen.clear()
            curses.echo()
            try:
                screen.move(0, 0)
                speed = int(screen.getstr(3))
            except ValueError:
                screen.addstr(4, 0, "La vitesse doit etre un nombre valide.")
            curses.noecho()
            screen.nodelay(True)
        elif user_key in ['d', 'D']:
            screen.nodelay(False)
            screen.clear()
            curses.echo()
            try:
                screen.move(0, 0)
                dir_key = screen.getkey()
                direction = directions[dir_key]
            except KeyError:
                screen.addstr(4, 0, "La direction doit etre soit 'c' ou soit 'cc'.")
            curses.noecho()
            screen.nodelay(True)

    ser.write(protocol.generate_manual_speed_command(motor_id, 0, direction))

    return None


def all_motors(screen):
    ser.read(ser.inWaiting())
    screen.clear()
    screen.addstr("Vitesse: ")
    screen.nodelay(False)
    curses.echo()
    try:
        speed = int(screen.getstr(3))
    except ValueError:
        speed = DEFAULT_SPEED

    screen.addstr(1, 0, "Direction (f|b): ")
    try:
        dir_key = screen.getkey()
        direction = directions[dir_key]
    except KeyError:
        direction = DEFAULT_DIRECTION

    screen.nodelay(True)
    curses.noecho()
    screen.clear()
    for motor_id in protocol.Motors:
        ser.write(protocol.generate_manual_speed_command(motor_id, speed, direction))
        ser.read(1)
        time.sleep(DEFAULT_COMM_SLEEP)

    sub_run = True
    while sub_run:
        try:
            user_key = screen.getkey()
        except curses.error:
            user_key = -1

        draw_all_motor_menu(direction, screen, speed)

        if user_key in ['q', 'Q', 'c', 'C']:
            sub_run = False
        elif user_key == 's':
            screen.nodelay(False)
            curses.echo()
            screen.clear()
            try:
                speed = int(screen.getstr(3))
            except ValueError:
                pass
            screen.nodelay(True)
            curses.noecho()
            update_all_motor_cmd(speed, direction)
            draw_all_motor_menu(direction, screen, speed)
        elif user_key == 'd':
            screen.nodelay(False)
            curses.echo()
            screen.clear()
            try:
                dir_key = screen.getkey()
                direction = directions[dir_key]
            except KeyError:
                pass
            screen.nodelay(True)
            curses.noecho()
            update_all_motor_cmd(speed, direction)
            draw_all_motor_menu(direction, screen, speed)

    for motor_id in protocol.Motors:
        ser.write(protocol.generate_manual_speed_command(motor_id, 0, direction))
        time.sleep(DEFAULT_COMM_SLEEP)

    return None


def update_all_motor_cmd(speed, direction):
    for motor_id in protocol.Motors:
        ser.write(protocol.generate_manual_speed_command(motor_id, speed, direction))
        time.sleep(DEFAULT_COMM_SLEEP)


def draw_all_motor_menu(direction, screen, speed):
    screen.addstr(0, 0, "Commande de {} avec une direction {}".format(speed, direction))
    for idx, motor_id in enumerate(protocol.Motors):
        time.sleep(DEFAULT_COMM_SLEEP)
        motor_speed = read_encoder(motor_id, ser)
        ser.read(1)
        screen.addstr(idx * 2 + 1, 0, "Moteur {}: {}".format(idx, motor_speed))
    screen.addstr(9, 0, "Appuyer sur 's' pour changer la vitesse.")
    screen.addstr(10, 0, "Appuyer sur 'd' pour changer la direction.")
    screen.addstr(11, 0, "Appuyer sur 'q' pour revenir au menu principal")
    display_busy_wait(screen, 8)
    screen.move(12, 0)


def draw_motor_menu(direction, motor_speed, screen, speed):
    screen.addstr(0, 0,
                  "Vitesse du moteur: {} -- avec une commande de {} et une direction {}".format(motor_speed, speed,
                                                                                                direction))
    screen.addstr(1, 0, "Appuyer sur 'q' pour revenir au menu principal")
    screen.addstr(2, 0, "Appuyer sur 's' pour changer la vitesse")
    screen.addstr(3, 0, "Appuyer sur 'd' pour changer la direction")
    display_busy_wait(screen, 5)
    screen.move(4, 0)


def display_menu(screen):
    screen.clear()
    screen.addstr("Motor|All-motors|Keyboard")
    screen.move(1, 0)


def display_busy_wait(screen, row):
    global last_wait_update
    now = time.time()
    if now - last_wait_update > WAIT_DELTA:
        global wait_idx
        screen.addstr(row, 0, wait[wait_idx])
        wait_idx = (wait_idx + 1) % len(wait)
        last_wait_update = now


dispatch = {'keyboard': keyboard,
            'motor': motor,
            'all-motors': all_motors}


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
        elif user_input == 'M':
            motor(screen)
            display_menu(screen)
        elif user_input == 'A':
            all_motors(screen)
            display_menu(screen)
        elif user_input == 'K':
            keyboard(screen)
            display_menu(screen)

    deinit()


if __name__ == "__main__":
    curses.wrapper(main)
