import Mouse_Sim
import numpy as np
import cv2
import tkinter as tk
import Polar
import time
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
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

petal_row = ((ycoords1 - 0.5-screen_height/2 - 1)/(-1)).astype(int)
petal_col = ((xcoords1 + 0.5+screen_width/2 - 1) / 1).astype(int)
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

