from aruco import *
from symbol import *
from webcam import Webcam
import cv2

if __name__ == '__main__':
    
    aruco = Aruco() 
    symbol = Symbol('dangerous_goods.png')

    with Webcam() as cam:
        while cam.running():
            # get frame from camera
            frame = cam.read()

            # find things in frame
            markerCorners, markerIds, rejectedCandidates = aruco.find(frame)
            region = symbol.find(frame)

            # draw things on frame
            aruco.draw(frame, markerCorners, markerIds)
            symbol.draw(frame, region)

            # display frame
            cam.display(frame)
