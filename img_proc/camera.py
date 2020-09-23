import cv2
from threading import Thread

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


