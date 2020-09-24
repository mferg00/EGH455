import os 
import cv2

def run_gui():
    try:
        import RPi.GPIO
        import flask_camera_stream
        flask_camera_stream.run()

    except ImportError:
        from gui import show_camera
        show_camera()

def prerecorded():
    pass

if __name__ == '__main__':
    run_gui()