from tflite_model import tflite_model
import numpy as np
import cv2
import os
from pynput import keyboard
import re

ab = 0
keyPressed = False
remove = False
keep = False
storeOld = False
useOld = False
model = tflite_model(model_file = '../../Downloads/model_edgetpu_25.tflite')

def blobFinder(frame,box_cut = 20):
	mask = np.zeros((224,224),dtype = 'uint8')
	cv2.rectangle(mask,(box_cut,box_cut),(224-box_cut,224-box_cut),(255,255,255),-1)
	blur = cv2.GaussianBlur(frame,(7,7),0)

	threshed = cv2.threshold(blur,0,255,cv2.THRESH_BINARY)[1]

	output = cv2.bitwise_and(threshed,mask,mask = None)
	contours,hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	output = cv2.cvtColor(output,cv2.COLOR_GRAY2BGR)
	x = np.nan
	y = np.nan
	MA = np.nan
	ma = np.nan
	angle = np.nan
	ellipse = np.nan
	if len(contours) != 0:
		cv2.drawContours(output,contours,-1,255,3)
		c = max(contours,key = cv2.contourArea)
		try:
			((x,y),(MA,ma),angle) = cv2.fitEllipse(c)
			ellipse = ((x,y),(MA,ma),angle)
			cv2.ellipse(output,ellipse,(0,255,0),2)
		except:
			
			pass
	return output, np.array([[x,y,MA,ma,angle]])

def sorted_nicely(l):

	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(l,key,alphanum_key)

def on_press(key):
	global storeOld
	global remove
	global keep
	global useOld 
#	print('Key pressed' + key)
	if(key ==  keyboard.Key.up):
		storeOld = True
	if(key == keyboard.Key.down):
		useOld = True
	if(key == keyboard.Key.left):
		remove = True
		keep = False
	if(key == keyboard.Key.right):
		keep = True
		remove = False
	

def increase_brightness(img,value = 0):
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	h,s,v = cv2.split(hsv)
	lim = 255-value
	v[v>lim] = 255
	v[v<=lim] +=value
	final_hsv = cv2.merge((h,s,v))
	return img
def decrease_brightness(img):
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	hsv[...,2] = hsv[...,2]*0.95
#	h,s,v=cv2.split(hsv)
#	lim = 255- value
#	v[v>lim] = 255
#	v[v<=lim] += value
#	final_hsv = cv2.merge((h,s,v))
	img = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
	return img

def imuEllipseDataCombine(imuData,ellipseData):
	print(imuData.shape)
	imuData = imuData[~np.isnan(imuData).any(axis=1)]
	print(imuData.shape)
	splits = int(imuData.shape[0]/ellipseData.shape[0])
	e = imuData[::splits,:]
	while(e.shape[0] != ellipseData.shape[0]):
		rand = np.random.random_sample()
		numb = int((e.shape[0]) * rand)
		e = np.delete(e,numb,axis=0)
	data = np.hstack((ellipseData,e))
	return data

listener = keyboard.Listener(on_press=on_press)
listener.start()
j = 0
for a in range(1,17):
	print("Starting Dataset:" + str(a) )
	locDir = '/home/pi/Desktop/Recordings/camera_points/' + str(a) + '/'
	frame1Vid = locDir + str(a) + 'frame1_' + str(a) + '.avi'
	frame2Vid = locDir + str(a) + 'frame2_' + str(a) + '.avi'
	imuData = locDir + str(a) + 'data.csv'
	cap1 = cv2.VideoCapture(frame1Vid)
	cap2 = cv2.VideoCapture(frame2Vid)
	cap1FrameCount = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
	cap2FrameCount = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
	print(str(cap1FrameCount) + ' Frames in CAP1')
	print(str(cap2FrameCount) + ' Frames in CAP2')
	postData = np.array([None])
	imuData = np.genfromtxt(imuData,delimiter = ',')
	oldellipse1 = np.array([[np.nan,np.nan,np.nan,np.nan,np.nan]])
	oldellipse2 = np.array([[np.nan,np.nan,np.nan,np.nan,np.nan]])
	print(str(imuData.shape[0]) + " Samples in IMU RECORDING")
	b = 1
	while(cap1.isOpened()):
		ret1,frame1 = cap1.read()
		ret2,frame2 = cap2.read()
		if(ret1 and ret2):
			while(keep == False and remove ==  False):
				ab = 0
				frame1 = cv2.resize(frame1,(224,224))
				frame2 = cv2.resize(frame2,(224,224))
				predframe1 = model.predict(frame1)
				predframe2 = model.predict(frame2)
				ellipse_frame1,ellipse1 = blobFinder(predframe1,20)
				ellipse_frame2,ellipse2 = blobFinder(predframe2,20)
				cv2.imshow('raw_f1',frame1)
				cv2.imshow('raw_f2',frame2)
				cv2.imshow('ellipse_f1',ellipse_frame1)
				cv2.imshow('ellipse_f2',ellipse_frame2)
				cv2.waitKey(1)
				if(storeOld == True):
					print('stored')
					oldellipse1 = ellipse1
					oldellipse2 = ellipse2
					j = b
				if(keep == True):
					print('File Kept')
					if(useOld == True):
						print('Using Old Ellipse from '+  str(j) )
						ellipse1 = oldellipse1
						ellipse2 = oldellipse2
						print(ellipse1)
					if(postData.any() == None):
						dataRow = np.hstack((ellipse1,ellipse2))
						postData = dataRow
						print(str(100 * b/cap1FrameCount) + "% Done")
					else:
						dataRow = np.hstack((ellipse1,ellipse2))
						postData = np.vstack((postData, dataRow))
						print(str(100 * b/cap1FrameCount) + "% Done") 
				if remove == True:
					print('Not Being Used')
					print(postData.shape)
					pass

			keep = False
			remove = False
			storeOld = False
			useOld = False
			b = b + 1
		else:
			break
	cap1.release()
	cap2.release()
	data = imuEllipseDataCombine(imuData,postData)
	saveDir = '/home/pi/Desktop/Recordings/camera_points/'
	np.savetxt(saveDir +str(a) + '.csv',data,delimiter=',' )
	print('Wrote Save File')
