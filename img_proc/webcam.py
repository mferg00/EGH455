from camera import Camera
import cv2

class Webcam(Camera):
    """Class to access a webcam.

    Args:
        Camera (Object): Camera class to inherit from.
    """
    def __init__(self, do_processing=False, src=0):
        """Webcam initialiser

        Args:
            do_processing (bool, optional): Do processing (find and draw symbols/markers). Defaults to False.
            src (int, optional): Webcam source. Defaults to 0.
        """
        # initialize the video camera stream and read the first frame
        # from the stream
        super().__init__(do_processing)
        self.stream = cv2.VideoCapture(src)
        (_, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def _update(self):
        """Parent method override, stores frames in self.frame.
        """
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self._cleanup()
                return

            # otherwise, read the next frame from the stream
            (_, self.frame) = self.stream.read()

    def _cleanup(self):
        """Parent method override, closes video stream.
        """
        print('video stream 0 closed')
        self.stream.release()

    def resolution(self):
        """Get the resolution of the webcam

        Returns:
            tuple: Containing:
                - width (int): Width of webcam (px)
                - height (int): Height of webcam (px)
        """
        width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)

if __name__ == '__main__':

    from recorder import Recorder

    with Webcam(do_processing=False) as cam, Recorder(cam.resolution()) as recorder: 
        while cam.running() and recorder.running():
            frame = cam.get_frame()
            recorder.write(frame)


