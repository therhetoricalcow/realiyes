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

listener = keyboard.Listener(on_press=on_press)
listener.start()
j = 0
for a in range(2,41):
	locDir = '/home/pi/Desktop/Recordings/camera_points/' + str(a) + '/'
	imgDir = locDir + 'images/'
	frame1Dir = imgDir + 'frame1/'
	frame2Dir = imgDir + 'frame2/'
	recDir = locDir + 'recording/'

	postData = np.array([None])
	preData = np.genfromtxt(recDir + str(a) + '.csv',delimiter = ',')
	preData = np.transpose(preData)
	oldellipse1 = np.array([[np.nan,np.nan,np.nan,np.nan,np.nan]])
	oldellipse2 = np.array([[np.nan,np.nan,np.nan,np.nan,np.nan]])
	print(preData.shape)
	for b in range(1,preData.shape[0]+1):
		img1Path = frame1Dir + str(b) + '.png'
		if(os.path.exists(img1Path)):
			frame1 = cv2.imread(frame1Dir + str(b) + '.png')
			frame2 = cv2.imread(frame2Dir + str(b) + '.png')
			frame2 = decrease_brightness(frame2)
			frame1 = increase_brightness(frame1)
#			oldellipse1 = np.array([[np.nan,np.nan,np.nan,np.nan,np.nan]])
#			oldellipse2 = np.array([[np.nan,np.nan,np.nan,np.nan,np.nan]])
			while(keep == False and remove == False):
#				frame1 = increase_brightness(frame1,ab)
#				frame2 = increase_brightness(frame2,ab)
				ab = 0
				predframe1 = model.predict(frame1)
				predframe2 = model.predict(frame2)
				ellipsed_frame1,ellipse1 = blobFinder(predframe1,30)
				ellipsed_frame2,ellipse2 = blobFinder(predframe2,15)
				cv2.imshow('raw_f1',frame1)
				cv2.imshow('raw_f2',frame2)
				cv2.imshow('ellipse_f1',ellipsed_frame1)
				cv2.imshow('ellipse_f2',ellipsed_frame2)
				
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
					dataRow = preData[b-1,:]
				
					dataRow = np.hstack((ellipse1,ellipse2,dataRow.reshape((1,4))))
					postData = dataRow
					print(b/preData.shape[0])
				else:
					dataRow = preData[b-1,:]
					dataRow = np.hstack((ellipse1,ellipse2,dataRow.reshape((1,4))))
					postData = np.vstack((postData, dataRow))
					print(b/preData.shape[0])
			if(remove == True):
				print('File Deleted')
				print(postData.shape)
	#			os.remove(frame1Dir + str(b) + '.png')
	#			os.remove(frame2Dir + str(b) + '.png')
				pass

			keep = False
			remove = False
			storeOld = False
			useOld = False
		else:
			print('Img Doesnt exist')
	saveDir = '/home/pi/Desktop/Recordings/camera_points/recordings/'
	np.savetxt(saveDir +str(a) + '.csv',postData,delimiter=',' )
	print('Wrote Save File')
