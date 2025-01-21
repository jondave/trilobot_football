from flask import Flask, render_template, send_from_directory, Response
from flask_sock import Sock
import socket 
import cv2
from picamera2 import Picamera2
import numpy as np
import time
from trilobot import Trilobot

class TrilobotController:
    def __init__(self):
        self.app = Flask(__name__)
        self.sock = Sock(self.app)

        self.speed = 0.5
        self.tbot = Trilobot()

        self.enable_colour_detect = False
        self.hue_min = 0
        self.hue_max = 179
        self.saturation_min = 0
        self.saturation_max = 255
        self.intensity_min = 0
        self.intensity_max = 255

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)}))
        self.picam2.start()

        @self.app.route('/')
        def index():
            hostname = (socket.gethostname().split(".")[0]).upper()
            return render_template('index.html', hostname=hostname)

        @self.app.route("/manifest.json")
        def manifest():
            return send_from_directory('./static', 'manifest.json')

        @self.app.route("/app.js")
        def script():
            return send_from_directory('./static', 'app.js')

        @self.sock.route('/command')
        def command(sock):
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
                
                # Split the received command by ':' to get speed
                cmd = sock.receive().split(':')

                if cmd[0] == "left":
                    self.tbot.turn_left(self.speed)

                elif cmd[0] == "right":
                    self.tbot.turn_right(self.speed)

                elif cmd[0] == "up":
                    self.tbot.forward(self.speed)

                elif cmd[0] == "down":
                    self.tbot.backward(self.speed)

                elif cmd[0] == "stop":
                    self.tbot.stop()

                elif cmd[0] == "opencv":
                    self.enable_colour_detect = not self.enable_colour_detect

                elif cmd[0] == "speed":
                    self.speed = float(cmd[1])

                elif cmd[0] == "hue_min":
                    self.hue_min = int(cmd[1])

                elif cmd[0] == "hue_max":
                    self.hue_max = int(cmd[1])

                elif cmd[0] == "saturation_min":
                    self.saturation_min = int(cmd[1])

                elif cmd[0] == "saturation_max":
                    self.saturation_max = int(cmd[1])

                elif cmd[0] == "intensity_min":
                    self.intensity_min = int(cmd[1])

                elif cmd[0] == "intensity_max":
                    self.intensity_max = int(cmd[1])

                else: 
                    print("send either `up` `down` `left` `right` or `stop` to move your robot!")

        def colour_detect(self, _img):
            hsv_img = cv2.cvtColor(_img, cv2.COLOR_BGR2HSV) # convert to hsv image

            # Create a binary (mask) image, HSV = hue (colour) (0-179), saturation  (0-255), value (brightness) (0-255)
            #hsv_thresh = cv2.inRange(hsv_img,
            #                            np.array((50, 0, 0)), # lower range
            #                            np.array((80, 255, 255))) # upper range

            hsv_thresh = cv2.inRange(hsv_img,
                                        np.array((self.hue_min, self.saturation_min, self.intensity_min)), # lower range
                                        np.array((self.hue_max, self.saturation_max, self.intensity_max))) # upper range

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

        def video_gen(self):
            """Video streaming generator function."""
            while True:
                img = self.picam2.capture_array()

                if self.enable_colour_detect:
                    img = colour_detect(self, img)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                ret, jpeg = cv2.imencode('.jpg', img)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        @self.app.route('/video_feed')
        def video_feed():
            """Video streaming route. Put this in the src attribute of an img tag."""
            return Response(video_gen(self), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    controller = TrilobotController()
    controller.app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    controller.tbot.stop()
    print("Trilobot stopped.")
