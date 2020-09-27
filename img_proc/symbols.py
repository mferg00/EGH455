from typing import Tuple
import cv2 
import numpy as np
import os
import math

FONT = cv2.FONT_HERSHEY_SIMPLEX

def calculate_px_dim(resolution: Tuple[int, int]=(320, 240), fov: Tuple[float, float]=(62.2, 48.8), \
    height_m: float=2., target_dim_m: Tuple[float, float]=(0.2, 0.2)) -> Tuple[int, int]:
    viewing_field_w_m = 2. * (height_m * math.tan(math.radians(fov[0] / 2.)))
    viewing_field_h_m = 2. * (height_m * math.tan(math.radians(fov[1] / 2.)))
    viewing_field_m = (viewing_field_w_m, viewing_field_h_m)

    pixel_dim_m = (viewing_field_m[0] / resolution[0], viewing_field_m[1] / resolution[1])

    target_dim_px = tuple(map(lambda x, y: int(x / y), target_dim_m, pixel_dim_m))

    return target_dim_px

class Symbols:
    """Class to detect and draw hazard symbols.
    """
    def __init__(self, 
        level: int = 10, 
        classifier_path: str = "cascade",
        scale_factor: float = 1.05,
        min_neighbours: int = 4,
        recording_height_m: float = 2,
        bound_tolerance_px: int = 20,
        flags = cv2.CASCADE_DO_ROUGH_SEARCH
    ):
        """Symbol detector initialiser

        Args:
            level (int, optional): Trained cascade classifier level to use. Defaults to 10.
        """
        self.level = level
        self.danger_classifier = cv2.CascadeClassifier(f'{classifier_path}/dangerous-{level}.xml')
        self.corrosive_classifier = cv2.CascadeClassifier(f'{classifier_path}/corrosive-{level}.xml')

        w_px, h_px = calculate_px_dim(height_m=recording_height_m)

        self.detectorKwargs = {
            'minNeighbours': min_neighbours,
            'scaleFactor': scale_factor,
            'minSize': (max(w_px - bound_tolerance_px, 0), max(h_px - bound_tolerance_px, 0)),
            'maxSize': (w_px + bound_tolerance_px, h_px + bound_tolerance_px),
            'flags': flags
        }
    
    def __preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Preprocess the raw frame to a frame to be used by the classifier

        Args:
            frame (np.ndarray): Camera frame

        Returns:
            np.ndarray: Camera frame, processed
        """
        return None


    def _find(self, frame: np.ndarray, **kwargs) -> Tuple[list, list]:
        """Find hazard symbols in frame

        Args:
            frame (np.ndarray): Camera frame

        Returns:
            tuple: Containing:
                - danger_results (list): List of (x,y,w,h) integer tuple for each dangerous goods symbol spotted
                - corrosive_results (list): List of (x,y,w,h) integer tuple for each dangerous goods symbol spotted
        """
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # run cascade clasifer on image
        danger_results = self.danger_classifier.detectMultiScale(grey, **kwargs)
        corrosive_results = self.corrosive_classifier.detectMultiScale(grey, **kwargs)

        return (danger_results, corrosive_results)

    def find(self, frame: np.ndarray) -> Tuple[list, list]:
        return self._find(frame, **self.detectorKwargs)

    def draw(self, frame: np.ndarray, dangerous: list, corrosive: list) -> np.ndarray:
        """Draw the dangerous goods and corrosive symbol bounding boxes onto the frame

        Args:
            frame (np.ndarray): Camera frame
            dangerous (list): List of (x,y,w,h) tuples of dangerous goods symbols
            corrosive (list): List of (x,y,w,h) tuples of corrosive symbols
        """
        def do_draw(name: str, points: list, colour: tuple):
            for x,y,w,h in points:
                cv2.rectangle(frame, (x,y), (x+w, y+h), colour, thickness=2)
                cv2.putText(frame, name, 
                    (x, y), FONT, 
                    0.5, colour, 1, 
                    cv2.LINE_AA)

        if dangerous is not None:
            do_draw('dgrs', dangerous, (207, 138, 0))
        
        if corrosive is not None:
            do_draw('crsv', corrosive, (0, 207, 0))

        return frame

if __name__ == '__main__':
    from camera import Camera
    from gui import Gui
    symbols = Symbols(level=10, path="cascade")

    src = "ml/training/pi-targets.avi"

    with Camera(src=0, fps=32) as cam, Gui('press p to pause') as gui:

        gui.add_bar('scale factor: 1.', min=1, default=5, max=99)
        gui.add_bar('min neighbours: ', min=1, default=4, max=100)
        gui.add_bar('recording height (cm): ', min=1, default=160, max=1000)
        gui.add_bar('detection bounds (px): ', min=1, default=30, max=200)

        while cam.running() and gui.running():
            w_px, h_px = calculate_px_dim(height_m=(gui.get_bar('recording height (cm): ') / 100))
            frame = cam.get_frame().copy()
            bounds = gui.get_bar('detection bounds (px): ')

            dangerous, corrosive = symbols._find(
                frame,
                scaleFactor=1. + (gui.get_bar('scale factor: 1.') / 100),
                minNeighbours=gui.get_bar('min neighbours: '),
                minSize=(max(w_px - bounds, 0), max(h_px - bounds, 0)),
                maxSize=(min(w_px + bounds, cam.resolution[0]), min(h_px + bounds, cam.resolution[1])),
                flags=cv2.CASCADE_DO_ROUGH_SEARCH
            )

            ld = len(dangerous)
            lc = len(corrosive)

            if ld or lc:
                # print(ld, lc)
                pass

            symbols.draw(frame, dangerous, corrosive)
            
            if gui.imshow(frame):
                cam.toggle_pause()





