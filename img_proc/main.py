from aruco import *
from webcam import Webcam as Cam
# from picam import Picam as Cam
from recorder import Recorder
from gui import Gui
from symbols import Symbols
import cv2

def pi():
    aruco = Aruco(aruco_dict=cv2.aruco.DICT_6X6_250) 
    symbols = Symbols()

    with Cam() as cam, Recorder(cam.resolution()) as recorder:
        while cam.running() and recorder.running():
            # get frame from camera
            frame = cam.read()

            # find arucos in frame
            markerCorners, markerIds, rejectedCandidates = aruco.find(frame)

            # draw arucos on frame
            aruco.draw(frame, markerCorners, markerIds)

            # find symbols in frame
            dangerous, corrosive = symbols.find_symbols(frame)

            # draw symbols on frame
            symbols.draw_symbols(frame, dangerous, corrosive)

            # save frame to file
            recorder.write(frame)

def test():
    aruco = Aruco(aruco_dict=cv2.aruco.DICT_6X6_250) 
    symbols = Symbols()
    gui = Gui()

    with Cam() as cam:
        while cam.running():
            # get frame from camera
            frame = cam.read()

            # find arucos in frame
            markerCorners, markerIds, rejectedCandidates = aruco.find(frame)

            # draw arucos on frame
            aruco.draw(frame, markerCorners, markerIds)

            # find symbols in frame
            dangerous, corrosive = symbols.find_symbols(frame)

            # draw symbols on frame
            symbols.draw_symbols(frame, dangerous, corrosive)

            # show in gui 
            if not gui.imshow(frame): break

if __name__ == '__main__':
    
    test()
