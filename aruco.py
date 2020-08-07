import cv2
import numpy as np

FONT = cv2.FONT_HERSHEY_SIMPLEX

# use https://chev.me/arucogen/ for aruco markers and seeing what the aruco dicts are
class Aruco:

    def __init__(self, aruco_dict=cv2.aruco.DICT_6X6_250):
        self.dictionary = cv2.aruco.Dictionary_get(aruco_dict)
        self.parameters =  cv2.aruco.DetectorParameters_create()

    def find(self, frame):
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, self.dictionary, parameters=self.parameters)

        return markerCorners, markerIds, rejectedCandidates

    def draw(self, frame, markerCorners, markerIds):
        if markerIds is not None: 
                for markerCorner, markerId in zip(markerCorners, markerIds):
                    cv2.putText(frame, str(markerId[0]), 
                        tuple(markerCorner[0][0]), FONT, 
                        1, (255, 0, 0), 1, 
                        cv2.LINE_AA)

                    corners = np.int32(markerCorner).reshape((-1, 1, 2))
                    cv2.polylines(frame, [corners], True, 
                        (0, 0, 255), thickness=2)
 
