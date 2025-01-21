from flask import Flask, render_template, send_from_directory, Response
from flask_sock import Sock
import socket 
import cv2
from picamera2 import Picamera2
import numpy as np

app = Flask(__name__)
sock = Sock(app)

import time
from trilobot import Trilobot

tbot = Trilobot()

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
        cmd = sock.receive().split(':')

        if cmd[0] == "left":
            tbot.turn_left(speed)

        elif cmd[0] == "right":
            tbot.turn_right(speed)

        elif cmd[0] == "up":
            tbot.forward(speed)

        elif cmd[0] == "down":
            tbot.backward(speed)

        elif cmd[0] == "stop":
            tbot.stop()

        elif cmd[0] == "speed":
            speed = float(cmd[1])

        else: 
            print("send either `up` `down` `left` `right` or `stop` to move your robot!")

# From https://www.aranacorp.com/en/stream-video-from-a-raspberry-pi-to-a-web-browser/
def video_gen():
    """Video streaming generator function."""
    while True:
        img = picam2.capture_array()
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