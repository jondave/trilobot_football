# This script uses the camera mounted on the trilobot to detect and count the number of balls in the image. 
# The ball detection is activated when an object is detected within a specific distance.
# When the robot is detecting balls, the LEDs are activated in red color, otherwise they are turned off.

from picamera2 import Picamera2
import cv2
import numpy as np
from trilobot import Trilobot
import time

# create the robot object
tbot = Trilobot()

# create the pi camera object
picam = Picamera2()
picam.configure(picam.create_preview_configuration(main={"format": 'BGR888', "size": (320, 240)}))
picam.start()

window_name = 'Image'

# RGB Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def distance_detection():
    # Take 3 measurements rapidly
    for i in range(3):
        clock_check = time.perf_counter()
        distance = tbot.read_distance(timeout=25, samples=3)
        #print("Rapid:  Distance is {:.1f} cm (took {:.4f} sec)".format(distance, (time.perf_counter() - clock_check)))
        time.sleep(0.01)
    
    return distance
  
def circle_detection(image):  
    # Convert to grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1 = 30,  param2 = 80, minRadius = 0, maxRadius = 0)

    # Count and locate the circles that are detected.
    x=[] # list with x component of the circles detected
    y=[] # list with y component of the circles detected
    r=[] # list with the radius of the circles detected

    if detected_circles is not None:
        tbot.fill_underlighting(RED)
        num_circles=len(detected_circles[0,:,0])  

        # Convert the circle parameters x, y and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0,:]:
            x.append(pt[0])
            y.append(pt[1])
            r.append(pt[2])

            # paint cicle on image       
            image = cv2.circle(image, (pt[0], pt[1]), pt[2], GREEN, 5) 
    else:
        num_circles=0
        tbot.fill_underlighting(WHITE)
    return num_circles,x,y,r,image
        
while True or KeyboardInterrupt:
    distance=distance_detection()
    image = picam.capture_array()

    if distance < 50: #50cm threshold
        ball_detection = circle_detection(image)
        print("NUMBER OF BALLS:",ball_detection[0])
        image = ball_detection[4]
    else:
        print("NO BALLS DETECTED")
        tbot.fill_underlighting(WHITE)
    
    cv2.imshow(window_name, image)
    cv2.waitKey(1)