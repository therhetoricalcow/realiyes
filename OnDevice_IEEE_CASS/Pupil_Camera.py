from threading import Thread
import cv2
import numpy as np
import PIL
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
		while(self.grabbed1 == False or self.grabbed2 == False):
			(self.grabbed1, self.frame1) = self.stream1.read()
			(self.grabbed2, self.frame2) = self.stream2.read()

	def assignVideoCaps(self,src1,src2):
		self.videocap1 = cv2.VideoWriter(src1,cv2.VideoWriter_fourcc('M','J','P','G'), 20, (self.frame1.shape[1],self.frame1.shape[0]))
		self.videocap2 = cv2.VideoWriter(src2,cv2.VideoWriter_fourcc('M','J','P','G'), 20, (self.frame2.shape[1],self.frame2.shape[0]))

	def start(self):
		Thread(target=self.update,args=()).start()
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
			self.videocap1.write(frame1)
			self.videocap2.write(frame2)

	def stop(self):
		self.videocap1.release()
		self.videocap2.release()
		self.stopped = True