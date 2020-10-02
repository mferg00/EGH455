from platform import processor
import cv2
from threading import Thread, Event
from typing import Tuple, Union, List, Iterator

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    RPI = True 
except ImportError:
    RPI = False

import numpy as np
import time

FONT = cv2.FONT_HERSHEY_SIMPLEX

class Processor:
    def load(self):
        raise NotImplementedError

    def find(self, frame: np.ndarray):
        raise NotImplementedError

    def parse_results(self, results):
        raise NotImplementedError

    def draw_results(self, frame: np.ndarray, results):
        raise NotImplementedError

class Camera:
    """Class to record/play pre-recorded video and process that video.
    """
    def __init__(self,
        resolution: Tuple[int, int] = (320, 240),
        fps: int = 32,
        src: Union[int, str] = 0,
        processors: List[Processor] = [],
        prevent_picam: bool = False
    ):
        """Initialiser

        Args:
            resolution (Tuple[int, int], optional): Camera resolution to record in. Defaults to (320, 240).
            fps (int, optional): Frames per second. Defaults to 32.
            src (Union[int, str], optional): Camera src: 0 for webcam, or path to video file. Defaults to 0.
            processors (List[Processor], optional): A list of processor objects to use when processing. Defaults to [].
            prevent_picam (bool, optional): Prevent the picamera module from loading when on a RPi. Defaults to False.
        """
        self.USE_PICAM = RPI and not prevent_picam and src == 0
        self.processors = processors
        self.results: dict = {}
        self.src = src
        self.stopped = False
        self.fps = fps
        self.resolution = resolution
        self.paused = False
        self.new_frame_event = Event()
        self.new_processed_frame_event = Event()
        self.new_processed_frame_event.set()

        self.frame = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
        self.processed_frame = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
        cv2.putText(self.processed_frame, 'Image recognition loading...', 
                    (int(resolution[0] / 6), int(resolution[1] / 6)), FONT, 
                    0.5, (255, 255, 255), 1, 
                    cv2.LINE_AA)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def __process(self):
        """Find the symbols and aruco markers in the frame. Used in a Thread.
        """
        for processor in self.processors:
            processor.load()

        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            if self.new_frame_event.isSet():
                if self.frame is None:
                    continue

                processed_frame = self.frame.copy()

                if processed_frame is None:
                    continue

                for processor in self.processors:
                    results = processor.find(self.frame)
                    self.results.update(processor.parse_results(results))
                    processor.draw_results(processed_frame, results)

                self.processed_frame = processed_frame
                self.new_processed_frame_event.set()

    def __update_picamera(self):
        """Update the picamera, used in a Thread.
        """
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.fps
        self.raw = PiRGBArray(self.camera, size=self.resolution)
        time.sleep(0.1)
        self.stream = self.camera.capture_continuous(self.raw,
            format="bgr", use_video_port=True)

        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            if not self.paused:
                self.frame = f.array

            self.raw.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.__cleanup()
                return

            self.new_frame_event.set()

    def __update_opencv(self):
        """Update the opencv camera, used in a Thread.
        """
        self.stream = cv2.VideoCapture(self.src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.stream.set(cv2.CAP_PROP_FPS, self.fps)
        (_, self.frame) = self.stream.read()

        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.__cleanup()
                return

            # otherwise, read the next frame from the stream
            if not self.paused:
                (ret, self.frame) = self.stream.read()

                if not ret:
                    self.stopped = True 
                    continue

            self.new_frame_event.set()

            time.sleep(1. / self.fps)

    def __cleanup(self):
        """Cleanup the appropriate camera streams.
        """
        if self.USE_PICAM:
            print('picam closed')
            self.stream.close()
            self.raw.close()
            self.camera.close()
        else:
            print('opencv camera closed')
            self.stream.release()

    # PUBLIC METHODS
    def start(self):
        """Start the frame retrieval thread and the processing thread if neccessary.
        """
        if not self.USE_PICAM:
            print(f'recording with openCV from source: {self.src}')
            Thread(target=self.__update_opencv, args=()).start()
        else:
            print('recording with picam module')
            Thread(target=self.__update_picamera, args=()).start()

        if len(self.processors) > 0:
            Thread(target=self.__process, args=()).start()

    def running(self) -> bool:
        """Check whether the camera is still retreiving frames.

        Returns:
            bool: True if camera is still running.
        """
        return not self.stopped

    def resolution(self) -> Tuple[int, int]:
        """Returns the resolution of the camera.
        """
        if self.USE_PICAM:
            return self.camera.resolution
        else:
            width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)

    def toggle_pause(self):
        """Toggle between paused and playing.
        """
        self.paused = not self.paused

    def get_frame(self, get_processed: bool = False) -> np.ndarray:
        """Get the frame from the camera

        Args:
            get_processed (bool, optional): Retrieve the raw frame, or the processed frame with bounding boxes. Defaults to False.

        Returns:
            np.ndarray: The image frame.
        """
        if (get_processed and len(self.processors) > 0):
            frame = self.processed_frame
            self.new_processed_frame_event.clear()
        else:
            frame = self.frame 
            self.new_frame_event.clear()

        return frame

    def get_results(self) -> dict:
        """Get the results after processing the frame.

        Returns:
            dict: A dict containing targets as keys and counts or id arrays as values.
        """
        return self.results

    def stop(self):
        """Stops the camera and processing thread.
        """
        self.stopped = True

if __name__ == '__main__':
    """Gui testing with both processors
    """
    from aruco import Aruco
    from symbols_ml import SymbolsMl
    from gui import Gui

    processors = [
        Aruco(),
        SymbolsMl()
    ]
    src = 'ml/training/pi-targets.avi'

    with Camera(processors=processors, src=src, fps=60) as cam, Gui() as gui:
        cam.start()

        while cam.running() and gui.running() and cam.new_processed_frame_event.wait(10):
            frame = cam.get_frame(get_processed=True)

            if gui.imshow(frame):
                cam.toggle_pause()