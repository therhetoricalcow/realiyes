##This code is heaviy based and inspired by Yutaloh's 3D Eyetracker
##Written by Avaneesh Murugesan 2020
import cv2
import time
import timeit
import numpy as np
from tkinter import *


class PupilFit:

    def __init__(self,name,ltc = 10,htc = 12,size = 280,dPL1 = 23,dPL2 = 23,pSA = 20,pSX = 50,pSY = 50,d = 4,t = 3,erode = False):
        self.lowThresholdCanny = ltc # default 10: for detecting dark (low contrast) parts of pupil
        self.highThresholdCanny = htc # default 30: for detecting lighter (high contrast) parts of pupil
        self.size = size # default 280: max L/H of pupil
        self.darkestPixelL1 = dPL1 # default 10: for setting low darkness threshold
        self.darkestPixelL2 = dPL2 # default 20: for setting high darkness threshold
        self.pupilSearchArea = pSA # default 20: for setting min size of pupil in pixels / 2
        self.pupilSearchXMin = pSX # default 50: distance from left side of image to start pupil search
        self.pupilSearchYMin = pSY # default 50: distance from right side of image to start pupil search
        self.spacing = d ##spacing
        self.thickness = t ##thickness of drawn lines
        self.erodeOn = erode # perform erode operation: turn off for one-offs, where eroding the image may actually hurt accuracy
        self.name = name
    def __del__(self):
        print(self.name + " has been deleted")

    def getDrawnImage(self,shifted_ellipse,image):
        imagetoDraw = image.copy()
        cv2.ellipse(imagetoDraw,tuple(shifted_ellipse),(0,255,0),1)
        return imagetoDraw
    def getImageSegment(self,shifted_ellipse,image):
        black = np.zeros((image.shape[0], image.shape[1]), dtype='uint8')
        pts = cv2.ellipse2Poly((int(shifted_ellipse[0][0]), int(shifted_ellipse[0][1])), (int(shifted_ellipse[1][0]/2), int(shifted_ellipse[1][1]/2)), int(shifted_ellipse[2]), 0, 360, 1)
        cv2.fillPoly(black,np.int32([pts]),(255,255,255))
        return black

###Setters
    def setLtc(self,val):
        self.lowThresholdCanny = val
    def setHtc(self,val):
        self.highThresholdCanny = val
    def setSize(self,val):
        self.size = val
    def setDpl1(self,val):
        self.darkestPixelL1 = val
    def setDpl2(self,val):
        self.darkestPixelL2 = val
    def setPsa(self,val):
        self.pupilSearchArea = val
    def setPsx(self,val):
        self.pupilSearchXMin = val
    def setPsy(self,val):
        self.pupilSearchYMin = val
    def setSpacing(self,val):
        self.spacing = val
    def setThickness(self,val):
        self.thickness = val
    def setErode(self,val):
        self.erodeOn = val
##Getters
    def getName(self):
        return self.name
    def getLtc(self):
        return self.lowThresholdCanny
    def getHtc(self):
        return self.highThresholdCanny
    def getSize(self):
        return self.size
    def getDpl1(self):
        return self.darkestPixelL1
    def getDpl2(self):
        return self.darkestPixelL2
    def getPsa(self):
        return self.pupilSearchArea
    def getPsx(self):
        return self.pupilSearchXMin
    def getPsy(self):
        return self.pupilSearchYMin
    def getSpacing(self):
        return self.spacing
    def getThickness(self):
        return self.thickness
    def getErode(self):
        return self.erodeOn



    '''
    @param input_img (converted to grayscale)
    @return min_value and locaiton within the iris region
    '''
    def getDarkestPixel(self,input_img):
        assert input_img.shape[0]>50
        assert input_img.shape[1]>50

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(input_img)
        return min_val


    '''
    @param input_img (converted to grayscale)
    @param input_img2 copy of input image onto which geen block of pixels is drawn (BGR), null ok
    @return a point within the iris region
    '''
    def getDarkestPixelArea(self,img):
        rows = img.shape[0]
        cols = img.shape[1]

        # for searching img
        sArea = self.pupilSearchArea
        outerSearchDivisor = 2

        # darkness calculation
        width =20
        searchDivisor = 3

        areaMin = 255 * 9 * searchDivisor ** 2

        ROI = (self.pupilSearchXMin, self.pupilSearchYMin)
        i = self.pupilSearchYMin
        while (i < (rows - width)):
            j = self.pupilSearchXMin
            while (j < (cols - width)):

                intensitySum = np.sum(img[(int(i)):(int(i) + width), (int(j)):(int(j) + width)])
                if (intensitySum < areaMin):
                    ROI = np.array([int(j), int(i)])
                    areaMin = intensitySum

                j = j + sArea / outerSearchDivisor
            i = i + sArea / outerSearchDivisor
        return ROI


    def refinePoints(self,contours, idx, ROI, checkThickness, checkSpacing, rmOutliers=False):
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

    def correctBounds(self,inputPoint,maxSize):

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

    def getBiggest(self,contours):
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


    def pupilAreafitRR(self,orig,debug=False):
        blur = cv2.GaussianBlur(orig, (5, 5), 0)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        darkestPixelConfirm = self.getDarkestPixelArea(gray)

        ##correct bounds
        darkestPixelConfirm = self.correctBounds(darkestPixelConfirm, self.getSize())
        ##find dakrest pixel (for thresholding)
        Rroi = gray[darkestPixelConfirm[1]:(darkestPixelConfirm[1] + self.getSize()),
               darkestPixelConfirm[0]:(darkestPixelConfirm[0] + self.getSize())]
        darkestPixel = self.getDarkestPixel(Rroi)

        erosion_size = 3
        erosion_type = cv2.MORPH_ELLIPSE

        element = cv2.getStructuringElement(erosion_type, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                            (erosion_size, erosion_size))
        if (self.getErode()):
            gray = cv2.erode(gray, element)
        if (debug and self.getErode()):
            cv2.imshow('Eroded',gray)
        ret, threshLow = cv2.threshold(Rroi, int(darkestPixel + self.getDpl1()), 255, cv2.THRESH_BINARY_INV)

        if (debug):
            cv2.imshow('threshlow',threshLow)
        ##find contours
        _,contoursLow, hierarchy = cv2.findContours(threshLow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # ##get biggest contours (iris)
        biggest = self.getBiggest(contoursLow)

        #  #get bounding rect center
        # minX,minY,minW,minH = cv2.boundingRect(contoursLow[biggest])
        # rectCenter = np.array([minX + darkestPixelConfirm[0] + minW/2,minY+darkestPixelConfirm[1] + minH/2])
        # vals = np.array([minW,minH,0])
        # idx = vals.argmax()
        # if(vals[idx] == 0):
        #     maxS = size
        # else:
        #     maxS = vals[idx]

        size2 = self.getSize()
        ret, threshHigh = cv2.threshold(Rroi, int(darkestPixel + self.getDpl2()), 255, cv2.THRESH_BINARY_INV)
        if (debug):
            cv2.imshow('threshHigh',threshHigh)
        ##contours for high threshold
        _,contoursHigh, hierarchy2 = cv2.findContours(threshHigh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        ##
        biggestHigh = self.getBiggest(contoursHigh)
        # gray = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
        green = (0, 255, 0)

        # ##canny params
        # edgeThresh = 1
        # max_lowThreshold = 100
        ratio = 3
        kernel2 = 3

        ##canny to get best canidate points
        thresh3 = cv2.Canny(Rroi, self.getLtc(), self.getLtc() * ratio, kernel2)
        thresh4 = cv2.Canny(Rroi, self.getHtc(), self.getHtc() * ratio, kernel2)

        ##dilating to increase thickness
        dilatethresh3 = cv2.dilate(thresh3, (3, 3), 3)
        dilatethresh4 = cv2.dilate(thresh4, (3, 3), 3)
        if (debug):
            cv2.imshow('dilatethresh3',dilatethresh3)
            cv2.imshow('dilatethresh4',dilatethresh4)
        ##drawing contours
        contourBackground = np.zeros((size2, size2), dtype='uint8')
        drawContoursLow = cv2.drawContours(contourBackground, contoursLow, biggest, (255, 255, 255), self.getThickness())
        drawContoursHigh = cv2.drawContours(contourBackground, contoursHigh, biggestHigh, (255, 255, 255), self.getThickness())

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
        try:
            biggestC = self.getBiggest(contours)
            allPts = self.refinePoints(contours, biggestC, Rroi, self.getSpacing(), 2, True)
            allPts = np.array(allPts, dtype=np.float32)
            ellipse = cv2.fitEllipse(allPts)
            shiftedellipse = ((ellipse[0] + darkestPixelConfirm), ellipse[1], ellipse[2])
            return shiftedellipse


        except:
            shiftedellipse = ([0,0],(0,0),0)
            return shiftedellipse
