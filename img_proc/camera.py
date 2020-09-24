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

class Camera:
    """Base camera class for other classes to inherit from and provide hardware-specific method overrides. 

    Raises:
        NotImplementedError: If any class inheriters don't override certain methods.

    Returns:
        Object: Camera object.
    """
    # private methods
    def __init__(self, do_processing):
        """Initialise base camera class

        Args:
            do_processing (bool): Choose whether to find symbols and aruco markers in a seperate thread
        """
        self.frame = None
        self.stopped = False
        self.aruco = Aruco()
        self.symbols = Symbols()
        self.do_processing = do_processing
        self.processed_frame = None
        self.num_dangerous = 0
        self.num_corrosive = 0
        self.marker_ids = []
         
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def __process(self):
        """Find the symbols and aruco markers in the frame. Used in a Thread.
        """
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            frame = self.get_frame()

            if frame is None:
                continue

            # find arucos in frame
            marker_corners, marker_ids, rejected_candidates = self.aruco.find(frame)

            # draw arucos on frame
            self.aruco.draw(frame, marker_corners, marker_ids)

            # find symbols in frame
            dangerous, corrosive = self.symbols.find(frame)

            # draw symbols on frame
            self.symbols.draw(frame, dangerous, corrosive)

            self.process_frame = frame
            self.num_dangerous = 0 if dangerous is None else len(dangerous)
            self.num_corrosive = 0 if corrosive is None else len(corrosive)
            self.marker_ids = marker_ids

    # protected methods
    def _update(self):
        """Get the frame from the camera. Used in a Thread.

        Raises:
            NotImplementedError: Any child classes must override this method.
        """
        raise NotImplementedError

    def _cleanup(self):
        """Close all streams and video feeds.

        Raises:
            NotImplementedError: Any child classes must override this method.
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def start(self):
        """Start the frame retrieval thread and the processing thread if specified by self.do_processing.
        """
        print('camera recording')
        Thread(target=self._update, args=()).start()
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


class AutoCamera():

    def __init__(self, do_processing=False, resolution=(320, 240), fps=32, pps=None, src=0):
        self.frame = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
        self.stopped = False
        self.fps = fps
        self.pps = pps
        self.prev_time = 0
        self.resolution = resolution
        self.aruco = Aruco()
        self.symbols = Symbols()
        self.do_processing = do_processing
        self.processed_frame = None
        self.num_dangerous = 0
        self.num_corrosive = 0
        self.marker_ids = []

        if src != 0 or not RPI:
            print(f'using webcam with source: {src}')
            self.__init_webcam(src)
        else:
            print('using picam')
            self.__init_picam()

    def __enter__(self):
        self.start()
        return self 

    def __exit__(self, type, value, traceback):
        self.stop()

    def __init_picamera(self):
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.fps = self.fps
        self.raw = PiRGBArray(self.camera, size=resolution)
        time.sleep(0.1)
        self.stream = self.camera.capture_continuous(self.raw,
            format="bgr", use_video_port=True)

    def __init_webcam(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, self.resolution[0])
        self.stream.set(4, self.resolution[1])
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

            # if self.pps is not None and time.time() - self.prev_time < 1./self.pps:
            #     continue

            # self.prev = time.time()

            # otherwise, read the next frame from the stream
            frame = self.get_frame()

            if frame is None:
                continue

            # find arucos in frame
            marker_corners, marker_ids, rejected_candidates = self.aruco.find(frame)

            # draw arucos on frame
            self.aruco.draw(frame, marker_corners, marker_ids)

            # find symbols in frame
            dangerous, corrosive = self.symbols.find(frame)

            # draw symbols on frame
            self.symbols.draw(frame, dangerous, corrosive)

            self.process_frame = frame
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

    def __update_webcam(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.__cleanup()
                return

            # otherwise, read the next frame from the stream
            (_, self.frame) = self.stream.read()

    def __cleanup(self):
        if RPI:
            print('picam closed')
            self.stream.close()
            self.raw.close()
            self.camera.close()
        else:
            print('webcam closed')
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
        raise NotImplementedError

    def start(self):
        """Start the frame retrieval thread and the processing thread if specified by self.do_processing.
        """
        print('camera recording')

        if RPI:
            Thread(target=self.__update_picamera, args=()).start()
        else:
            Thread(target=self.__update_webcam, args=()).start()

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


if __name__ == '__main__':

    if not RPI:
        from gui import Gui
        gui = Gui()
        
        with AutoCamera() as cam:
            while cam.running():
                frame = cam.get_frame()
                if not gui.imshow(frame): break
    
    else:
        from recorder import Recorder 

        with AutoCamera() as cam, Recorder(cam.resolution()) as recorder:
            while (cam.running() and recorder.running()):
                frame = cam.get_frame()
                recorder.write(frame)
        
            
     
    