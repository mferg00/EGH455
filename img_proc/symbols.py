import cv2 
import numpy as np
import os

class Symbols:

    def __init__(self):
        self.danger_classifier = cv2.CascadeClassifier('classifiers/dangerous-10.xml')
        self.corrosive_classifier = cv2.CascadeClassifier('classifiers/corrosive-10.xml')

    def find_symbols(self, frame):
        grey = self.preprocess(frame)

        # run cascade clasifer on image
        danger_results = self.danger_classifier.detectMultiScale(grey, 1.05, 3)
        corrosive_results = self.corrosive_classifier.detectMultiScale(grey)

        return (danger_results, corrosive_results)

    def preprocess(self, frame):
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grey = cv2.equalizeHist(grey)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([30, 0, 0], dtype="uint8")
        upper = np.array([90, 255, 255], dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        grey_masked = cv2.bitwise_and(grey, grey, mask=mask)

        return grey

    def draw_symbols(self, frame, dangerous, corrosive):
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
            frame = cam.read()  
            # frame = cv2.resize(frame, (100, 100))
            
            dangerous, corrosive = symbol_detector.find_symbols(frame)
            symbol_detector.draw_symbols(frame, dangerous, corrosive)

            if not gui.imshow(frame): break

