import cv2

<<<<<<< HEAD
# Opens the Video file
cap= cv2.VideoCapture('../mi5s-targets/mi5s-targets.mp4')
i=0
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    if count == 16:
        i+=1
        cv2.imwrite('../mi5s-targets/imgs/frame-'+str(i)+'a.jpg',frame)

    count += 1

    if count >= 32:
        count = 0

cap.release()
cv2.destroyAllWindows()
=======

files = [
    '/home/max/uni/EGH455/EGH455/img_proc/ml/training/targets2/VID_20201006_163655.mp4',
    '/home/max/uni/EGH455/EGH455/img_proc/ml/training/targets2/VID_20201006_163926.mp4',
    '/home/max/uni/EGH455/EGH455/img_proc/ml/training/targets2/VID_20201006_164142.mp4'
]

i=0

for file in files:
    # Opens the Video file
    cap= cv2.VideoCapture(file)

    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break

        if count == 0:
            i+=1
            cv2.imwrite('../targets2/imgs/image'+str(i)+'.jpg', frame)

        count += 1

        if count >= 32:
            count = 0

    cap.release()
>>>>>>> origin/master
