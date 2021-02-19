import paho.mqtt.client as mqtt
from sensorData import sensorData
from Pupil_Tracker import Pupil_Tracker
from tflite_model import tflite_model
import threading
import cv2
import numpy as np
import time


global sensor
sensor = sensorData()
p = Pupil_Tracker(src1 =-1,src2 =2)
model = tflite_model(model_file='../../Downloads/model_edgetpu_25.tflite')
p.start()

startSensorCalibration = False
stopSensorCalibration = False
startHeadMountCalibration = False
stopHeadMountCalibration = False
startRecording = False
stopRecording = False
endCalibration = False
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
	if(str(info) == '1'): ##Start Sensor Calibration
		startSensorCalibration = True
	if(str(info) == '2'): ## Stop Sensor Calibration
		stopSensorCalibration = True
		sensor.stopInitializingEuler = True
	if(str(info) == '3'): ## Start Head Mount Calibration
		startHeadMountCalibration = True
		sensor.stopInitializingEuler = False
		sensor.initialEulerPrint = False
	if(str(info) == '4'): ##Stop Head Mount Calibration
		stopHeadMountCalibration = True
		sensor.stopInitializingEuler = True
	if(str(info) == '5'): ## Start Recording
		startRecording = True
	if(str(info) == '6'): ## Stop Recording
		stopRecording = True

broker_address = 'localhost'
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
print("Secure to Face and Press Q to Start Calibrating Head Mount")
while(startHeadMountCalibration == False):
	pass
print('Starting Head Mount Calibration')
t = threading.Thread(target=sensor.getInitialEuler, args=())
t.daemon = True
t.start()
p.daemon = True
p.start()
initialCoord1 = np.array([None])
initialCoord2 = np.array([None])
while(stopHeadMountCalibration == False):
#	print('Starting CAmeras')
	frame1,frame2 = p.preprocess()
	frame1_pic,frame1_ellipse = p.blobFinder(model.predict(frame1))
	frame2_pic,frame2_ellipse = p.blobFinder(model.predict(frame2))
	cv2.imshow('Predicted_F1',frame1_pic)
	cv2.waitKey(1)
	cv2.imshow('Predicted_F2',frame2_pic)
	cv2.waitKey(1)
	if(initialCoord1.any() == None):
		initialCoord1 = np.array([[frame1_ellipse[0]],[frame1_ellipse[1]]])
		initialCoord2 = np.array([[frame2_ellipse[0]],[frame2_ellipse[1]]])
	else:
		initialCoord1 = np.hstack((initialCoord1,np.array([[frame1_ellipse[0]],[frame1_ellipse[1]]])))
		initialCoord2 = np.hstack((initialCoord2,np.array([[frame2_ellipse[0]],[frame2_ellipse[1]]])))
initialCoord1 = np.mean(initialCoord1,axis = 1)
initialCoord2 = np.mean(initialCoord2, axis = 1)
cv2.destroyAllWindows()
print('Done Calibration')
t.join()
print('Waiting to Start Recording... Press Q to Start...Follow Tracer')
while(startRecording == False):
	pass
print('Starting Recording')
t_data =threading.Thread(target=sensor.getData, args=()) 
t_data.daemon = True
t_data.start()
data = None
start = time.time()
while(stopRecording == False):
	frame1,frame2 = p.preprocess()
	frame1_ellipse = p.blobEllipse(model.predict(frame1))
	frame2_ellipse = p.blobEllipse(model.predict(frame2))
	frame1_ellipse[0] = frame1_ellipse[0] - initialCoord1[0]
	frame1_ellipse[1] = frame1_ellipse[1] - initialCoord1[1]
	frame2_ellipse[0] = frame2_ellipse[0] - initialCoord2[0]
	frame2_ellipse[1] = frame2_ellipse[1] - initialCoord2[1]
	print(frame1_ellipse.shape)
	euler = sensor.euler
	print(euler.shape)
	linAccel = sensor.linAccel
	print(linAccel.shape)
	compAccel = sensor.compAccel
	print(compAccel.shape)
	i = np.array([time.time() - start])
	if(data == None):
		data = np.vstack((i,frame1_ellipse,frame2_ellipse,euler,linAccel,compAccel))
	else:
		arry = np.vstack((i,frame1_ellipse,frame2_ellipse,euler,linAccel,compAccel))
		data = np.hstack((data,arry))

t_data.join()
p.stop()
print('Finished Recording')
np.savetxt("/home/pi/Desktop/Recordings/data.csv",np.transpose(data),delimiter = ",")

