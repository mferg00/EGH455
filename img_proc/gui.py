import cv2
import numpy as np

def void(a):
    pass 

class Gui:
    """Simple class to access openCV gui
    """
    def __init__(self, title: str="frame"):
        self.stopped = False
        self.title = title
        self.mins = {}
        cv2.namedWindow(self.title)

    def __enter__(self):
        return self 

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def running(self) -> bool:
        return not self.stopped

    def cleanup(self):
        print('cv2 windows closed')
        cv2.destroyAllWindows()

    def add_bar(self, label: str, min: int=1, default: int=1, max: int=100):
        cv2.createTrackbar(label, self.title, default, max, void)
        self.mins[label] = min

    def get_bar(self, label: str) -> int:
        return max(cv2.getTrackbarPos(label, self.title), self.mins[label])

    def imshow(self, frame: np.ndarray) -> bool:
        if type(frame) is list:
            new_frame = np.hstack(frame)
        else:
            new_frame = frame

        cv2.imshow(self.title, new_frame)
        key = cv2.waitKey(1) & 0xFF

        self.stopped = \
            ((cv2.getWindowProperty(self.title, cv2.WND_PROP_VISIBLE) < 1) \
            or (key == ord('q')))

        return key == ord('p')