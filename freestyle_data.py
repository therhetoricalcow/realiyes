import cv2

import os


img_dir = '/home/avaneesh/Desktop/freestyle_imgs'
def imagedirectory():
    i = 0
    try:
        os.mkdir(img_dir)
    except:
        print("Folder is Already There!")

cap0 = cv2.VideoCapture(7)
cap1 = cv2.VideoCapture(3)
print(cap0.isOpened())
print(cap1.isOpened())
imagedirectory()
os.chdir(img_dir)
i = 0
while(True):
    ret0,frame0 = cap0.read()
    ret1,frame1 = cap1.read()
    if(ret0==True and ret1 == True):
        cv2.imwrite(str(i)+ '.png', cv2.rotate(frame1, cv2.ROTATE_180))
        i = i + 1
        cv2.imwrite(str(i) + '.png',frame0)
        i = i + 1
