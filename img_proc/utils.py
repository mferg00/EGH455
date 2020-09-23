import os 
import importlib
import cv2
from flask import Flask, render_template, request, jsonify, Response
import requests

from gui import Gui
try:
    importlib.util.find_spec("RPi.GPIO")
    RPI = True
    from picam import Picam as Cam 
except: 
    RPI = False
    from webcam import Webcam as Cam

def yield_frames(post_url=None):
    """Video streaming generator function."""
    with Cam() as cam:
        while cam.running():
            frame = cam.get_frame(get_processed=True, get_bytestr=True)
            num_dangerous, num_corrosive, marker_ids = cam.get_data()
            if post_url is not None:
                res = requests.post(post_url, json=
                    {'corrosive': num_corrosive, 
                    'dangerous_goods': num_dangerous, 
                    'aruco': marker_ids}
                )
                if not res.ok:
                    print(res.json())

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def run_gui():
    with Cam(do_processing=True) as cam, Gui() as gui:
        while cam.running():
            # get frame from camera
            frame = cam.get_frame(get_processsed=True)
            data = cam.get_data()
            if not gui.imshow(frame): break

if __name__ == '__main__':
    run_gui()
    
