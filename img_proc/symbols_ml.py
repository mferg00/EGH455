from typing import Tuple, List, Union
import os
import json
from ml.keras_yolo3.utils.utils import get_yolo_boxes, makedirs
from ml.keras_yolo3.utils.bbox import BoundBox, draw_boxes
from keras.models import load_model
import numpy as np

from camera import Processor

class SymbolsMl(Processor):
    """Class to detect and draw hazard symbols using machine learning.

    Args:
        Processor (Processor): Parent class to inherit from.
    """
    def __init__(self,
        config_path: str = 'ml/config_label.json',
        h5_weight_path: str = 'ml/label_frames_2.h5',
        quality: int = 4,
        obj_thresh: float = 0.7,
        nms_thresh: float = 0.3
    ):
        """Initialiser.

        Args:
            config_path (str, optional): Path to generated config json file. Defaults to 'ml/config_label.json'.
            h5_weight_path (str, optional): Path to keras trained .h5 weight path, can be None if specified in config_path. Defaults to 'ml/label_frames_2.h5'.
            quality (int, optional): Multiple of 32 to use for convolution, smaller is faster. Defaults to 4.
            obj_thresh (float, optional): Object threshold, I think higher equals less false negatives. Defaults to 0.7.
            nms_thresh (float, optional): Non-maximal boxes threshold, not sure what this does. Defaults to 0.3.
        """
        self.config_path = config_path
        self.quality = quality 
        self.h5_weight_path = h5_weight_path

        self.net_h, self.net_w = 32 * self.quality, 32 * self.quality # a multiple of 32, the smaller the faster
        self.obj_thresh, self.nms_thresh = obj_thresh, nms_thresh

    def load(self):
        """Load the config and keras model (takes a few seconds)
        """
        with open(self.config_path) as config_buffer:
            self.config = json.load(config_buffer)

        os.environ['CUDA_VISIBLE_DEVICES'] = self.config['train']['gpus']
        self.h5_weight_path = self.config['train']['saved_weights_name'] if not self.h5_weight_path else self.h5_weight_path
        self.infer_model = load_model(self.h5_weight_path)

    def find(self, frame: np.ndarray) -> List[BoundBox]:
        """Find the symbols in the frame.

        Args:
            frame (np.ndarray): Image frame.

        Returns:
            list: List of boundboxes.
        """
        if frame is None:
            return []
        
        batch_boxes = get_yolo_boxes(self.infer_model, [frame], self.net_h, self.net_w, \
            self.config['model']['anchors'], self.obj_thresh, self.nms_thresh)

        return batch_boxes[0]

    def parse_results(self, results: List[BoundBox]) -> dict:
        """Converts the results from find() into a dictionary containing count of each symbol.

        Args:
            results (list): List of boundboxes.

        Returns:
            dict: Dict containing count of symbols.
        """
        counts = dict(zip(self.config['model']['labels'], [0] * len(self.config['model']['labels'])))

        # batch_boxes = [frame 0:[[object 1 boxes], [object n boxes]], frame n:[[object 1 boxes], [object n boxes]]]
        for box in results:
            for i in range(len(self.config['model']['labels'])):
                if box.classes[i] > self.obj_thresh:
                    counts[self.config['model']['labels'][i]] += 1

        return counts

    def draw_results(self, frame: np.ndarray, results: List[BoundBox]):
        """Draw the results from find() to the frame

        Args:
            frame (np.ndarray): Image frame.
            results (list): List of boundboxes
        """
        if results is not None:
            draw_boxes(frame, results, self.config['model']['labels'], self.obj_thresh)

if __name__ == '__main__':
    """Parameter tweaking with ml symbols detection
    """
    from camera import Camera
    from gui import Gui

    processors = [
        SymbolsMl(
            config_path='ml/config_label.json',
            h5_weight_path='ml/label_frames_2.h5',
            quality=4
        )
    ]
    src = 'ml/training/pi-targets.avi'

    with Camera(processors=processors, src=src, fps=60) as cam, Gui() as gui:
        cam.start()

        while cam.running() and gui.running() and cam.new_processed_frame_event.wait(10):

            cam.fps = gui.bar('fps', tmin=1, tmax=64, default=64)

            ###### TWEAK PARAMETERS
            cam.processors[0].obj_thresh = gui.bar('obj thresh: 0.', tmin=1, tmax=9, default=7) / 10.
            cam.processors[0].nms_thresh = gui.bar('nms thresh: 0.', tmin=1, tmax=9, default=3) / 10.
            ######

            frame = cam.get_frame(get_processed=True)

            if gui.imshow(frame):
                cam.toggle_pause()



