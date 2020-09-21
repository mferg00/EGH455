
from time import time
import os

class Camera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    


    def __init__(self):
        self.frames = []
        for f in os.listdir(os.getcwd() + '/classifiers/training/corrosive/pos/'):
            process_f = os.getcwd() + '/classifiers/training/corrosive/pos/' + f
            self.frames.append(open(process_f,'rb').read())
        # self.frames = [open(os.getcwd() + '/classifiers/training/corrosive/pos/' + f, 'rb').read() for f in os.listdir(os.getcwd() + '/classifiers/training/corrosive/pos/')]

    def get_frame(self):
        return self.frames[int(time()) % 30]

if __name__ == '__main__':
    cam = Camera()
    print(type(cam.frames[0]), cam.frames[0])
