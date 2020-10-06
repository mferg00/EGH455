import cv2

vidcap = cv2.VideoCapture('video_targets.mp4')
success,image = vidcap.read()
count = 0
i = 0
success = True
while success:
	success,image = vidcap.read()
	if i%11 == 0:
		cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file
		count += 1
	i = i + 1

