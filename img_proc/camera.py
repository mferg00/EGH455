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

    def resolution(self):
        raise NotImplementedError

    def start(self):
        print('camera recording')
        Thread(target=self.update, args=()).start()
        return self

    def read(self):
        return self.frame

    def read_as_bytestr(self):
        return cv2.imencode('.jpg', self.frame)[1].tostring()

    def stop(self):
        self.stopped = True

    def cleanup(self):
        raise NotImplementedError


