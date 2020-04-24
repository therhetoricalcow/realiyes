##This code is heaviy based and inspired by Yutaloh's 3D Eyetracker

import cv2
import time
import timeit
import numpy as np
from tkinter import *

##Global Params
lowThresholdCanny = 10 #default 10: for detecting dark (low contrast) parts of pupil
highThresholdCanny = 12 #default 30: for detecting lighter (high contrast) parts of pupil
size = 175; #default 280: max L/H of pupil
darkestPixelL1 = 23 #default 10: for setting low darkness threshold
darkestPixelL2 = 23 #default 20: for setting high darkness threshold
pupilSearchArea = 20 #default 20: for setting min size of pupil in pixels / 2
pupilSearchXMin = 50 #default 0: distance from left side of image to start pupil search
pupilSearchYMin = 50 #default 0: distance from right side of image to start pupil search
dilation = 3 ##how much to dilate threshedging by
thickness = 6 ##thickness of drawn lines
erodeOn = False #perform erode operation: turn off for one-offs, where eroding the image may actually hurt accuracy




class PupilFit:
    def __init__(self):
        thresh = True

    def __del__(self,thresh0):
        thresh = thresh0

'''
@param input_img (converted to grayscale)
@return min_value and locaiton within the iris region
'''
def getDarkestPixel(input_img):
    assert input_img.shape[0]>50
    assert input_img.shape[1]>50

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(input_img)
    return min_val


'''
@param input_img (converted to grayscale)
@param input_img2 copy of input image onto which geen block of pixels is drawn (BGR), null ok
@return a point within the iris region
'''
def getDarkestPixelArea(img):
    rows = img.shape[0]
    cols = img.shape[1]

    # for searching img
    sArea = 10
    outerSearchDivisor = 2

    # darkness calculation
    width = 30
    searchDivisor = 3

    areaMin = 255 * 9 * searchDivisor ** 2

    ROI = (pupilSearchXMin, pupilSearchYMin)
    i = pupilSearchYMin
    while (i < (rows - width)):
        j = pupilSearchXMin
        while (j < (cols - width)):

            intensitySum = np.sum(img[(int(i)):(int(i) + width), (int(j)):(int(j) + width)])
            if (intensitySum < areaMin):
                ROI = np.array([int(j), int(i)])
                areaMin = intensitySum

            j = j + sArea / outerSearchDivisor
        i = i + sArea / outerSearchDivisor
    return ROI


def refinePoints(contours, idx, ROI, checkThickness, checkSpacing, rmOutliers=False):
    i = 0
    refinedPoints = []
    for i in range(len(contours[idx])):
        finalX = contours[idx][i][0][0]
        finalY = contours[idx][i][0][1]

        if ((contours[idx][i][0][0] - checkThickness * checkSpacing - 1) >= 0 and (
                contours[idx][i][0][0] + checkThickness * checkSpacing + 1) < ROI.shape[1]):
            xNumerator = 0
            xDenominator = 0
            j = -checkThickness * checkSpacing
            while (j < checkThickness * checkSpacing):
                centerValue = ROI[contours[idx][i][0][1], contours[idx][i][0][0] + j]
                leftDiff = np.abs(centerValue - ROI[contours[idx][i][0][1], contours[idx][i][0][0] + j - 1])
                rightDiff = np.abs(centerValue - ROI[contours[idx][i][0][1], contours[idx][i][0][0] + j + 1])
                xNumerator += (contours[idx][i][0][0] + j) * (leftDiff + rightDiff)
                xDenominator += (leftDiff + rightDiff)
                j = j + checkSpacing
            if (xDenominator != 0):
                finalX = xNumerator / xDenominator
        if ((contours[idx][i][0][1] - checkThickness * checkSpacing - 1) >= 0 and (
                contours[idx][i][0][1] + checkThickness * checkSpacing + 1) < ROI.shape[0]):
            yNumerator = 0
            yDenominator = 0
            j = -checkThickness * checkSpacing
            while (j < checkThickness * checkSpacing):
                centerValue2 = ROI[contours[idx][i][0][1] + j, contours[idx][i][0][0]]
                topDiff = np.abs(centerValue2 - ROI[contours[idx][i][0][1] + j - 1, contours[idx][i][0][0]])
                botDiff = np.abs(centerValue2 - ROI[contours[idx][i][0][1] + j + 1, contours[idx][i][0][0]])
                yNumerator += (contours[idx][i][0][1] + j) * (topDiff + botDiff)
                yDenominator += (topDiff + botDiff)
                j = j + checkSpacing
            if (yDenominator != 0):
                finalY = yNumerator / yDenominator

        refinedPoints.append([[finalX, finalY]])

    return refinedPoints

def correctBounds(inputPoint,maxSize):

    ##max Size of Pupil ROI
    size = maxSize

    #x/y from input point
    mcX = inputPoint[0]
    mcY = inputPoint[1]

    newX = mcX - size/2
    newY = mcY - size/2

    if(newX<0):
        newX = 0
    elif(newX > 639 - size):
        newX -= newX - 639 + size
    if(newY < 0):
        newY = 0
    elif(newY>479 -size):
        newY -= newY - 479 + size
    return np.array([int(newX),int(newY)])

def getBiggest(contours):
    biggestOut = 0
    i = 0
    biggestSize = 0
    for i in range(len(contours)):
        M = cv2.moments(contours[i]) ##Moments
        if(M['m00']!=0):
          cx = int(M['m10'] / M['m00'])
          cy = int(M['m01']/M['m00'])
        else:
          cx = 0
          cy = 0
        if(cy >10 and cx < 620):
            area = cv2.contourArea(contours[i])
            if(area > biggestSize):
                biggestSize = area
                biggestOut = i

    return biggestOut


def pupilAreafitRR(orig,debug):
    start = time.time()
    blur = cv2.GaussianBlur(orig, (5, 5), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    darkestPixelConfirm = getDarkestPixelArea(gray)

    ##correct bounds
    darkestPixelConfirm = correctBounds(darkestPixelConfirm, size)
    ##find dakrest pixel (for thresholding)
    Rroi = gray[darkestPixelConfirm[1]:(darkestPixelConfirm[1] + size),
           darkestPixelConfirm[0]:(darkestPixelConfirm[0] + size)]
    darkestPixel = getDarkestPixel(Rroi)

    erosion_size = 3
    erosion_type = cv2.MORPH_ELLIPSE

    element = cv2.getStructuringElement(erosion_type, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                        (erosion_size, erosion_size))
    if (erodeOn):
        gray = cv2.erode(gray, element)
    if (debug and erodeOn):
        cv2.imshow('Eroded',gray)
    ret, threshLow = cv2.threshold(Rroi, int(darkestPixel + darkestPixelL1), 255, cv2.THRESH_BINARY_INV)

    if (debug):
        cv2.imshow('threshlow',threshLow)
    ##find contours
    _,contoursLow, hierarchy = cv2.findContours(threshLow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # ##get biggest contours (iris)
    biggest = getBiggest(contoursLow)

    #  #get bounding rect center
    # minX,minY,minW,minH = cv2.boundingRect(contoursLow[biggest])
    # rectCenter = np.array([minX + darkestPixelConfirm[0] + minW/2,minY+darkestPixelConfirm[1] + minH/2])
    # vals = np.array([minW,minH,0])
    # idx = vals.argmax()
    # if(vals[idx] == 0):
    #     maxS = size
    # else:
    #     maxS = vals[idx]

    size2 = size
    ret, threshHigh = cv2.threshold(Rroi, int(darkestPixel + darkestPixelL2), 255, cv2.THRESH_BINARY_INV)
    if (debug):
        cv2.imshow('threshHigh',threshHigh)
    ##contours for high threshold
    _,contoursHigh, hierarchy2 = cv2.findContours(threshHigh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    ##
    biggestHigh = getBiggest(contoursHigh)
    # gray = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    green = (0, 255, 0)

    # ##canny params
    # edgeThresh = 1
    # max_lowThreshold = 100
    ratio = 3
    kernel2 = 3

    ##canny to get best canidate points
    thresh3 = cv2.Canny(Rroi, lowThresholdCanny, lowThresholdCanny * ratio, kernel2)
    thresh4 = cv2.Canny(Rroi, highThresholdCanny, highThresholdCanny * ratio, kernel2)

    ##dilating to increase thickness
    dilatethresh3 = cv2.dilate(thresh3, (dilation, dilation), 3)
    dilatethresh4 = cv2.dilate(thresh4, (dilation, dilation), 3)
    if (debug):
        cv2.imshow('dilatethresh3',dilatethresh3)
        cv2.imshow('dilatethresh4',dilatethresh4)
    ##drawing contours
    contourBackground = np.zeros((size2, size2), dtype='uint8')
    drawContoursLow = cv2.drawContours(contourBackground, contoursLow, biggest, (255, 255, 255), thickness)
    drawContoursHigh = cv2.drawContours(contourBackground, contoursHigh, biggestHigh, (255, 255, 255), thickness)

    if (debug):
        cv2.imshow('drawContoursLow',drawContoursLow)
        cv2.imshow('drawContoursHigh',drawContoursHigh)
    ##bitwise_ands of contours and thresholds
    ctland = cv2.bitwise_and(drawContoursLow, dilatethresh3, mask=None)
    cthand = cv2.bitwise_and(drawContoursHigh, dilatethresh4, mask=None)
    ctOR = cv2.bitwise_or(ctland, cthand, mask=None)
    if (debug):
        cv2.imshow('ctland',ctland)
        cv2.imshow('cthand',cthand)
        cv2.imshow('cTOR',ctOR)

    _,contours, hierarchy = cv2.findContours(ctOR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggestC = getBiggest(contours)



    try:
        allPts = refinePoints(contours, biggestC, Rroi, 4, 2, True)

        allPts = np.array(allPts, dtype=np.float32)

        ellipse = cv2.fitEllipse(allPts)


        shiftedellipse = ((ellipse[0] + darkestPixelConfirm), ellipse[1], ellipse[2])

        cv2.ellipse(orig, shiftedellipse, green, 2)
    except:
        print('No ellipse in boundary')
    end = time.time() - start
    print(end)
    cv2.imshow('cam',orig)
    cv2.waitKey(1)
def setSliderValues():
    lowThresholdCanny = w1.get()
    highThresholdCanny = w2.get()
    size = w3.get()
    darkestPixelL1 = w4.get()
    darkestPixelL2 = w5.get()


master = Tk()
w1 = Scale(master,from_=0,to= 50,orient=HORIZONTAL,label = "lowThresholdCanny")
w1.set(10)
w1.pack()
w2 = Scale(master,from_=0,to= 50,orient = HORIZONTAL,label = "highThresholdCanny")
w2.set(30)
w2.pack()
w3 = Scale(master,from_=0,to= 300,orient = HORIZONTAL,label = "size")
w3.set(150)
w3.pack()
w4 = Scale(master,from_=0,to= 20,orient = HORIZONTAL,label = "darkestPixelL1")
w4.set(8)
w4.pack()
w5 = Scale(master,from_=0,to= 20,orient = HORIZONTAL,label = "darkestPixelL2")
w5.set(15)
w5.pack()

while(True):

    pupilAreafitRR(frame0,True)
    setSliderValues()
mainloop()


cap0.release()
cv2.destroyAllWindows()
