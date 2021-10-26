import GUI
import Polar
import LiveDisplay
import time
import numpy as np
import cv2
import paho.mqtt.client as mqtt
from pynput import keyboard
global i
import os.path
from os import path

test = GUI.GUI(10)
w,h = test.getScreenDim()
four_petal = Polar.Polar(k=4,screen_w=w,screen_h=h,reverse=False,num_times=1,numpoints=1000)
xcoords,ycoords = four_petal.normpetalCartesian()
print(xcoords,ycoords)
start = time.time()
display_one = LiveDisplay.LiveDisplay('Four Petal',test,xcoords,ycoords,"/home/avaneesh/Desktop/Recordings/test.csv")
display_one.run()
print(time.time() - start)