import os
import cv2
import numpy as np 
import sys

original = cv2.imread(sys.argv[1])
resized = cv2.resize(original, (50,50))
name = sys.argv[1][:-4] + 'resized' + '.jpg'
cv2.imwrite(name, resized)

