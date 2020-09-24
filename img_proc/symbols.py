import cv2 
import numpy as np
import os

class Symbols:
    """Class to detect and draw hazard symbols.
    """
    def __init__(self, level=10):
        """Symbol detector initialiser

        Args:
            level (int, optional): Trained cascade classifier level to use. Defaults to 10.
        """
        self.danger_classifier = cv2.CascadeClassifier(f'classifiers/dangerous-{level}.xml')
        self.corrosive_classifier = cv2.CascadeClassifier(f'classifiers/corrosive-{level}.xml')

    def __preprocess(self, frame):
        """Preprocess the raw frame to a frame to be used by the classifier

        Args:
            frame (np.ndarray): Camera frame

        Returns:
            np.ndarray: Camera frame, processed
        """
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grey = cv2.equalizeHist(grey)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower = np.array([30, 0, 0], dtype="uint8")
        # upper = np.array([90, 255, 255], dtype="uint8")
        # mask = cv2.inRange(hsv, lower, upper)
        # grey_masked = cv2.bitwise_and(grey, grey, mask=mask)

        return grey

    def find(self, frame):
        """Find hazard symbols in frame

        Args:
            frame (np.ndarray): Camera frame

        Returns:
            tuple: Containing:
                - danger_results (list): List of (x,y,w,h) integer tuple for each dangerous goods symbol spotted
                - corrosive_results (list): List of (x,y,w,h) integer tuple for each dangerous goods symbol spotted
        """
        grey = self.__preprocess(frame)

        # run cascade clasifer on image
        danger_results = self.danger_classifier.detectMultiScale(grey, 1.05, 3)
        corrosive_results = self.corrosive_classifier.detectMultiScale(grey)

        return (danger_results, corrosive_results)

    def draw(self, frame, dangerous, corrosive):
        """Draw the dangerous goods and corrosive symbol bounding boxes onto the frame

        Args:
            frame (np.ndarray): Camera frame
            dangerous (list): List of (x,y,w,h) tuples of dangerous goods symbols
            corrosive (list): List of (x,y,w,h) tuples of corrosive symbols
        """
        if dangerous is not None:
            for x,y,w,h in dangerous:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 255), 2)

        if corrosive is not None: 
            for x,y,w,h in corrosive:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 127, 255), 2)


if __name__ == '__main__':
    from gui import Gui
    from webcam import Webcam

    symbol_detector = Symbols()

    with Webcam() as cam, Gui() as gui: 
        while cam.running():
            frame = cam.get_frame()  
            
            dangerous, corrosive = symbol_detector.find(frame)
            symbol_detector.draw(frame, dangerous, corrosive)

            if not gui.imshow(frame): break

