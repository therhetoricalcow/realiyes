from threading import Thread
import cv2
import numpy as np
import PIL
class Pupil_Tracker:
	def __init__(self,src1 = -1,src2 = 2):
		self.stream1 = cv2.VideoCapture(src1)
		self.stream2 = cv2.VideoCapture(src2)
		self.stream1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
		self.stream2.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
		(self.grabbed1, self.frame1) = self.stream1.read()
		(self.grabbed2, self.frame2) = self.stream2.read()
		self.stopped = False
		while(self.grabbed1 == False or self.grabbed2 == False):
			(self.grabbed1, self.frame1) = self.stream1.read()
			(self.grabbed2, self.frame2) = self.stream2.read()
	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while(True):
			if self.stopped:
				return
			
			(self.grabbed1,frame1) = self.stream1.read()
			(self.grabbed2,frame2) = self.stream2.read()
			while(self.grabbed1 == False or self.grabbed2 == False):
				(self.grabbed1,frame1) = self.stream1.read()
				(self.grabbed2,frame2) = self.stream2.read()
			self.frame1 = frame1
			self.frame2 = frame2
	def read(self):
		frame1 = cv2.resize(self.frame1,(224,224))
		frame2 = cv2.resize(self.frame2,(224,224))
		return frame1,frame2


	def preprocess(self,frame1,frame2):
#		frame1 = cv2.resize(self.frame1,(224,224))
#		frame2 = cv2.resize(self.frame2,(224,224))
		frame1 = frame1.astype('float32')/255.0
		frame2 = frame2.astype('float32')/255.0
		frame1 = np.expand_dims(frame1,axis=0)
		frame2 = np.expand_dims(frame2,axis=0)
		return frame1,frame2

	def blobFinder(self,frame):
#		frame = frame.astype('int8')
		mask = np.zeros((224,224),dtype = 'uint8')
		cv2.rectangle(mask,(20,20),(204,204),(255,255,255),-1)
		blur = cv2.GaussianBlur(frame,(5,5),0)
#		frame = frame.astype('int8')
		threshed = cv2.threshold(blur,7,255,cv2.THRESH_BINARY)[1]
#		threshed = threshed.astype('uint8')
		output = cv2.bitwise_and(threshed,mask,mask = None)
#		print(output.dtype)
		contours,hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		output = cv2.cvtColor(output,cv2.COLOR_GRAY2BGR)
		if len(contours) != 0:
			cv2.drawContours(output,contours,-1,255,3)
			c = max(contours,key = cv2.contourArea)
			try:
				ellipse = cv2.fitEllipse(c)
				cv2.ellipse(output,ellipse,(0,255,0),2)
			except:
				pass
		return output
	
	def blobEllipse(self,frame):
#		frame = frame.astype('int8')
		mask = np.zeros((224,224),dtype = 'uint8')
		cv2.rectangle(mask,(20,20),(204,204),(255,255,255),-1)
		blur = cv2.GaussianBlur(frame,(5,5),0)
		threshed = cv2.threshold(blur,7,255,cv2.THRESH_BINARY)[1]
		output = cv2.bitwise_and(threshed,mask,mask = None)
		contours,hierarchy = cv2.findContours(output,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		x = None
		y = None
		MA = None
		ma = None
		angle = None
		if len(contours) != 0:
			c = max(contours,key = cv2.contourArea)
			try:
				(x,y),(MA,ma),angle = cv2.fitEllipse(c)
			except:
				pass
		return np.array([[x],[y],[MA],[ma],[angle]])

	def stop(self):
		self.stopped = True

