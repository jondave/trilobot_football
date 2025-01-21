# This script uses the camera mounted on the trilobot to detect and locate balls of different colors in the image. 
# The location of the ball with a specific color (defined by the user) in the image is used to make 
# the robot rotate in a way that the ball stays detected in the center of the image.
# When the robot detects a ball with a specific color wanted, the LEDs are activated in that color, otherwise they are turned off.

from picamera2 import Picamera2
import cv2
import numpy
from trilobot import Trilobot

# create the robot object
tbot = Trilobot()

# create the pi camera object
picam = Picamera2()
picam.configure(picam.create_preview_configuration(main={"format": 'BGR888', "size": (320, 240)}))
picam.start()

# RGB Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Color wanted to be tracked
color_wanted="RED" # it can be "RED", "YELLOW", "GREEN", "BLUE"
  
def circle_detection(image):  
    # Convert to grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 30,
                   param2 = 80, minRadius = 0, maxRadius = 0)
    # Count and locate the circles that are detected.
    x=[] # list with x component of the circles detected
    y=[] # list with y component of the circles detected
    r=[] # list with the radius of the circles detected
    if detected_circles is not None:
        num_circles=len(detected_circles[0,:,0])  
        # Convert the circle parameters x, y and r to integers.
        detected_circles = numpy.uint16(numpy.around(detected_circles))
        for pt in detected_circles[0,:]:
            x.append(pt[0])
            y.append(pt[1])
            r.append(pt[2])
    else:
        num_circles=0
    return num_circles,x,y,r

def check_color(mask,h,w,x,y,r):
    
    search_top = max(int(y - r),0)
    search_bot = min(int(y + r),h)
    search_left = max(int(x - r),0)
    search_right = min(int(x + r),w)
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    mask[0:h, 0:search_left] = 0
    mask[0:h, search_right:w] = 0
    
    M = cv2.moments(mask)
    if M['m00'] > 0:
        color_det=True
    else:
        color_det=False
    return color_det,[M['m00'],M['m10'],M['m01']]

def color_detection(image,color_wanted,x,y,r):
    ## convert to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    ## mask of red 
    mask_r_lower = cv2.inRange(hsv, (0,0,0), (10, 255, 255))
    mask_r_upper = cv2.inRange(hsv, (170,0,0), (180, 255, 255))
    mask_r=cv2.bitwise_or(mask_r_lower, mask_r_upper)
    ## mask of yellow 
    mask_y = cv2.inRange(hsv, (15,0,0), (36, 255, 255))
    ## mask of green 
    mask_g = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))
    ## mask of blue 
    mask_b = cv2.inRange(hsv, (100,0,0), (135, 255, 255))

    h, w, d = image.shape
    index=[]
    color_detected=False
    for circle_index in range(len(x)):
        ## Masking
        [color_det_r,M_r]=check_color(mask_r,h,w,x[circle_index],y[circle_index],r[circle_index])
        [color_det_y,M_y]=check_color(mask_y,h,w,x[circle_index],y[circle_index],r[circle_index])
        [color_det_g,M_g]=check_color(mask_g,h,w,x[circle_index],y[circle_index],r[circle_index])
        [color_det_b,M_b]=check_color(mask_b,h,w,x[circle_index],y[circle_index],r[circle_index])       

        ## Detecting the color (R,Y,G,B) of the ball             
        color_det=[color_det_r,color_det_y,color_det_g,color_det_b]
        M=[M_r[0],M_y[0],M_g[0],M_b[0]]
        unknown_color=True
        for j in range(4):
            # Is the ball of a known color?
            if color_det[j]==True:
                if unknown_color==True:
                    color_index=j
                    unknown_color=False
                # To prioritize the color detected with bigger M0
                if M[j]>M[color_index]:
                    color_index=j
        if unknown_color==False:
            if color_index==0:
                object_color="RED"
            elif color_index==1:
                object_color="YELLOW"
            elif color_index==2:
                object_color="GREEN"
            elif color_index==3:
                object_color="BLUE"
        else:
            object_color="UNKNOWN"
        if object_color==color_wanted:
            index=circle_index
            color_detected=True
            break
        
    return color_detected,index,w

def activate_leds(color_wanted):
    if color_wanted=="RED":
        tbot.fill_underlighting(RED)
    elif color_wanted=="YELLOW":
        tbot.fill_underlighting(YELLOW)
    elif color_wanted=="GREEN":
        tbot.fill_underlighting(GREEN)
    elif color_wanted=="BLUE":
        tbot.fill_underlighting(BLUE)   

def ball_tracking(x,w):
    err_x = x - w/2
    vel = 0.5*(-float(err_x) / 100)
    print("VELOCITY",vel)
    if abs(vel)<0.15:
        tbot.disable_motors()
    else:
        tbot.set_motor_speeds(-vel, vel)
              
while True or KeyboardInterrupt:
    image = picam.capture_array()
    [num_balls,x,y,r]=circle_detection(image)
    if num_balls>0:
        [color_detected,ball_index,w]=color_detection(image,color_wanted,x,y,r)
        if color_detected==True:
            print("NUMBER OF BALLS:",num_balls,"TRACKING ",color_wanted)
            ball_tracking(x[ball_index],w) 
            activate_leds(color_wanted)            
        else:
            print("NUMBER OF BALLS:",num_balls)
            tbot.fill_underlighting(BLACK)  
            tbot.disable_motors()
    else:
        print("NUMBER OF BALLS:",num_balls)
        tbot.fill_underlighting(BLACK)  
        tbot.disable_motors()
