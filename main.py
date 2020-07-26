from aruco import *
from webcam import Webcam
import cv2

if __name__ == '__main__':
    
    aruco = Aruco() 

    with Webcam() as cam:
        while cam.running():
            frame = cam.read()

            markerCorners, markerIds, rejectedCandidates = aruco.find(frame)
            aruco.draw(frame, markerCorners, markerIds)

            cam.display(frame)
