import paho.mqtt.client as mqtt
from sensorData import sensorData
from Pupil_Tracker import Pupil_Tracker
from multi_tflite import multi_tflite
import threading
import cv2
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score

import time
global sensor
sensor = sensorData()
pupil_model_dir = '../../Downloads/model_edgetpu_25.tflite'
point_model_dir = '../../Downloads/point_model_edgetpu.tflite'
model =  multi_tflite(ellipse_model = pupil_model_dir,point_model = point_model_dir)

startSensorCalib = False
stopSensorCalib = False
startCheckImage  = False
stopCheckImage = False
startPointCalib = False
stopPointCalib = False
startRecording = False
stopRecording = False
sendData = False
stopData = False
startShiftCalib = False
stopShiftCalib = False
def on_connect(client,user,flags,rc):
	client.subscribe("data")
	
def on_message(client,userdata,message):
	info = message.payload.decode()
	print(info)
	
	global startSensorCalib
	global stopSensorCalib
	global startCheckImage
	global stopCheckImage
	global startPointCalib
	global stopPointCalib
	global sendData
	global stopData
	global startRecording
	global stopRecording
	global startShiftCalib
	global stopShiftCalib
	if(str(info) == "startCalib"):
		startSensorCalib = True

	if(str(info) == "stopCalib"):
		stopSensorCalib = True
		sensor.stopInitializingEuler = True
	if(str(info) == "startCheckeye"):
		
		startCheckImage = True
		
	if(str(info) == "stopCheckeye"):
		stopCheckImage = True
	if(str(info) == "startRecording"):
		startRecording = True
	if(str(info) == "stopRecording"):
		stopRecording = True
	if(str(info) == "startCalibPoint"):
		startPointCalib = True
		stopPointCalib = False
	if(str(info) == "stopCalibPoint"):
		stopPointCalib = True
		startPointCalib = False
	if(str(info) == "startShiftCalib"):
		startShiftCalib = True
	if(str(info) == "stopShiftCalib"):
		stopShiftCalib = True
	if(str(info) == "sendData"):
		sendData = True
	if(str(info) == "stopData"):
		stopData = True

broker_address = "localhost"
client = mqtt.Client()
client.connect(broker_address)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

print('Waiting to Calibrate IMU/GPS ... Press Q to start')

while(startSensorCalib == False):
	pass
print('Starting IMU Calibration')
sensor.getInitialEuler()

print('Check Eye Image')

while(startCheckImage == False):
	pass

print('Starting Pupil Check')

p = Pupil_Tracker()
p.daemon = True
p.start()

while(stopCheckImage == False):
	frame1, frame2 = p.read()
	frame1_pic,_ = p.blobFinder(model.predict_img(frame1))
	frame2_pic,_ = p.blobFinder(model.predict_img(frame2))
	cv2.imshow('Predicted_F1',frame1_pic)
	cv2.imshow('Predicted_F2',frame2_pic)
	cv2.imshow('raw_f1',frame1)
	cv2.imshow('raw_f2',frame2)
	cv2.waitKey(1)

cv2.destroyAllWindows()
print('Done Pupil Check')

t_data = threading.Thread(target = sensor.getData, args=())
t_data.daemon = True
t_data.start()

while(startPointCalib==False):
	pass
print('Starting Calibration')
initialQuaternion = None
while(stopPointCalib == False):
	if(initialQuaternion is None):
		initialQuaternion = sensor.quaternion
	else:
		initialQuaternion = np.vstack((initialQuaternion,sensor.quaternion))
print(initialQuaternion.shape)
initialQuaternion = np.mean(initialQuaternion,axis=0)
print(initialQuaternion)
print('Finished Calibration')


while(startShiftCalib ==False):
	pass
print("Starting Shift Calib")
bias_pred = None
while(stopShiftCalib == False):
	frame1,frame2 = p.read()
	frame1_ellipse = p.blobEllipse(model.predict_img(frame1))
	frame2_ellipse = p.blobEllipse(model.predict_img(frame2))
	quaternion = sensor.quaternion - initialQuaternion
	frame1_ellipse = np.hstack((frame1_ellipse[0,0:2],frame1_ellipse[0,4])).reshape((1,3))
	frame2_ellipse = np.hstack((frame2_ellipse[0,0:2],frame2_ellipse[0,4])).reshape((1,3))
	input_arr = np.hstack((frame1_ellipse,frame2_ellipse,quaternion.reshape((1,4))))
	output_arr = model.predict_point(input_arr)
	pred = output_arr.reshape((1,2))
	if(bias_pred is None):
		bias_pred = pred - np.array([1920/2,1080/2])
bias_pred = np.mean(bias_pred,axis=0)
#linear_model = LinearRegression()
#linear_model.fit(rawData,trueData)
#pr = linear_model.predict(rawData)
#print(accuracy_score(pr,trueData))

print("Press Q to start recording")
while(sendData == False):
	pass
print("Starting Real Time")
while(stopData == False):
	frame1,frame2 = p.read()
	frame1_ellipse = p.blobEllipse(model.predict_img(frame1))
	frame2_ellipse = p.blobEllipse(model.predict_img(frame2))
#	euler = sensor.euler
	quaternion = sensor.quaternion - initialQuaternion
	frame1_ellipse = np.hstack((frame1_ellipse[0,0:2],frame1_ellipse[0,4])).reshape((1,3))
	frame2_ellipse = np.hstack((frame2_ellipse[0,0:2],frame2_ellipse[0,4])).reshape((1,3))
	input_arr = np.hstack((frame1_ellipse,frame2_ellipse,quaternion.reshape((1,4))))
	output_arr = model.predict_point(input_arr)
	pred = output_arr.reshape((1,2))
#	pred = linear_model.predict(output_arr)
#	pred = pred - bias_pred
	client.publish("data",str(pred[0][0]) + ","+str(pred[0][1]))


