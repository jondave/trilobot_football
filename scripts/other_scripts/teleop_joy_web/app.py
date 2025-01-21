from flask import Flask, render_template, send_from_directory, Response
from flask_sock import Sock
import socket 
import cv2
from picamera2 import Picamera2
import numpy as np
import math

app = Flask(__name__)
sock = Sock(app)

import time
from trilobot import Trilobot

tbot = Trilobot()

enable_colour_detect = False
four_way_mapping = False
eight_way_mapping = True
motor_speed_mapping = False

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)})) # opencv works in BGR not RGB
picam2.start()

@app.route('/')
def index():
    hostname = (socket.gethostname().split(".")[0]).upper()
    return render_template('index.html', hostname=hostname)

@app.route("/manifest.json")
def manifest():
    return send_from_directory('./static', 'manifest.json')

@app.route("/app.js")
def script():
    return send_from_directory('./static', 'app.js')

@sock.route('/command')
def command(sock):
    
    speed = 0.5
    joy_x = 0
    joy_y = 0
    
    while True:
        # trilobot movement commands
        # tbot.forward(speed)
        # tbot.backward(speed)
        # tbot.turn_left(speed)
        # tbot.turn_right(speed)

        # tbot.set_left_speed(speed)
        # tbot.set_right_speed(speed)
        # tbot.set_motor_speeds(left_speed, right_speed)

        # tbot.curve_forward_right(speed)
        # tbot.curve_forward_left(speed)
        # tbot.curve_backward_right(speed)
        # tbot.curve_backward_left(speed)

        # tbot.stop() # stop quickly
        # tbot.coast()  # Come to a halt gently

        # joystick x,y directions
        # -y == up
        # +y == down
        # -x == left
        # +x == right

        cmd = sock.receive().split(':')

        if cmd[0] == "joy_x":
            joy_x = float(cmd[1])

        elif cmd[0] == "joy_y":
            joy_y = float(cmd[1])

        else: 
            print("movement command error")

        if four_way_mapping:
            if (joy_x == 0.0 and joy_y == 0.0):
                tbot.stop()

            elif (joy_y < 0 and abs(joy_y) > abs(joy_x)):
                speed = abs(joy_y)
                tbot.forward(speed)
            
            elif (joy_y > 0 and abs(joy_y) > abs(joy_x)):
                speed = abs(joy_y)
                tbot.backward(speed)
            
            elif (joy_x < 0 and abs(joy_x) > abs(joy_y)):
                speed = abs(joy_x)
                tbot.turn_left(speed)
            
            elif (joy_x > 0 and abs(joy_x) > abs(joy_y)):
                speed = abs(joy_x)
                tbot.turn_right(speed)
        
        if eight_way_mapping:
            # Determine the magnitude and direction of the joystick input
            speed = math.sqrt(joy_x ** 2 + joy_y ** 2)
            angle = math.atan2(joy_y, joy_x)

            # Check the direction based on angle and magnitude
            if (joy_x == 0.0 and joy_y == 0.0):
                tbot.stop()
            elif -math.pi / 8 <= angle < math.pi / 8:       
                tbot.turn_right(speed)
            elif math.pi / 8 <= angle < 3 * math.pi / 8:
                tbot.curve_backward_right(speed)
            elif 3 * math.pi / 8 <= angle < 5 * math.pi / 8:
                tbot.backward(speed)
            elif 5 * math.pi / 8 <= angle < 7 * math.pi / 8:
                tbot.curve_backward_left(speed)
            elif (7 * math.pi / 8 <= angle <= math.pi) or (-math.pi <= angle < -7 * math.pi / 8):
                tbot.turn_left(speed)
            elif -7 * math.pi / 8 <= angle < -5 * math.pi / 8:
                tbot.curve_forward_left(speed)
            elif -5 * math.pi / 8 <= angle < -3 * math.pi / 8:
                tbot.forward(speed)
            elif -3 * math.pi / 8 <= angle < -math.pi / 8:
                tbot.curve_forward_right(speed)

        if motor_speed_mapping:
            if (joy_x == 0.0 and joy_y == 0.0):
                tbot.stop()

            joy_x *= -1
            joy_y *= -1

            # Assuming joy_x and joy_y are in the range of -1 to 1
            max_joystick_value = 1.0

            # Map joy_x and joy_y to motor speeds
            left_speed = max_joystick_value * (joy_y + joy_x)
            right_speed = max_joystick_value * (joy_y - joy_x)

            left_speed = max(-1.0, min(1.0, left_speed))
            right_speed = max(-1.0, min(1.0, right_speed))

            tbot.set_motor_speeds(left_speed, right_speed)

def colour_detect(_img):
    hsv_img = cv2.cvtColor(_img, cv2.COLOR_BGR2HSV) # convert to hsv image

    # Create a binary (mask) image, HSV = hue (colour) (0-180), saturation  (0-255), value (brightness) (0-255)
    hsv_thresh = cv2.inRange(hsv_img,
                                np.array((50, 0, 0)), # lower range
                                np.array((80, 255, 255))) # upper range

    # Find the contours in the mask generated from the HSV image
    hsv_contours, hierachy = cv2.findContours(
        hsv_thresh.copy(),
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    
        
    # In hsv_contours we now have an array of individual closed contours (basically a polgon around the blobs in the mask). Let's iterate over all those found contours.
    for c in hsv_contours:
        # This allows to compute the area (in pixels) of a contour
        a = cv2.contourArea(c)
        # and if the area is big enough, we draw the outline
        # of the contour (in blue)
        if a > 100.0:
            cv2.drawContours(_img, c, -1, (255, 0, 0), 10)

    return _img

# From https://www.aranacorp.com/en/stream-video-from-a-raspberry-pi-to-a-web-browser/
def video_gen():
    """Video streaming generator function."""
    while True:
        img = picam2.capture_array()
        if enable_colour_detect:
            img = colour_detect(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert back to rgb image
        ret, jpeg = cv2.imencode('.jpg', img)
        frame=jpeg.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(video_gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port =5000, debug=False, threaded=True)
    tbot.stop()
    print("Trilobot stopped.")