import time
from Pupil_Tracker import Pupil_Tracker
import cv2
from tflite_model import tflite_model

model = tflite_model(model_file='/home/pi/Downloads/model_edgetpu_25.tflite')

p = Pupil_Tracker()
p.start()
start = time.time()
i = 0
while(True):
	raw_frame1,raw_frame2 = p.read()
#	frame1,frame2 = p.preprocess()
	frame1_ellipse,ellipse1 = p.blobFinder(model.predict(raw_frame1))
	frame2_ellipse,ellipse2 = p.blobFinder(model.predict(raw_frame2))
	print(ellipse1)
	print(ellipse2)
	cv2.imshow("Predicted_Frame1",frame1_ellipse)
	cv2.imshow("Predicted_Frame2",frame2_ellipse)
	cv2.imshow("RAW Frame1",raw_frame1)
	cv2.imshow("RAW Frame2",raw_frame2)
	cv2.waitKey(1)
	i = i+1
	print(i/(time.time() - start))
