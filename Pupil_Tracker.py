from threading import Thread
import cv2
import numpy as np
import tensorflow as tf
import PIL
class Pupil_Tracker:
    def __init__(self,src = 0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        while(self.grabbed == False):
            (self.grabbed, self.frame) = self.stream.read()
    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed,self.frame) = self.stream.read()

    def read(self):
        return self.frame


    def preprocess(self,frame):
        frame = cv2.resize(frame,(224,224))
        frame = frame.astype('float32')/255.0
        frame = np.expand_dims(frame,axis=0)
        return frame

    def predict(self,frame):
        self.interpreter.set_tensor(self.input_details[0]['index'],frame)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        output_data = np.sqeeze(output_data)
        return output_data

    def stop(self):
        self.stopped = True

