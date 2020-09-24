import cv2
from threading import Thread

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    RPI = True 
except ImportError:
    RPI = False

import numpy as np
import time

from symbols import Symbols
from aruco import Aruco

class Camera():

    def __init__(self, do_processing=False, resolution=(320, 240), fps=32, pps=32, src=0, \
        prevent_picam=False):
        self.USE_PICAM = RPI and not prevent_picam and src == 0
        self.src = src
        self.frame = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
        self.processed_frame = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
        self.stopped = False
        self.fps = fps
        self.pps = pps
        self.prev_time = 0
        self.resolution = resolution
        self.aruco = Aruco()
        self.symbols = Symbols()
        self.do_processing = do_processing
        self.num_dangerous = 0
        self.num_corrosive = 0
        self.marker_ids = []

        if not self.USE_PICAM:
            print(f'recording with openCV from source: {src}')
            self.__init_opencv(src)
        else:
            print('recording with picam module')
            self.__init_picamera()

    def __enter__(self):
        self.start()
        return self 

    def __exit__(self, type, value, traceback):
        self.stop()

    def __init_picamera(self):
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.fps
        self.raw = PiRGBArray(self.camera, size=self.resolution)
        time.sleep(0.1)
        self.stream = self.camera.capture_continuous(self.raw,
            format="bgr", use_video_port=True)

    def __init_opencv(self, src):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.stream.set(cv2.CAP_PROP_FPS, self.fps)
        (_, self.frame) = self.stream.read()

    def __process(self):
        """Find the symbols and aruco markers in the frame. Used in a Thread.
        """
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            if self.pps is not None and time.time() - self.prev_time < 1. / self.pps:
                continue

            self.prev_time = time.time()

            # otherwise, read the next frame from the stream
            frame = self.get_frame()

            if frame is None:
                continue

            self.processed_frame = frame

            # find arucos in frame
            marker_corners, marker_ids, rejected_candidates = self.aruco.find(frame)

            # draw arucos on frame
            self.aruco.draw(self.processed_frame, marker_corners, marker_ids)
            
            # find symbols in frame
            dangerous, corrosive = self.symbols.find(frame)

            # draw symbols on frame
            self.symbols.draw(self.processed_frame, dangerous, corrosive)

            self.num_dangerous = 0 if dangerous is None else len(dangerous)
            self.num_corrosive = 0 if corrosive is None else len(corrosive)
            self.marker_ids = marker_ids

    def __update_picamera(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.raw.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.__cleanup()
                return

    def __update_opencv(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.__cleanup()
                return

            # otherwise, read the next frame from the stream
            (_, self.frame) = self.stream.read()

            time.sleep(1. / self.fps)

    def __cleanup(self):
        if self.USE_PICAM:
            print('picam closed')
            self.stream.close()
            self.raw.close()
            self.camera.close()
        else:
            print('opencv closed')
            self.stream.release()

    # public methods
    def running(self):
        """Check whether the camera is still retreiving frames.

        Returns:
            bool: True if camera is still running.
        """
        return not self.stopped

    def resolution(self):
        """Returns the resolution of the camera.

        Raises:
            NotImplementedError: Any child classes must override this method.
        """
        if self.USE_PICAM:
            return self.camera.resolution
        else:
            width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)

    def start(self):
        """Start the frame retrieval thread and the processing thread if specified by self.do_processing.
        """
        print('camera recording')

        if self.USE_PICAM:
            Thread(target=self.__update_picamera, args=()).start()
        else:
            Thread(target=self.__update_opencv, args=()).start()

        if self.do_processing: 
            Thread(target=self.__process, args=()).start()

    def get_frame(self, get_processed=False, get_bytestr=False):
        """Get the frame from the camera

        Args:
            get_processed (bool, optional): Retrieve the raw frame, or the processed frame with bounding boxes. Defaults to False.
            get_bytestr (bool, optional): Retrieve as a np.ndarray or as a string of bytes. Defaults to False.

        Returns:
            np.ndarray or str: The frame as retrieved by numpy, or a string of bytes.
        """
        frame = self.processed_frame if (get_processed and self.do_processing) else self.frame

        return frame if not get_bytestr else cv2.imencode('.jpg', frame)[1].tostring()

    def get_data(self):
        """Get the data found when processing the frame.

        Returns:
            tuple: Containing:
                - num_dangerous (int): Number of dangerous goods symbols detected.
                - num_corrosive (int): Number of corrosive symbols detected.
                - marker_ids (list): List of all marker ids detected.
        """
        return self.num_dangerous, self.num_corrosive, self.marker_ids

    def stop(self):
        """Stops the camera and processing thread.
        """
        self.stopped = True


def html_frame_gen():
    """Video streaming generator function."""
    with Camera(do_processing=True, src=0) as cam:
    # with Camera(do_processing=True, src="vids/output.avi") as cam:
        while cam.running():
            frame = cam.get_frame(get_processed=True, get_bytestr=True)
            num_dangerous, num_corrosive, marker_ids = cam.get_data()

            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    pass