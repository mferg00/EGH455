import cv2
from threading import Thread

class Camera:

    def __init__(self):
        self.frame: None
        self.stopped: bool
         
    def __enter__(self):
        return self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    def running(self):
        return not self.stopped
        
    def update(self):
        raise NotImplementedError

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

    def display(self, frame):
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF 

        if (cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1) \
            or (key == ord('q')): 
            self.stop()