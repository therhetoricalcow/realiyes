import cv2
import numpy as np
import random as r
from matplotlib import pyplot as plt
import time
import os
import cv2
import ctypes
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

height = screen_height +1
width = screen_width +1
##BGR
white = np.ones((height, width, 3), dtype="uint8") * 255

black = (0, 0, 0)
grey = (128, 128, 128)
green = (0, 255, 0)
red = (0, 0, 255)
img_dir = '/home/avaneesh/Desktop/Images'

"""
Using BGR Format ccp takes in an coordinates, the image,
desired color, the number of layers you want the 'cross' to be for visiblity
and returns an image with the cross
"""


def ccp(x, y, inputimg, color, layers):
    img = inputimg
    img[y, x, :] = color[:]
    for i in range(layers):

        if (x - i > 0): img[y, x - i, :] = color[:]
        if (x + i < width): img[y, x + i, :] = color[:]
        if (y - i > 0 and x - i > 0): img[y - i, x - i, :] = color[:]
        if (y - i > 0 and x + i < width): img[y - i, x + i, :] = color[:]
        if (y + i < height and x - i > 0): img[y + i, x - i, :] = color[:]
        if (y + i < height and x + i < width): img[y + i, x + i, :] = color[:]
        if (y - i > 0): img[y - i, x, :] = color[:]
        if (y + i < height): img[y + i, x, :] = color[:]
    return img


"""
Given a height and width and the number of points for sensitivity you want to
have your data getPoints returns two numpy arrays with points equidistant
"""


def getPoints(height, width, samp):
    newY = np.empty([samp, 1], dtype=int)
    newX = np.empty([samp, 1], dtype=int)
    for i in range(samp):
        newY[i] = (i / (samp - 1)) * height
        newX[i] = (i / (samp - 1)) * width
    return newY, newX


"""
Given 2 numpy arrays, getSamples iterates and returns an array with all 
a all possible datapoints 
"""
def getSamples(Y, X):
    i = 0
    j = 0
    c = 0
    data = np.empty(shape=(Y.size * X.size, 2), dtype=int)
    for i in range(Y.size):
        for j in range(X.size):
            data[c, 0] = X[j]
            data[c, 1] = Y[i]
            c += 1
    return data


def imagedirectory(data):
    i = 0
    try:
        os.mkdir(img_dir)
        for i in range(len(data)):
            x = data[i, 0]
            y = data[i, 1]
            img_directory = img_dir + '/' +str(x) + '_' + str(y)
            os.mkdir(img_directory)
            os.mkdir(img_directory + '/right')
            os.mkdir(img_directory + '/left')
    except:
        print("Folder is Already There!")


nY, nX = getPoints(1080, 1920, 10)
data = getSamples(nY, nX)

cap0 = cv2.VideoCapture(4)
cap1 = cv2.VideoCapture(2)
imagedirectory(data)
ret0,frame0 = cap0.read()
ret1,frame1 = cap1.read()
while (ret0==True and ret1 == True):
    ret0,frame0 = cap0.read()
    ret1,frame1 = cap1.read()
    #
    cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    i = 0
    for i in range(len(data)):
        blackp = ccp(data[i][0], data[i][1], white, black, 5)
        cv2.imshow('screen', blackp)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
        redp = ccp(data[i][0], data[i][1], white, red, 5)

        cv2.imshow('screen', redp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        s1 = time.time()
        j = 0
        while (time.time() - s1 < 2):

            ret0, frame0 = cap0.read()
            ret1, frame1 = cap1.read()
            img_direct = img_dir + '/'+str(data[i, 0]) + '_' + str(data[i, 1])
            print(img_direct)
            os.chdir(img_direct + '/right')
            cv2.imwrite(str(j) + '.png', frame0)
            os.chdir(img_direct + '/left')
            cv2.imwrite(str(j) + '.png', cv2.rotate(frame1, cv2.ROTATE_180))
            j += 1

        greenp = ccp(data[i][0], data[i][1], white, green, 5)

        cv2.imshow('screen', greenp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    break

cap0.release()
cap1.release()
cv2.destroyAllWindows()