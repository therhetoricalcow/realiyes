import pdb

from threading import Thread
import cv2
import numpy as np
import PIL
import time
class Pupil_Camera:
	def __init__(self):
		src1 = -1
		self.stream1 = cv2.VideoCapture(src1)
		while self.stream1 is None or not self.stream1.isOpened():
			src1 = src1 + 1
			self.stream1 = cv2.VideoCapture(src1)
		src2 = src1 + 1
		self.stream2 = cv2.VideoCapture(src2)
		while self.stream2 is None or not self.stream2.isOpened():
			src2 = src2 + 1
			self.stream2 = cv2.VideoCapture(src2)
		self.stream1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
		self.stream2.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
		(self.grabbed1, self.frame1) = self.stream1.read()
		(self.grabbed2, self.frame2) = self.stream2.read()
		self.videocap1 = None
		self.videocap2 = None
		self.stopped = False
		self.updateThread = None
		self.start_ = 0
		while(self.grabbed1 == False or self.grabbed2 == False):
			(self.grabbed1, self.frame1) = self.stream1.read()
			(self.grabbed2, self.frame2) = self.stream2.read()

	def read(self):
		return self.frame1,self.frame2
	def assignVideoCaps(self,src1,src2):
		print(self.frame1.shape)
		self.videocap1 = cv2.VideoWriter(src1,cv2.VideoWriter_fourcc(*'XVID'), 10, (self.frame1.shape[1],self.frame1.shape[0]))
		self.videocap2 = cv2.VideoWriter(src2,cv2.VideoWriter_fourcc(*'XVID'), 10, (self.frame2.shape[1],self.frame2.shape[0]))

	def start(self):
		self.stopped = False
		self.updateThread = Thread(target=self.update,args=())
		self.start_ = time.time()
		self.j = 1
		self.updateThread.start()
		
		return self

	def update(self):
		
		while(self.stopped== False):
			(self.grabbed1,self.frame1) = self.stream1.read()
			(self.grabbed2,self.frame2) = self.stream2.read()
			while(self.grabbed1 == False or self.grabbed2 == False):
				(self.grabbed1,self.frame1) = self.stream1.read()
				(self.grabbed2,self.frame2) = self.stream2.read()
#			cv2.imshow("f1",self.frame1)
#			cv2.imshow("f2",self.frame2)
#			cv2.waitKey(1)
#			self.videocap1.write(frame1)
#			self.videocap2.write(frame2)
			
	def write(self):
		print(self.j/(time.time()-self.start_))
		self.videocap1.write(self.frame1)
		self.videocap2.write(self.frame2)
		self.j = self.j + 1
	def stop(self):
		self.videocap1.release()
		self.videocap2.release()
		self.stopped = True
		self.updateThread.join()
