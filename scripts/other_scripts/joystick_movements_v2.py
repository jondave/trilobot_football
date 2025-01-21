#!/usr/bin/env python3

import time
from trilobot import Trilobot
import sys, termios, tty, os, time
import struct
import math

"""
An example of how move Trilobot with Logitech games controller..
# https://www.socsci.ru.nl/wilberth/computer/joystick.html #
"""
print("Trilobot Example: Joystick Movement Using Eight Way Joystick Mapping\n")

device_path = "/dev/input/js0"

tbot = Trilobot()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

LIGHT_FRONT_RIGHT = 0
LIGHT_FRONT_LEFT = 1
LIGHT_MIDDLE_LEFT = 2
LIGHT_REAR_LEFT = 3
LIGHT_REAR_RIGHT = 4
LIGHT_MIDDLE_RIGHT = 5

joy_x = 0
joy_y = 0

with open(device_path, "rb") as device_file:
    while True:
        event_data = device_file.read(8)
        t, value, event_type, event_number = struct.unpack("<Ihbb", event_data ) # 4 bytes, 2 bytes, 1 byte, 1 byte
        # t: time in ms
        # index: button/axis number (0 for x-axis)
        # code: 1 for buttons, 2 for axis
        # value: axis position, 0 for center, 1 for buttonpress, 0 for button release

        if event_type == 2 and event_number == 1: # if event_type is joystick and event_number is left stick up/down
            joy_y = round(value/32767, 2) * -1 # 32767 is the max of the joystick range, x-1 as up is neg numbers

        if event_type == 2 and event_number == 2: # if event_type is joystick and event_number is right stick left/right
            joy_x = round(value/32767, 2) # 32767 is the max of the joystick range

        if event_type == 1 and event_number == 1: # if event_type is button and event_number is a button press
            print("A button pressed")
            tbot.stop()
            tbot.clear_underlighting()

        # eight way mapping
        # Determine the magnitude and direction of the joystick input
        speed = math.sqrt(joy_x ** 2 + joy_y ** 2)
        angle = math.atan2(joy_y, joy_x)

        # Check the direction based on angle and magnitude
        if (joy_x == 0.0 and joy_y == 0.0):
            tbot.stop()

        elif -math.pi / 8 <= angle < math.pi / 8:       
            tbot.turn_right(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW, show=False)
            tbot.show_underlighting()

        elif math.pi / 8 <= angle < 3 * math.pi / 8:
            tbot.curve_forward_right(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW, show=False)
            tbot.show_underlighting()

        elif 3 * math.pi / 8 <= angle < 5 * math.pi / 8:
            tbot.forward(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
            tbot.show_underlighting()

        elif 5 * math.pi / 8 <= angle < 7 * math.pi / 8:
            tbot.curve_forward_left(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
            tbot.show_underlighting()


        elif (7 * math.pi / 8 <= angle <= math.pi) or (-math.pi <= angle < -7 * math.pi / 8):
            tbot.turn_left(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
            tbot.show_underlighting()

        elif -7 * math.pi / 8 <= angle < -5 * math.pi / 8:
            tbot.curve_backward_left(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, RED, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, WHITE, show=False)
            tbot.show_underlighting()


        elif -5 * math.pi / 8 <= angle < -3 * math.pi / 8:
            tbot.backward(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, RED, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, WHITE, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, RED, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, WHITE, show=False)
            tbot.show_underlighting()

        elif -3 * math.pi / 8 <= angle < -math.pi / 8:
            tbot.curve_backward_right(speed)
            tbot.set_underlight(LIGHT_FRONT_LEFT, RED, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_LEFT, WHITE, show=False)
            tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
            tbot.set_underlight(LIGHT_FRONT_RIGHT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_MIDDLE_RIGHT, YELLOW, show=False)
            tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW, show=False)
            tbot.show_underlighting()
