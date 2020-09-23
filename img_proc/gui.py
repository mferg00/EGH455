import cv2

class Gui:
    """Simple class to access openCV gui
    """
    def __enter__(self):
        return self 

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def cleanup(self):
        print('cv2 windows closed')
        cv2.destroyAllWindows()

    def imshow(self, frame):
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF

        return not \
            ((cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1) \
            or (key == ord('q')))
