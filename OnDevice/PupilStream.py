import cv2
from threading import Thread


class PupilStream:
    def __init__(self,src1=-1):
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
        self.stopped = False
        while (self.grabbed1 == False or self.grabbed2 == False):
            (self.grabbed1, self.frame1) = self.stream1.read()
            (self.grabbed2, self.frame2) = self.stream2.read()

    def start(self):
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        while (True):
            if self.stopped:
                return

            (self.grabbed1, frame1) = self.stream1.read()
            (self.grabbed2, frame2) = self.stream2.read()
            while (self.grabbed1 == False or self.grabbed2 == False):
                (self.grabbed1, frame1) = self.stream1.read()
                (self.grabbed2, frame2) = self.stream2.read()
            self.frame1 = frame1
            self.frame2 = frame2

    def read(self):
        frame1 = self.frame1
        frame2 = self.frame2
        return

    def stop(self):
        self.stopped = True
        self.stream1.release()
        self.stream2.release()
