from typing import Iterator
from flask import Flask, render_template, request, jsonify, Response
import cv2
import time 

from camera import Camera
from symbols_ml import SymbolsMl
from aruco import Aruco

from sys import argv
DB_HOST_IP = '0.0.0.0' if len(argv) < 2 else argv[1]

app = Flask(__name__)

def yield_frames(cam: Camera, get_processed: bool = True) -> Iterator[str]:
    """Yield frames from camera for html usage.

    Args:
        cam (Camera): Camera object to get frames from.
        get_processed (bool, optional): Whether to get raw or processed frames. Defaults to True.

    Yields:
        Iterator[str]: A string to embed in html to play video.
    """
    try:
        cam.start()

        while cam.running() and cam.new_processed_frame_event.wait(10):
            frame = cam.get_frame(get_processed=get_processed)
                
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tostring() + b'\r\n')

    finally:
        cam.stop()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    processors = [
        SymbolsMl(), Aruco()
    ]
    cam = Camera(processors=processors, send_to_db=True)
    return Response(yield_frames(cam, get_processed=True), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return 'hi'

def run():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
	run()