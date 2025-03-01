from flask import Flask, render_template, send_from_directory, Response, jsonify
from flask_sock import Sock
import socket 
import cv2
from picamera2 import Picamera2
from libcamera import Transform
import numpy as np
import time
from trilobot import Trilobot
import atexit

class TrilobotController:
    def __init__(self):
        self.app = Flask(__name__)
        self.sock = Sock(self.app)

        atexit.register(self.cleanup) # Clean up when exiting

        ################# tunable variables       

        ####### follow ball function
        # Define a threshold for how far the centre of contour around the ball can be from the center before adjusting the motors
        self.threshold = 100
        
        # Calculate speed adjustments based on the offset
        self.speed_factor = 0.005  # You can adjust this factor for more sensitivity
        self.max_speed = 0.5  # Set the max speed of the follow ball function
        ####### follow ball function

        ################# tunable variables

        self.speed = 0.5 # starting speed
        self.tbot = Trilobot()

        self.enable_colour_detect = False # starting flag 
        self.enable_colour_detect_goal = False # starting flag
        self.enable_follow_ball = False # starting flag
        self.enable_follow_goal = False # starting flag
        self.enable_custom_code = False # starting flag

        # Ball detection colour ranges
        self.hue_min = 0 # starting hue min 
        self.hue_max = 179 # starting hue  max
        self.saturation_min = 0 # starting saturation min
        self.saturation_max = 255 # starting saturation max
        self.intensity_min = 0 # starting intensity min
        self.intensity_max = 255 # starting intensity max

        # Goal detection colour ranges
        self.hue_min_goal = 0 # starting hue min 
        self.hue_max_goal = 179 # starting hue  max
        self.saturation_min_goal = 0 # starting saturation min
        self.saturation_max_goal = 255 # starting saturation max
        self.intensity_min_goal = 0 # starting intensity min
        self.intensity_max_goal = 255 # starting intensity max

        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'BGR888', "size": (1640, 1232)}))
        # self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)}))
        self.picam2.start()
        
        # Camera resolutions
        # 0x2464-SBGGR8_1X8 - Selected unicam format: 3280x2464-BA81
        # [
        # {'format': SRGGB10_CSI2P, 'unpacked': 'SRGGB10', 'bit_depth': 10, 'size': (640, 480), 'fps': 103.33, 'crop_limits': (1000, 752, 1280, 960), 'exposure_limits': (75, None)},
        # {'format': SRGGB10_CSI2P, 'unpacked': 'SRGGB10', 'bit_depth': 10, 'size': (1640, 1232), 'fps': 41.85, 'crop_limits': (0, 0, 3280, 2464), 'exposure_limits': (75, 11766829, None)}, 
        # {'format': SRGGB10_CSI2P, 'unpacked': 'SRGGB10', 'bit_depth': 10, 'size': (1920, 1080), 'fps': 47.57, 'crop_limits': (680, 692, 1920, 1080), 'exposure_limits': (75, 11766829, None)}, 
        # {'format': SRGGB10_CSI2P, 'unpacked': 'SRGGB10', 'bit_depth': 10, 'size': (3280, 2464), 'fps': 21.19, 'crop_limits': (0, 0, 3280, 2464), 'exposure_limits': (75, 11766829, None)}, 
        # {'format': SRGGB8, 'unpacked': 'SRGGB8', 'bit_depth': 8, 'size': (640, 480), 'fps': 103.33, 'crop_limits': (1000, 752, 1280, 960), 'exposure_limits': (75, 11766829, None)}, 
        # {'format': SRGGB8, 'unpacked': 'SRGGB8', 'bit_depth': 8, 'size': (1640, 1232), 'fps': 41.85, 'crop_limits': (0, 0, 3280, 2464), 'exposure_limits': (75, 11766829, None)}, 
        # {'format': SRGGB8, 'unpacked': 'SRGGB8', 'bit_depth': 8, 'size': (1920, 1080), 'fps': 47.57, 'crop_limits': (680, 692, 1920, 1080), 'exposure_limits': (75, 11766829, None)}, 
        # {'format': SRGGB8, 'unpacked': 'SRGGB8', 'bit_depth': 8, 'size': (3280, 2464), 'fps': 21.19, 'crop_limits': (0, 0, 3280, 2464), 'exposure_limits': (75, 11766829, None)}
        # ]

        @self.app.route('/')
        def index():
            hostname = (socket.gethostname().split(".")[0]).upper()
            return render_template('index.html', hostname=hostname)

        @self.app.route('/xbox')
        def xbox():
            hostname = (socket.gethostname().split(".")[0]).upper()
            return render_template('xbox.html', hostname=hostname)

        @self.app.route("/manifest.json")
        def manifest():
            return send_from_directory('./static', 'manifest.json')

        @self.app.route("/app.js")
        def script():
            return send_from_directory('./static', 'app.js')

        @self.sock.route('/command')
        def command(sock):
            try:
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
                        self.enable_follow_ball = False
                        self.enable_follow_goal = False

                    elif cmd[0] == "opencv":
                        self.enable_colour_detect = not self.enable_colour_detect

                    elif cmd[0] == "follow_ball":
                        self.enable_colour_detect = not self.enable_colour_detect
                        self.enable_follow_ball = not self.enable_follow_ball
                        self.enable_follow_goal = False

                    elif cmd[0] == "opencv_goal":
                        self.enable_colour_detect_goal = not self.enable_colour_detect_goal

                    elif cmd[0] == "follow_goal":
                        self.enable_colour_detect_goal = not self.enable_colour_detect_goal
                        self.enable_follow_goal = not self.enable_follow_goal
                        self.enable_follow_ball = False

                    elif cmd[0] == "custom_code":
                        self.enable_custom_code = not self.enable_custom_code

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

                    elif cmd[0] == "speed":
                        self.speed = float(cmd[1])

                    elif cmd[0] == "hue_min_goal":
                        self.hue_min_goal = int(cmd[1])

                    elif cmd[0] == "hue_max_goal":
                        self.hue_max_goal = int(cmd[1])

                    elif cmd[0] == "saturation_min_goal":
                        self.saturation_min_goal = int(cmd[1])

                    elif cmd[0] == "saturation_max_goal":
                        self.saturation_max_goal = int(cmd[1])

                    elif cmd[0] == "intensity_min_goal":
                        self.intensity_min_goal = int(cmd[1])

                    elif cmd[0] == "intensity_max_goal":
                        self.intensity_max_goal = int(cmd[1])

                    else: 
                        print("send either `up` `down` `left` `right` or `stop` to move your robot!")

            except Exception as e:
                # Stop the robot if there's an error or disconnection
                print(f"Error or disconnection: {e}")
                self.tbot.stop()

        @self.app.route('/get_ultrasonic_data', methods=['GET'])
        def get_ultrasonic_data():
            distance = self.tbot.read_distance(timeout=25, samples=3)
            print("distance: " + str(distance))
            return jsonify({'distance': round(distance, 1)})

        def colour_detect(self, _img):
            hsv_img = cv2.cvtColor(_img, cv2.COLOR_BGR2HSV) # convert to hsv image

            # Draw and fill all the contours of the ball detection
            hsv_thresh = cv2.inRange(hsv_img,
                                        np.array((self.hue_min, self.saturation_min, self.intensity_min)), # lower range
                                        np.array((self.hue_max, self.saturation_max, self.intensity_max))) # upper range

            # Find the contours in the mask generated from the HSV image
            hsv_contours, hierachy = cv2.findContours(
                hsv_thresh.copy(),
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

            # Check if any contours are found
            if not hsv_contours:
                # If no contours are found, return the original image and None for the largest contour
                return _img, None
                
            # Find the largest contour using max() and cv2.contourArea as the key
            largest_contour = max(hsv_contours, key=cv2.contourArea)                
        
            # Create an overlay to draw the contours on
            overlay = _img.copy()

            # Iterate through the contours
            for c in hsv_contours:
                # Calculate the area of the contour
                a = cv2.contourArea(c)
                # If the area is big enough, fill the contour on the overlay
                if a > 100.0:
                    cv2.drawContours(overlay, [c], -1, (0, 255, 0), cv2.FILLED)  # Draw filled contour on overlay
                    cv2.drawContours(_img, [c], -1, (255, 255, 255), 2)  # Draw outline of contours

            # Set the desired opacity (0.0 to 1.0)
            opacity = 0.5

            # Blend the overlay with the original image
            _img = cv2.addWeighted(overlay, opacity, _img, 1 - opacity, 0)

            return _img, largest_contour

        def colour_detect_goal(self, _img):
            hsv_img = cv2.cvtColor(_img, cv2.COLOR_BGR2HSV) # convert to hsv image            
                
            # Draw and fill all the contours of the goal detection
            hsv_thresh = cv2.inRange(hsv_img,
                                        np.array((self.hue_min_goal, self.saturation_min_goal, self.intensity_min_goal)), # lower range
                                        np.array((self.hue_max_goal, self.saturation_max_goal, self.intensity_max_goal))) # upper range

            # Find the contours in the mask generated from the HSV image
            hsv_contours, hierachy = cv2.findContours(
                hsv_thresh.copy(),
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

            # Check if any contours are found
            if not hsv_contours:
                # If no contours are found, return the original image and None for the largest contour
                return _img, None
                
            # Find the largest contour using max() and cv2.contourArea as the key
            largest_contour = max(hsv_contours, key=cv2.contourArea)   

            # Create an overlay to draw the contours on
            overlay = _img.copy()

            # Iterate through the contours
            for c in hsv_contours:
                # Calculate the area of the contour
                a = cv2.contourArea(c)
                # If the area is big enough, fill the contour on the overlay
                if a > 100.0:
                    cv2.drawContours(overlay, [c], -1, (255, 0, 0), cv2.FILLED)  # Draw filled contour on overlay
                    cv2.drawContours(_img, [c], -1, (255, 255, 255), 2)  # Draw outline of contours

            # Set the desired opacity (0.0 to 1.0)
            opacity = 0.5

            # Blend the overlay with the original image
            _img = cv2.addWeighted(overlay, opacity, _img, 1 - opacity, 0)

            return _img, largest_contour

        def follow_ball(self, _img, largest_contour):
            # Get the bounding box around the largest contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Calculate the horizontal middle (center) of the bounding box
            bounding_box_center = x + w // 2

            # Get the center of the image
            image_center = _img.shape[1] // 2  # Width of the image

            # Calculate the offset between the contour's center and the image center
            offset = bounding_box_center - image_center

            # Proportional control: If the offset is larger than the threshold, adjust the robot's speed
            if abs(offset) > self.threshold:
                if bounding_box_center > image_center:
                    # If the contour is to the right of the center, turn right
                    left_speed = self.speed + (abs(offset) * self.speed_factor)
                    right_speed = self.speed - (abs(offset) * self.speed_factor)
                else:
                    # If the contour is to the left of the center, turn left
                    left_speed = self.speed - (abs(offset) * self.speed_factor)
                    right_speed = self.speed + (abs(offset) * self.speed_factor)
                
                # Clamp the speeds to be within the range [0, max_speed]
                left_speed = max(0, min(self.max_speed, left_speed))
                right_speed = max(0, min(self.max_speed, right_speed))
                
                # Set the motor speeds to move the robot
                self.tbot.set_motor_speeds(round(left_speed, 1), round(right_speed, 1))
                print("left_speed:", left_speed, "right_speed:", right_speed, end="\r")
            else:
                # If the contour is close to the center, move forward
                self.tbot.set_motor_speeds(self.speed, self.speed)
                print("forward speed: ", self.speed)

            # Optionally, draw the bounding box and the middle point
            cv2.rectangle(_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(_img, (bounding_box_center, y + h // 2), 5, (0, 255, 0), -1)

            return _img

        def follow_goal(self, _img, largest_contour):
            # Get the bounding box around the largest contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Calculate the horizontal middle (center) of the bounding box
            bounding_box_center = x + w // 2

            # Get the center of the image
            image_center = _img.shape[1] // 2  # Width of the image

            # Calculate the offset between the contour's center and the image center
            offset = bounding_box_center - image_center

            # Proportional control: If the offset is larger than the threshold, adjust the robot's speed
            if abs(offset) > self.threshold:
                if bounding_box_center > image_center:
                    # If the contour is to the right of the center, turn right
                    left_speed = self.speed + (abs(offset) * self.speed_factor)
                    right_speed = self.speed - (abs(offset) * self.speed_factor)
                else:
                    # If the contour is to the left of the center, turn left
                    left_speed = self.speed - (abs(offset) * self.speed_factor)
                    right_speed = self.speed + (abs(offset) * self.speed_factor)
                
                # Clamp the speeds to be within the range [0, max_speed]
                left_speed = max(0, min(self.max_speed, left_speed))
                right_speed = max(0, min(self.max_speed, right_speed))
                
                # Set the motor speeds to move the robot
                self.tbot.set_motor_speeds(round(left_speed, 1), round(right_speed, 1))
                print("left_speed:", left_speed, "right_speed:", right_speed, end="\r")
            else:
                # If the contour is close to the center, move forward
                self.tbot.set_motor_speeds(self.speed, self.speed)
                print("forward speed: ", self.speed)

            # Optionally, draw the bounding box and the middle point
            cv2.rectangle(_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(_img, (bounding_box_center, y + h // 2), 5, (255, 0, 0), -1)

            return _img

        def custom_code(self):
            ##### Add custom code in the function, when the custom code button is pressed this function will run
            print("custom_code running")

            ##### example code to read ultrasonic sensor
            distance = self.tbot.read_distance(timeout=25, samples=3)
            print("distance: " + str(distance))

        def video_gen(self):
            """Video streaming generator function."""
            while True:
                img = self.picam2.capture_array()

                img = cv2.resize(img, (640, 480))

                if self.enable_colour_detect:
                    img, largest_contour = colour_detect(self, img)

                if self.enable_colour_detect_goal:
                    img, largest_contour_goal = colour_detect_goal(self, img)

                if self.enable_follow_ball and largest_contour is not None:
                    img = follow_ball(self, img, largest_contour)                

                if self.enable_follow_goal and largest_contour_goal is not None:
                    img = follow_goal(self, img, largest_contour_goal)                

                if self.enable_custom_code:
                    custom_code(self)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                ret, jpeg = cv2.imencode('.jpg', img)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        @self.app.route('/video_feed')
        def video_feed():
            """Video streaming route. Put this in the src attribute of an img tag."""
            return Response(video_gen(self), mimetype='multipart/x-mixed-replace; boundary=frame')

    def cleanup(self):
        """This function will be called when the program exits."""
        print("Cleaning up before exit...")
        self.tbot.stop()

if __name__ == "__main__":
    controller = TrilobotController()
    controller.app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    controller.tbot.stop()
    print("Trilobot stopped.")
