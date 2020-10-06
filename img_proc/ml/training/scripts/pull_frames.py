import cv2

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