from typing import Tuple, List, Union
import os
import argparse
import json
import cv2
from utils.utils import get_yolo_boxes, makedirs
from utils.bbox import draw_boxes
from keras.models import load_model
from tqdm import tqdm
from threading import Thread
import numpy as np

class SymbolsMl:
    def __init__(self,
        config_path: str,
        h5_weight_path: str = '',
        quality: int = 13
    ):
        with open(config_path) as config_buffer:
            self.config = json.load(config_buffer)

        self.net_h, self.net_w = 32 * quality, 32 * quality # a multiple of 32, the smaller the faster
        self.obj_thresh, self.nms_thresh = 0.5, 0.45

        os.environ['CUDA_VISIBLE_DEVICES'] = self.config['train']['gpus']
        self.h5_weight_path = self.config['train']['saved_weights_name'] if not h5_weight_path else h5_weight_path
        self.infer_model = None

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def load(self):
        self.infer_model = load_model(self.h5_weight_path)

    def find(self, frame: np.ndarray) -> Tuple[dict, list]:
        if frame is None:
            return (0, None)
        
        batch_boxes = get_yolo_boxes(self.infer_model, [frame], self.net_h, self.net_w, \
            self.config['model']['anchors'], self.obj_thresh, self.nms_thresh)

        counts = dict(zip(self.config['model']['labels'], [0] * len(self.config['model']['labels'])))

        # batch_boxes = [frame 0:[[object 1 boxes], [object n boxes]], frame n:[[object 1 boxes], [object n boxes]]]
        for box in batch_boxes[0]:
            for i in range(len(self.config['model']['labels'])):
                if box.classes[i] > self.obj_thresh:
                    counts[self.config['model']['labels'][i]] += 1

        return (counts, batch_boxes[0])

    def draw(self, frame: np.ndarray, boxes: list):
        if boxes is not None:
            draw_boxes(frame, boxes, self.config['model']['labels'], self.obj_thresh)


if __name__ == '__main__':

    from camera import Camera
    from gui import Gui

    with \
        SymbolsMl('ml/keras-yolo3/zoo/config_rbc.json', h5_weight_path='ml/keras-yolo3/rbc.h5', quality=6) as symbols, \
        Camera(src='ml/keras-yolo3/zoo/BCCD_Dataset/video.avi', fps=1) as cam, \
        Gui() as gui:
        while cam.running() and gui.running():
            frame = cam.get_frame()

            count, boxes = symbols.find(frame)
            symbols.draw(frame, boxes)

            if gui.imshow(frame):
                cam.toggle_pause()



