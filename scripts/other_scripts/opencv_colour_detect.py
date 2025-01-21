#!/usr/bin/python3

import cv2
from picamera2 import Picamera2
import numpy as np

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)})) # opencv works in BGR not RGB
picam2.start()

while True:
    img = picam2.capture_array()

    # using the BGR colour space, create a mask for everything that is in a certain range
    bgr_thresh = cv2.inRange(img,
                                np.array((130, 130, 0)), # lower range
                                np.array((170, 170, 40))) # upper range

    # It often is better to use another colour space, that is less sensitive to illumination (brightness) changes.
    # The HSV colour space is often a good choice. 
    # So, we first change the colour space here.
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a binary (mask) image, HSV = hue (colour) (0-180), saturation  (0-255), value (brightness) (0-255)
    hsv_thresh = cv2.inRange(hsv_img,
                                np.array((100, 100, 0)), # lower range
                                np.array((150, 255, 255))) # upper range

    # just for the fun of it, print the mean value of each HSV channel within the mask 
    # print(cv2.mean(hsv_img[:, :, 0], mask = hsv_thresh)[0])
    # print(cv2.mean(hsv_img[:, :, 1], mask = hsv_thresh)[0])
    # print(cv2.mean(hsv_img[:, :, 2], mask = hsv_thresh)[0])

    # This is how we could find actual contours in
    # the BGR image, but we won't do this now.
    # _, bgr_contours, hierachy = cv2.findContours(
    #     bgr_thresh.copy(),
    #     cv2.RETR_TREE,
    #     cv2.CHAIN_APPROX_SIMPLE)

    # Instead find the contours in the mask generated from the HSV image.
    hsv_contours, hierachy = cv2.findContours(
        hsv_thresh.copy(),
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    
    # in hsv_contours we now have an array of individual closed contours (basically a polgon around the blobs in the mask). Let's iterate over all those found contours.
    for c in hsv_contours:
        # This allows to compute the area (in pixels) of a contour
        a = cv2.contourArea(c)
        # and if the area is big enough, we draw the outline
        # of the contour (in blue)
        if a > 100.0:
            cv2.drawContours(img, c, -1, (255, 0, 0), 10)
    #print('====')

    #img_small = cv2.resize(img, (0,0), fx=0.4, fy=0.4) # reduce image size
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert back to rgb image
    cv2.imshow("Image window", img)
    cv2.waitKey(1)