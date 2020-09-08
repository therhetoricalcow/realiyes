import cv2

cap0 = cv2.VideoCapture(4)
cap1 = cv2.VideoCapture(2)
print(cap0.isOpened())
print(cap1.isOpened())
ret0, frame0 = cap0.read()
ret1, frame1 = cap1.read()
while(ret0==True and ret1 == True):
    ret0,frame0 = cap0.read()
    ret1,frame1 = cap1.read()
    if(ret0==True and ret1 == True):
        cv2.imshow('right',frame0)
        cv2.imshow('left', cv2.rotate(frame1, cv2.ROTATE_180))
        cv2.waitKey(1)
cap0.release()
cap1.release()
cv2.destroyAllWindows()


