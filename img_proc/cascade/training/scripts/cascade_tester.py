'''
This is a cascade tester that takes a given folder of images and outputs the same images with
the ROIs that the cascade has found.

Command line arguments:
1. Path to test images folder
2. Path to output image folder
3. Cascade file
'''

import sys
import numpy as np 
import cv2 
import os

def test_samples():
	# load cascade classifier
	cc = cv2.CascadeClassifier(sys.argv[3])

	for img in os.listdir(sys.argv[1]):
		# check its a jpg file
		if(img[-4:] == '.jpg'):

			readName = sys.argv[1] + '/' + img

			# read in image
			image = cv2.imread(readName)
			# convert to gray
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			# run cascade clasifer on image
			results = cc.detectMultiScale(gray, 1.05, 3)
			# draw rectangles around each positive result
			for x,y,w,h in results:
				cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,0), 3)

			writeName = sys.argv[2] + '/' + img
			# save image to folder
			cv2.imwrite(writeName, image)

test_samples()

