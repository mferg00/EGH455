import cv2
import numpy as np

def void(a):
    pass 

class Gui:
    """Simple class to access openCV gui and add trackbars.
    """
    def __init__(self, title: str="'p' to pause, 'q' to quit"):
        self.stopped = False
        self.title = title
        self.mins = {}
        cv2.namedWindow(self.title)

    def __enter__(self):
        return self 

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def running(self) -> bool:
        """Check if the gui is running.

        Returns:
            bool: True if running
        """
        return not self.stopped

    def cleanup(self):
        """Closes any windows.
        """
        print('cv2 windows closed')
        cv2.destroyAllWindows()

    def add_bar(self, label: str, min: int=1, default: int=1, max: int=100):
        """DEPRECATED
        """
        cv2.createTrackbar(label, self.title, default, max, void)
        self.mins[label] = min

    def get_bar(self, label: str) -> int:
        """DEPRECATED
        """
        return max(cv2.getTrackbarPos(label, self.title), self.mins[label])

    def bar(self, label: str, tmin: int=1, default: int=1, tmax: int=100) -> int:
        """Get the value of a trackbar, automatically adding if not there.

        Args:
            label (str): Trackbar label.
            tmin (int, optional): Trackbar minimum value. Defaults to 1.
            default (int, optional): Trackbar default value. Defaults to 1.
            tmax (int, optional): Trackbar max value. Defaults to 100.

        Returns:
            int: Value of trackbar.
        """
        if label not in self.mins:
            cv2.createTrackbar(label, self.title, default, tmax, void)
            self.mins[label] = tmin
        return max(cv2.getTrackbarPos(label, self.title), self.mins[label])

    def imshow(self, frame: np.ndarray) -> bool:
        """Show a frame.

        Args:
            frame (np.ndarray): Image frame.

        Returns:
            bool: If 'p' (pause) button has been pressed.
        """
        if type(frame) is list:
            new_frame = np.hstack(frame)
        else:
            new_frame = frame

        cv2.imshow(self.title, new_frame)
        key = cv2.waitKey(1) & 0xFF

        self.stopped = \
            ((cv2.getWindowProperty(self.title, cv2.WND_PROP_VISIBLE) < 1) \
            or (key == ord('q')))

        return key == ord('p')

if __name__ == '__main__':
    """Gui testing
    """
    from camera import Camera

    with Camera() as cam, Gui() as gui:
        cam.start()

        while cam.running() and gui.running() and cam.new_frame_event.wait(10):
            frame = cam.get_frame(get_processed=False)

            if gui.imshow(frame):
                cam.toggle_pause()