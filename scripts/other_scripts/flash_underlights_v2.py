#!/usr/bin/env python3

import time
from trilobot import Trilobot

"""
This example will demonstrate the RGB underlights of Trilobot,
by making them flash in a red, green and blue sequence.
"""
print("Trilobot Example: Flash Underlights\n")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# LED flashing variables
led_state = False
flash_interval = 0.5  # in seconds

LOOPS = 10  # How many times to play the LED animation
interval = 0.5  # Control the speed of the LED animation

tbot = Trilobot()

last_time = time.time()

led = False

while True:
    print(last_time, led)
    current_time = time.time()
    print(current_time - last_time)

    # If enough time has passed since the last change, consider it stable
    if(current_time - last_time) >= interval:
        if led == True:
            tbot.clear_underlighting()
            led = False
            print("OFF")
            last_time = time.time()
        else:
            tbot.fill_underlighting(RED)
            led = True
            print("ON")
            last_time = time.time()