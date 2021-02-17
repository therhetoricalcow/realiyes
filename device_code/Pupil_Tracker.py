from threading import Thread
import cv2
import numpy as np
import PIL
class Pupil_Tracker:
	def __init__(self,src1 = -1,src2 = 2):
		self.stream1 = cv2.VideoCapture(src1)
		self.stream2 = cv2.VideoCapture(src2)
		(self.grabbed1, self.frame1) = self.stream1.read()
		(self.grabbed2, self.frame2) = self.stream2.read()
		self.stopped = False
		while(self.grabbed1 == False and self.grabbed2 == False):
			(self.grabbed1, self.frame1) = self.stream1.read()
			(self.grabbed2, self.frame2) = self.stream2.read()
	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
	while True:
		if self.stopped:
			return
		(self.grabbed1,self.frame1) = self.stream1.read()
		(self.grabbed2,self.frame2) = self.stream2.read()

	def read(self):
		return self.frame1,self.frame2


	def preprocess(self,frame):
		frame = cv2.resize(frame,(224,224))
		frame = frame.astype('float32')/255.0
		frame = np.expand_dims(frame,axis=0)
		return frame

	def blobFinder(self,frame):
		frame = frame.astype('int8')
		mask = np.zeros((frame.shape[0],frame.shape[1]),dtype = 'int8')
		cv2.rectangle(mask,(10,10),(214,214),(255,255,255),-1)
		blur = cv2.GaussianBlur(frame,(5,5),0)
		threshed = cv2.threshold(blur,10,255,cv2.THRESH_BINARY)[1]
		output = cv2.bitwise_and(threshed,mask,mask = None)
		contours,hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		output = cv2.cvtColor(output,cv2.COLOR_GRAY2BGR)
		if len(contours) != 0:
			cv2.drawContours(output,contours,-1,255,3)
			c = max(contours,key = cv2.contourArea)
			ellipse = cv2.fitEllipse(c)
			cv2.ellipse(output,ellipse,(0,255,0),2)
		return output
	
	def blobEllipse(self,frame):
		frame = frame.astype('int8')
		mask = np.zeros((frame.shape[0],frame.shape[1]),dtype = 'int8')
		cv2.rectangle(mask,(10,10),(214,214),(255,255,255),-1)
		blur = cv2.GaussianBlur(frame,(5,5),0)
		threshed = cv2.threshold(blur,10,255,cv2.THRESH_BINARY)[1]
		output = cv2.bitwise_and(threshed,mask,mask = None)
		contours,hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		if len(contours) != 0:
			c = max(contours,key = cv2.contourArea)
			(x,y),(MA,ma),angle = cv2.fitEllipse(c)
		return (x,y),(MA,ma),angle

	def stop(self):
		self.stopped = True

