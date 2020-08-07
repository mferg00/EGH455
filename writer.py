import time
import cv2 

class Writer:

    def __init__(self, resolution: tuple, overwrite=True, \
        fps=20.0, time_limit=5):
        if overwrite:
            filename = 'vids/output.avi'
        else:
            i = 0
            while os.path.exists("vids/output%s.avi" % i):
                i += 1
            filename = "vids/output%s.avi" % i

        self.out = cv2.VideoWriter(
            filename, 
            cv2.VideoWriter_fourcc(*'MJPG'),
            fps, 
            resolution)

        self.time_limit = time.time() + time_limit

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def cleanup(self):
        print('writer released')
        self.out.release()

    def write(self, frame):
        self.out.write(frame)
        return not time.time() >= self.time_limit
