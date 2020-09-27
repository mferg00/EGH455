import os
import cv2
import numpy as np 
import sys

original = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
name = sys.argv[1][:-4] + 'gray' + '.jpg'
cv2.imwrite(name, gray)
