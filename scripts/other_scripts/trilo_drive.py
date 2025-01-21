#!/usr/bin/env python3
# trilo_drive.py
# esklar/9-nov-2023
#
# this is a little test programme for driving a trilobot using keyboard controls.


# import standard packages
import time
# import trilobot package 
from trilobot import Trilobot

# set some parameters for controlling the trilobot's speed
INITIAL_SPEED = 0.5
INCREMENT = 0.1
MAXIMUM = 1.0
speed = INITIAL_SPEED

# initialise a "tbot" object
tbot = Trilobot()

# loop until user quits
more = True
while ( more ):
    # display menu of options to user
    print( '+-------------+--------------+----------+-----------+------------+------------+----------+' )
    print( '| i = forward | , = backward | j = left | l = right | f = faster | s = slower | q = quit |' )
    print( '+-------------+--------------+----------+-----------+------------+------------+----------+' )
    # read user's input
    c = input( 'please enter command> ' )
    # branch on user's input
    if ( c == 'q' or c == 'Q' ):
        more = False
    elif ( c == 'i' or c == 'I' ):
        print( 'moving forward' )
        tbot.forward( speed )
        time.sleep( 1 )
        tbot.stop()
    elif ( c == ',' ):
        print( 'moving backward' )
        tbot.backward( speed )
        time.sleep( 1 )
        tbot.stop()
    elif ( c == 'j' or c == 'J' ):
        print( 'turning left' )
        tbot.curve_forward_left( speed )
        time.sleep( 1 )
        tbot.stop()
    elif ( c == 'l' or c == 'L' ):
        print( 'turning right' )
        tbot.curve_forward_right( speed )
        time.sleep( 1 )
        tbot.stop()
    elif ( c == 'f' or c == 'F' ):
        print( 'going faster' )
        speed += INCREMENT
        if ( speed > MAXIMUM ):
            speed = MAXIMUM
    elif ( c == 's' or c == 'S' ):
        print( 'going slower' )
        speed -= INCREMENT
        if ( speed <= 0 ):
            speed = INCREMENT
    else:
        print( 'illegal command. please try again.' )
# end of loop
print( 'bye!' )
