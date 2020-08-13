from aruco import *
from webcam import Webcam as Cam
# from picam import Picam as Cam
from recorder import Recorder
import cv2

if __name__ == '__main__':
    
    aruco = Aruco(aruco_dict=cv2.aruco.DICT_6X6_250) 

    with Cam() as cam, Recorder(cam.resolution()) as recorder:
        while cam.running() and recorder.running():
            # get frame from camera
            frame = cam.read()

            # find things in frame
            markerCorners, markerIds, rejectedCandidates = aruco.find(frame)

            # draw things on frame
            aruco.draw(frame, markerCorners, markerIds)

            # save frame to file
            recorder.write(frame)
