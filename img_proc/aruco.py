from typing import Tuple, List
import cv2
import numpy as np

from camera import Processor

FONT = cv2.FONT_HERSHEY_SIMPLEX

class Aruco(Processor):
    """Class to detect and draw aruco markers.

    Args:
        Processor (Processor): Inherits from the Processor class
    """
    def __init__(self, 
        aruco_dict: dict = cv2.aruco.DICT_4X4_1000,
        parameters: dict = {}
    ):
        """Class initialiser, specify which aruco markers to detect

        Args:
            aruco_dict (dict, optional): The openCV aruco dictionary to detect aruco markers with. Defaults to cv2.aruco.DICT_4X4_1000.
            parameters (dict, optional): The class attributes of the openCV detector paramters object to change. Defaults to {}.
        """
        self.aruco_dict = aruco_dict
        self.dictionary = None
        self.parameters_dict = parameters
        self.parameters = None

    def load(self):
        """Load the aruco dictionary and parameters.
        """
        self.dictionary = cv2.aruco.Dictionary_get(self.aruco_dict)
        self.parameters =  cv2.aruco.DetectorParameters_create()

        for key, value in self.parameters_dict.items():
            setattr(self.parameters, key, value)

    def find(self, frame: np.ndarray) -> Tuple[list, list, list]:
        """Find aruco markers in a frame.

        Args:
            frame (np.ndarray): Camera frame.

        Returns:
            tuple: Containing 3 lists: marker_corners, marker_ids and rejected_candidates
        """
        marker_corners, marker_ids, rejected_candidates = cv2.aruco.detectMarkers(frame, self.dictionary, parameters=self.parameters)
        return marker_corners, marker_ids, rejected_candidates

    def parse_results(self, results: Tuple[list, list, list]) -> dict:
        """Parse the results from find().

        Args:
            results (Tuple[list, list, list]): The results from find().

        Returns:
            dict: A dict with 'aruco_ids' as the key and the marker ids as the value.
        """
        return {'aruco_ids': [] if results[1] is None else results[1].flatten().tolist()}

    def draw_results(self, frame: np.ndarray, results: Tuple[list, list, list]):
        marker_ids = results[1]
        marker_corners = results[0]

        if marker_ids is not None: 
            for marker_corner, marker_id in zip(marker_corners, marker_ids):
                cv2.putText(frame, str(marker_id), 
                    tuple(marker_corner[0][0]), FONT, 
                    0.5, (207, 0, 0), 1, 
                    cv2.LINE_AA)

                corners = np.int32(marker_corner).reshape((-1, 1, 2))
                cv2.polylines(frame, [corners], True, (207, 0, 0), thickness=2)


if __name__ == '__main__':
    """Parameter tweaking aruco detection
    """
    from camera import Camera
    from gui import Gui

    processors = [
        Aruco(parameters={
            'minMarkerPerimeterRate': 0.1,
            'polygonalApproxAccuracyRate': 0.15,
            'maxErroneousBitsInBorderRate': 0.05,
            'errorCorrectionRate': 0.6
        })
    ]
    src = 'ml/training/pi-targets.avi'

    with Camera(processors=processors, src=src) as cam, Gui() as gui:
        cam.start()
        while cam.running() and gui.running() and cam.new_processed_frame_event.wait(10):
            cam.fps = gui.bar('fps', tmin=1, tmax=64, default=64)

            ##### TWEAK PARAMETERS
            # more parameters found here (about 2/3 down page): https://docs.opencv.org/master/d5/dae/tutorial_aruco_detection.html
            cam.processors[0].parameters.adaptiveThreshWinSizeMin = gui.bar('thresh min size: ', tmin=3, tmax=15, default=3)
            cam.processors[0].parameters.adaptiveThreshWinSizeMax = gui.bar('thresh max size: ', tmin=15, tmax=30, default=23)
            cam.processors[0].parameters.adaptiveThreshWinSizeStep = gui.bar('thresh step size: ', tmin=3, tmax=30, default=10)
            cam.processors[0].parameters.minMarkerPerimeterRate = gui.bar('minMarkerPerimeterRate: 0.', tmin=1, tmax=1, default=1) / 10.
            cam.processors[0].parameters.polygonalApproxAccuracyRate = gui.bar('polygonalApproxAR: 0.', tmin=1, tmax=99, default=15) / 100.
            cam.processors[0].parameters.maxErroneousBitsInBorderRate = gui.bar('maxErroneuousBitsInBorder: 0.', tmin=1, default=5, tmax=99) / 100.
            cam.processors[0].parameters.errorCorrectionRate = gui.bar('errorCorrectionRate: 0.', tmin=1, tmax=9, default=6) / 10.
            #####

            frame = cam.get_frame(get_processed=True)
            print(cam.get_results())

            if gui.imshow(frame):
                cam.toggle_pause()



 
