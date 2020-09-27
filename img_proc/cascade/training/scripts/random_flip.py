import cv2
import numpy as np
import os
import sys
import random

def rotate():
    for img in os.listdir(sys.argv[1]):
        if(img[-4:] == '.jpg'):
            # create file path string
            filepath = sys.argv[1] + img
            img = cv2.imread(filepath)

            num = random.randint(0, 4)

            if num == 0:
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            elif num == 1:
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif num == 2:
                img = cv2.rotate(img, cv2.ROTATE_180)

            cv2.imwrite(filepath, img)


rotate()