import cv2
import numpy as np 
import os
import sys

def create_bg_file():
	for img in os.listdir(sys.argv[1]):
		# create file path string
		line = 'neg' + '/' + img + '\n'
		# write line to file
		with open('../bg.txt','a+') as f:
			f.write(line)

create_bg_file()
