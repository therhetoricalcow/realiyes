import Test_GUI
import Polar
import mqtt_test
import tkinter as tk
import numpy as np
import time
import cv2
import Mouse_Sim

##Listening For Connection Screen
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.putText(waiting_background,"Listening for Connection",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
wait_start = time.time()
while(time.time() - wait_start < 30):
    cv2.imshow('Window',waiting_background)
    key = cv2.waitKey(1)
    if key ==27 or key ==113:
        break

##Establishing Connection Screen
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.putText(waiting_background,"Establishing Connection",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
wait_start = time.time()
while(time.time() - wait_start < 20):
    cv2.imshow('Window',waiting_background)
    key = cv2.waitKey(1)
    if key ==27 or key ==113:
        break

##Camera Check Screen
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.putText(waiting_background,"Checking/Streaming Camera Data",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
cap1 = cv2.VideoCapture('/home/avaneesh/Desktop/test_eyes/2021-01-24-221356.mp4')
cap2 = cv2.VideoCapture('/home/avaneesh/Desktop/test_eyes/2021-01-24-221536.mp4')
if (cap1.isOpened()==False or cap2.isOpened()==False):
    print("Error Opening Camera Stream")
wait_start = time.time()
while(time.time() - wait_start < 15):
    cv2.imshow('Window',waiting_background)
    ret1,frame1 = cap1.read()
    ret2,frame2 = cap2.read()
    cv2.waitKey(1000)
    if ret1 == True:
        cv2.imshow('Camera1',cv2.resize(frame1,(224,224)))
    if ret2 == True:
        cv2.imshow('Camera2',cv2.resize(frame2,(224,224)))

    key = cv2.waitKey(500)
    if key ==27 or key ==113:
        break
cap1.release()
cap2.release()
cv2.destroyAllWindows()

##Sensor Check Screen
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.putText(waiting_background,"Checking/Streaming Sensor Data",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
wait_start = time.time()
while(time.time() - wait_start < 6):
    cv2.imshow('Window',waiting_background)
    key = cv2.waitKey(1)
    if key ==27 or key ==113:
        break

##Press Button To Start Calibration Check Screen
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.putText(waiting_background,"Press 'Q' to Start Calibrating",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
wait_start = time.time()
while(time.time() - wait_start < 10):
    cv2.imshow('Window',waiting_background)
    key = cv2.waitKey(1)
    if key ==27 or key ==113:
        break


##Center Box Check Screen
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.rectangle(waiting_background, (int(1920/2 -1),int(1080/2 -1)), (int(1920/2 -1 + 30),int(1080/2 -1 + 30)), (0, 0, 0), -1)
cv2.putText(waiting_background,"Press 'Q' and Look at the Center",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
wait_start = time.time()
while(time.time() - wait_start < 15):
    cv2.imshow('Window',waiting_background)
    cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    key = cv2.waitKey(1)
    if key ==27 or key ==113:
        break

##Edge Devices checking for Output Data
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.putText(waiting_background,"Initializing Edge Devices... Checking for Output Data",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
wait_start = time.time()
while(time.time() - wait_start < 10):
    cv2.imshow('Window',waiting_background)
    cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    key = cv2.waitKey(1)
    if key ==27 or key ==113:
        break

##Start Mouse Control
waiting_background = np.zeros([screen_height,screen_width,3],dtype=np.uint8)
waiting_background.fill(255)
cv2.putText(waiting_background,"Ready! Pres 'Q' to Start..",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255),3)
while(True):
    cv2.imshow('Window',waiting_background)
    cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    key = cv2.waitKey(1)
    if key ==27 or key ==113:
        break

##

waiting_background = np.zeros([screen_height, screen_width, 3], dtype=np.uint8)
waiting_background.fill(255)
box_col = np.arange(0,1921,60)
box_row = np.arange(0,1081,60)
box_size = box_row.size * box_col.size
for i in range(0, 1921, 60):
    for j in range(0, 1081, 60):
        cv2.rectangle(waiting_background, (i, j), (i + 30, j + 30), (0, 0, 0), -1)
mouse = Mouse_Sim.Mouse_Sim()
four_petal = Polar.Polar(k=4,screen_w=screen_width,screen_h=screen_height,numpoints=1000)
xcoords1,ycoords1 = four_petal.diagpetalCartesian()
xcoords2,ycoords2 = four_petal.normpetalCartesian()
xcoords = np.concatenate([xcoords1,xcoords2])
ycoords = np.concatenate([ycoords1,ycoords2])

petal_row = ((ycoords2 - 0.5-screen_height/2 - 1)/(-1)).astype(int)
petal_col = ((xcoords2 + 0.5+screen_width/2 - 1) / 1).astype(int)
start = time.time()
while (True):
    x, y = mouse.getPointer()
    d = np.sqrt(np.square(petal_col - x) + np.square(petal_row - y))
    smallest = d.argmin()
    closestx = petal_col[smallest]
    closesty = petal_row[smallest]

    old_i = i
    old_j = j
    circle_back = np.copy(waiting_background)
    if(time.time() - start >3):
        old_i = i
        old_j = j
        i = np.random.choice(box_row)
        j = np.random.choice(box_col)
        if i == old_i:
            i = np.random.choice(box_row)

        cv2.rectangle(waiting_background, (i, j), (i + 30, j + 30), (0, 255, 0), -1)
        cv2.rectangle(waiting_background, (old_i, old_j), (old_i + 30, old_j + 30), (0, 0, 0), -1)
        start = time.time()
    cv2.circle(circle_back,(int(30*np.random.randn()+closestx),int(30*np.random.randn()+closesty)),10,(0,0,255),-1)
    cv2.imshow('Window',circle_back)
    cv2.namedWindow('Window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    key = cv2.waitKey(100)
    if key ==27 or key ==113:
        break



