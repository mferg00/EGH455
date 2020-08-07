from picamera.array import PiRGBArray
from picamera import PiCamera
from camera import Camera
import numpy as np
import time

class Picam(Camera):

    def __init__(self, resolution=(320, 240), framerate=32):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.raw = PiRGBArray(self.camera, size=resolution)
        time.sleep(0.1)
        self.stream = self.camera.capture_continuous(self.raw,
            format="bgr", use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
        self.stopped = False

    def cleanup(self):
        self.stream.close()
        self.raw.close()
        self.camera.close()

    def resolution(self):
        return self.camera.resolution

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.raw.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                return
              
                
if __name__ == '__main__':
    
    from writer import Writer 

    with Picam() as cam, Writer() as writer:
        while(cam.running()):
            frame = cam.read()
            if not writer.write(frame): break
        
