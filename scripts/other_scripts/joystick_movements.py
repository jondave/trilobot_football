#!/usr/bin/env python3

import time
from trilobot import Trilobot
import sys, termios, tty, os, time
import struct

"""
An example of how move Trilobot with Logitech games controller..
# https://www.socsci.ru.nl/wilberth/computer/joystick.html #
"""
print("Trilobot Example: Joystick Movement Using Four Way Joystick Mapping\n")

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

with open(device_path, "rb") as device_file:
    while True:
        event_data = device_file.read(8)
        t, value, event_type, event_number = struct.unpack("<Ihbb", event_data ) # 4 bytes, 2 bytes, 1 byte, 1 byte
        # t: time in ms
        # index: button/axis number (0 for x-axis)
        # code: 1 for buttons, 2 for axis
        # value: axis position, 0 for center, 1 for buttonpress, 0 for button release

        if event_type == 2 and event_number == 1: # if event_type is joystick and event_number is left stick up/down
            speed = round(value/32767, 2) * -1 # 32767 is the max of the joystick range, x-1 as up is neg numbers
            print("X speed: " + str(speed))
            
            if speed > 0:
                print("Forward")
                tbot.forward(speed)
                tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
                tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
                tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
                tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
                tbot.show_underlighting()

            elif speed <0:
                print("Reverse")
                tbot.forward(speed)
                tbot.set_underlight(LIGHT_FRONT_LEFT, RED, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
                tbot.set_underlight(LIGHT_REAR_LEFT, WHITE, show=False)
                tbot.set_underlight(LIGHT_FRONT_RIGHT, RED, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
                tbot.set_underlight(LIGHT_REAR_RIGHT, WHITE, show=False)
                tbot.show_underlighting()

        if event_type == 2 and event_number == 2: # if event_type is joystick and event_number is right stick left/right
            speed = round(value/32767, 2) # 32767 is the max of the joystick range
            print("Turn speed: " + str(speed))

            if speed > 0:
                print("Left")
                tbot.turn_left(round(speed * - 1, 2)) # *-1 as numbers are negative on joystick for left
                tbot.set_underlight(LIGHT_FRONT_LEFT, YELLOW, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_LEFT, YELLOW, show=False)
                tbot.set_underlight(LIGHT_REAR_LEFT, YELLOW, show=False)
                tbot.set_underlight(LIGHT_FRONT_RIGHT, WHITE, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_RIGHT, BLACK, show=False)
                tbot.set_underlight(LIGHT_REAR_RIGHT, RED, show=False)
                tbot.show_underlighting()

            elif speed <0:
                print("Right")
                tbot.turn_right(speed)
                tbot.set_underlight(LIGHT_FRONT_LEFT, WHITE, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_LEFT, BLACK, show=False)
                tbot.set_underlight(LIGHT_REAR_LEFT, RED, show=False)
                tbot.set_underlight(LIGHT_FRONT_RIGHT, YELLOW, show=False)
                tbot.set_underlight(LIGHT_MIDDLE_RIGHT, YELLOW, show=False)
                tbot.set_underlight(LIGHT_REAR_RIGHT, YELLOW, show=False)
                tbot.show_underlighting()

        if event_type == 1 and event_number == 1: # if event_type is button and event_number is a button press
            print("A button pressed")
            tbot.stop()
            tbot.clear_underlighting()
