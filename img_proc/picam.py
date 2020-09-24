from picamera.array import PiRGBArray
from picamera import PiCamera
from camera import Camera
import numpy as np
import time

class Picam(Camera):
    """Class to access the Picamera.

    Args:
        Camera (Object): Camera class to inherit from.
    """
    def __init__(self, do_processing=False, resolution=(320, 240), fps=32):
        """Initialise the Pi Camera.

        Args:
            resolution (tuple, optional): Resolution to record in. Defaults to (320, 240).
            fps (int, optional): fps to record in. Defaults to 32.
        """
        super().__init__(do_processing)
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.fps = fps
        self.raw = PiRGBArray(self.camera, size=resolution)
        time.sleep(0.1)
        self.stream = self.camera.capture_continuous(self.raw,
            format="bgr", use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
        self.stopped = False

    def _update(self):
        """Parent method override, stores frames in self.frame.
        """
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.raw.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self._cleanup()
                return

    def _cleanup(self):
        """Parent method override, closes camera streams.
        """
        print('picam closed')
        self.stream.close()
        self.raw.close()
        self.camera.close()

    def resolution(self):
        """Get resolution of the Pi Camera

        Returns:
            tuple: Containing:
                - width (int): width of camera (px)
                - height (int): height of camera (px)
        """
        return self.camera.resolution
              
if __name__ == '__main__':
    
    from recorder import Recorder

    with Picam(do_processing=True) as cam, Recorder(cam.resolution()) as recorder:
        while (cam.running() and recorder.running()):
            frame = cam.get_frame(get_processed=True)
            recorder.write(frame)
        
