import cv2

# Opens the Video file
cap= cv2.VideoCapture('../pi-targets.avi')
i=0
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    if count == 0:
        i+=1
        cv2.imwrite('../frames/frame-'+str(i)+'.jpg',frame)

    count += 1

    if count >= 32:
        count = 0

cap.release()
cv2.destroyAllWindows()