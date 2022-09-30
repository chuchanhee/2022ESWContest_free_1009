import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
cap1 = cv2.VideoCapture(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


while(True):
    ret,frame = cap.read()
    ret2,frame2 = cap1.read()

    if ret2:
        cv2.imshow('1',frame2)

        if cv2.waitKey(1) & 0XFF ==27:
            break
    if ret:
        cv2.imshow('2',frame)

        if cv2.waitKey(1) & 0XFF == 27:
            break

cap.release()
cap1.release()
cv2.destroyAllWindows()

