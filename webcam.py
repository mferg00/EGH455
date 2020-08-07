from camera import Camera
import cv2

class Webcam(Camera):

    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (_, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def cleanup(self):
        print('video stream 0 closed')
        self.stream.release()

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.cleanup()
                return

            # otherwise, read the next frame from the stream
            (_, self.frame) = self.stream.read()

    def resolution(self):
        width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)

if __name__ == '__main__':

    from gui import Gui

    with Webcam() as cam, Gui() as gui: 
        while cam.running():
            frame = cam.read()  
            if not gui.imshow(frame): break


