import time
import cv2 
from pathlib import Path
import os

class Recorder:
    """Class to record videos frame by frame
    """
    def __init__(self, resolution: tuple, overwrite=True, \
        fps=20.0, time_limit=5):
        """Recorder initialiser.

        Args:
            resolution (tuple): Resolution of the camera in px (width, height).
            overwrite (bool, optional): Overwrite the file 'vids/output.avi', or create new ones. Defaults to True.
            time_limit (int, optional): Time limit for recording in seconds. Defaults to 5.
        """
        Path("vids/").mkdir(exist_ok=True)

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
        self.stop()

    def stop(self):
        """Stops the recorder.
        """
        print('writer released')
        self.out.release()
    
    def running(self):
        """Checks if the camera has exceeded the specified time limit.

        Returns:
            bool: True if time limit hasn't been exceeded.
        """
        return not time.time() >= self.time_limit

    def write(self, frame):
        """Writes the frame to the file

        Args:
            frame (np.ndarray): Camera frame to write
        """
        self.out.write(frame)
