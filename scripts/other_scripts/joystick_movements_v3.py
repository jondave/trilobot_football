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
print("Trilobot Example: Joystick Movement Using Left and Right Motor Speed Joystick Mapping\n")

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
        
        if (joy_x == 0.0 and joy_y == 0.0):
            tbot.stop()

        # Assuming joy_x and joy_y are in the range of -1 to 1
        max_joystick_value = 1.0

        # Map joy_x and joy_y to motor speeds
        left_speed = max_joystick_value * (joy_y + joy_x)
        right_speed = max_joystick_value * (joy_y - joy_x)

        left_speed = max(-1.0, min(1.0, left_speed))
        right_speed = max(-1.0, min(1.0, right_speed))

        # Conditionally swap left and right speeds when reversing
        if joy_y < 0:
            # Swap left and right speeds
            left_speed, right_speed = right_speed, left_speed

        tbot.set_motor_speeds(left_speed, right_speed)

        
        tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_LEFT, YELLOW, show=False)
        tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
        tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
        tbot.set_underlight(LIGHT_MIDDLE_RIGHT, YELLOW, show=False)
        tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
        tbot.show_underlighting()

