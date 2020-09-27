import os 
import cv2
import numpy as np
import glob
from gui import Gui
from camera import Camera
import flask_camera_stream

try:
    import RPi.GPIO
    RPI = True 
except:
    RPI = False

def gui_camera(camera: Camera):
    try:
        camera.start()
        gui = Gui()

        while camera.running() and gui.running():
            # get frame from camera
            frame = camera.get_frame(get_processed=True)
            if gui.imshow(frame):
                camera.toggle_pause()

    finally:
        camera.stop()
        gui.cleanup()

def show_camera():
    if RPI:
        print('http://localhost:5000/video_feed/?do_processing=True')
        flask_camera_stream.run()

    else:
        gui_camera(Camera(do_processing=True))

def show_recorded(path="ml/training/pi-targets.avi"):
    if RPI:
        print(f'http://localhost:5000/video_feed/?do_processing=True&src={path}')
        flask_camera_stream.run()

    else:
        camera = Camera(do_processing=True, src=path, fps=30)
        gui_camera(camera)


def img_folder_to_video(input, output):
    
    img_array = []
    for filename in glob.glob(input):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)


    out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


if __name__ == '__main__':
    show_recorded()