import paho.mqtt.client as mqtt
from sensorData import sensorData
from Pupil_Tracker import Pupil_Tracker
from tflite_model import tflite_model
import threading
import cv2
import numpy as np
import time
import os.path
from os import path


global sensor
sensor = sensorData()
model = tflite_model(model_file='../../Downloads/model_edgetpu_25.tflite')

startSensorCalibration = False
stopSensorCalibration = False
startHeadMountCalibration = False
stopHeadMountCalibration = False
startRecording = False
stopRecording = False
endCalibration = False
startDataTake = False
stopDataTake = False
startCalibPoint = False
stopCalibPoint = False

def on_connect(client,user,flags,rc):
	client.subscribe("record")

def on_message(client,userdata,message):
	info = message.payload.decode()
	print(info)
	global startSensorCalibration
	global stopSensorCalibration
	global startHeadMountCalibration
	global stopHeadMountCalibration
	global startRecording
	global stopRecording
	global endCalibration
	global sensor
	global startDataTake
	global stopDataTake
	global startCalibPoint
	global stopCalibPoint
	if(str(info) == 'startCalib'): ##Start Sensor Calibration
		startSensorCalibration = True
	if(str(info) == 'stopCalib'): ## Stop Sensor Calibration
		stopSensorCalibration = True
		sensor.stopInitializingEuler = True
	if(str(info) == 'startCheckeye'): ## Start Head Mount Calibration
		startHeadMountCalibration = True
	if(str(info) == 'stopCheckeye'): ##Stop Head Mount Calibration
		stopHeadMountCalibration = True
	if(str(info) == "startCalibPoint"):
		startCalibPoint = True
	if(str(info) == "stopCalibPoint"):
		stopCalibPoint = True
	if(str(info) == 'startRecording'): ## Start Recording
		startRecording = True
	if(str(info) == 'start'):
		startDataTake = True
		stopDataTake = False
	if(str(info) == 'stop'):
		stopDataTake = True
		startDataTake = False
	if(str(info) == '6'): ## Stop Recording
		stopRecording = True

broker_address = "localhost"
client = mqtt.Client()
client.connect(broker_address)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

print('Waiting to Start Calibrating IMU/GPS... Press Q to start')

while(startSensorCalibration == False):
	pass
print("Starting Sensor Calibration... Keep Still on a Surface... Press Q after everything is finished")

sensor.getInitialEuler()
sensor.calibrate()
print("Finished Calibration")

print("Secure to Face and Press Q to Start Calibrating Head Mount")
while(startHeadMountCalibration == False):
	pass
print('Starting Head Mount Calibration')

p = Pupil_Tracker()
p.daemon = True
p.start()

while(stopHeadMountCalibration == False):
#	print('Starting CAmeras')
	frame1,frame2 = p.read()
	frame1_pic,_ = p.blobFinder(model.predict(frame1))
	frame2_pic,_ = p.blobFinder(model.predict(frame2))
	cv2.imshow('Predicted_F1',frame1_pic)
#	cv2.waitKey(1)
	cv2.imshow('Predicted_F2',frame2_pic)
#	euler = sensor.euler
#	print(np.hstack((quaternion,euler))) 
	cv2.waitKey(1)

print("Finished Eye Check")

initialQuaternion = np.array([None,None,None,None])
t_data = threading.Thread(target=sensor.getData,args = ())
t_data.daemon = True
t_data.start()

while(startCalibPoint == False):
	pass
while(stopCalibPoint == False):
	if(initialQuaternion.any() == None):
		initialQuaternion = sensor.quaternion
	else:
		initialQuaternion = np.vstack((initialQuaternion,sensor.quaternion))
#	if(initialCoord1.any() == None):
#		initialCoord1 = np.array([[frame1_ellipse[0]],[frame1_ellipse[1]]])
#		initialCoord2 = np.array([[frame2_ellipse[0]],[frame2_ellipse[1]]])
#	else:
#		initialCoord1 = np.hstack((initialCoord1,np.array([[frame1_ellipse[0]],[frame1_ellipse[1]]])))
#		initialCoord2 = np.hstack((initialCoord2,np.array([[frame2_ellipse[0]],[frame2_ellipse[1]]])))
#initialCoord1 = np.mean(initialCoord1,axis = 1)
#initialCoord2 = np.mean(initialCoord2, axis = 1)
cv2.destroyAllWindows()
print(initialQuaternion.shape)
initialQuaternion = np.mean(initialQuaternion,axis=0)
print(initialQuaternion)
print('Done Calibration')



print('Waiting to Start Recording... Press Q to Start...Follow Tracer')
while(startRecording == False):
	pass
print('Starting Recording')
dirNum = 1
dirPath = '/home/pi/Desktop/Recordings/' + str(dirNum) + '/'
while(path.exists(dirPath) == True):
	dirNum = dirNum + 1
	dirPath = '/home/pi/Desktop/Recordings/' + str(dirNum) + '/'
os.mkdir(dirPath)
print("Folder Created")

t_data =threading.Thread(target=sensor.getData, args=()) 
t_data.daemon = True
t_data.start()
data = np.array([None])
start = time.time()
j = 1

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (224, 224))

while(stopRecording == False):
	frame1,frame2 = p.read()
	
#	frame1_ellipse = p.blobEllipse(model.predict(frame1))
#	frame2_ellipse = p.blobEllipse(model.predict(frame2))
#	frame1_ellipse[0] = frame1_ellipse[0] - initialCoord1[0]
#	frame1_ellipse[1] = frame1_ellipse[1] - initialCoord1[1]
#	frame2_ellipse[0] = frame2_ellipse[0] - initialCoord2[0]
#	frame2_ellipse[1] = frame2_ellipse[1] - initialCoord2[1]
#	print(frame1_ellipse.shape)
	euler = sensor.euler
	quaternion = sensor.quaternion - initialQuaternion
#	print(euler.shape)
	linAccel = sensor.linAccel
#	print(linAccel.shape)
	compAccel = sensor.compAccel
#	print(compAccel.shape)
	if(data.any() ==  None and startDataTake == True):
		
		data = quaternion
		k = 1
		os.mkdir(dirPath + str(j))
		videoPath = dirPath + str(j) + '/videos/'
		sensPath = dirPath + str(j) + '/recording/'
		os.mkdir(videoPath)
		os.mkdir(sensPath)
		frame1Path = imgPath + 'frame1/'
		frame2Path = imgPath + 'frame2/'
		os.mkdir(frame1Path)
		os.mkdir(frame2Path)
		cv2.imwrite(frame1Path + str(k) +'.png',frame1)
		cv2.imwrite(frame2Path + str(k) +'.png',frame2)
		
	elif(startDataTake == True):
		k = k + 1
		cv2.imwrite(frame1Path + str(k) + '.png',frame1)
		cv2.imwrite(frame2Path + str(k) + '.png',frame2)
		
		arry = quaternion
		data = np.vstack((data,arry))

	elif(stopDataTake == True):
		
		recPath = sensPath + str(j) + '.csv'
		np.savetxt(recPath,np.transpose(data),delimiter = ",")
		stopDataTake = False
		print("Wrote " + str(j) + ".csv")
		print(data.shape)
		data = np.array([None])
		j = j + 1
	else:
		pass

t_data.join()
p.stop()
recPath = dirpath + str(j) + '.csv'
np.savetxt(recPath,np.transpose(data),delimiter = ",")
print("Finished Recording")
