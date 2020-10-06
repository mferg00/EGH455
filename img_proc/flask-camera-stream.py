"""Minimal flask application."""
import os
from flask import Flask, render_template, request, jsonify, Response
# emulated camera
# from webcam import Webcam as Cam
from picam import Picam as Cam
import cv2
# Initialize Flask web app
app = Flask(__name__)

def gen():
    """Video streaming generator function."""
    with Cam() as cam:
        while cam.running():
            frame = cam.read_as_bytestr()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return 'hello world'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)