import cv2
import numpy as np

FONT = cv2.FONT_HERSHEY_SIMPLEX

# use https://chev.me/arucogen/ for aruco markers and seeing what the aruco dicts are
class Aruco:
    """Class to detect and draw aruco markers.
    """
    def __init__(self, aruco_dict=cv2.aruco.DICT_4X4_1000):
        """Class initialiser, specify which aruco markers to detect

        Args:
            aruco_dict (dict, optional): The openCV aruco dictionary to detect aruco markers with. Defaults to cv2.aruco.DICT_4X4_1000.
        """
        self.dictionary = cv2.aruco.Dictionary_get(aruco_dict)
        self.parameters =  cv2.aruco.DetectorParameters_create()

        # https://docs.opencv.org/master/d5/dae/tutorial_aruco_detection.html
        self.parameters.minMarkerPerimeterRate = 0.1
        
    def find(self, frame: np.ndarray):
        """Find aruco markers in a frame.

        Args:
            frame (np.ndarray): Camera frame.

        Returns:
            tuple: Containing:
                - marker_corners (list): ...
                - marker_ids (list): ...
                - rejected_candidates (list): ...
        """
        marker_corners, marker_ids, rejected_candidates = cv2.aruco.detectMarkers(frame, self.dictionary, parameters=self.parameters)
        return marker_corners, marker_ids, rejected_candidates

    def draw(self, frame: np.ndarray, marker_corners: list, marker_ids: list):
        """Draw aruco markers onto frame.

        Args:
            frame (np.ndarray): Camera frame.
            marker_corners (list): List of marker corner coordinates.
            marker_ids (list): List of marker ids.
        """
        if marker_ids is not None: 
            for marker_corner, marker_id in zip(marker_corners, marker_ids):
                cv2.putText(frame, str(marker_ids[0]), 
                    tuple(marker_corner[0][0]), FONT, 
                    1, (255, 0, 0), 1, 
                    cv2.LINE_AA)

                corners = np.int32(marker_corner).reshape((-1, 1, 2))
                cv2.polylines(frame, [corners], True, (0, 0, 255), thickness=2)

if __name__ == '__main__':
    pass



 
