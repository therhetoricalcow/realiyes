import paho.mqtt.client as mqtt
from sensorData import sensorData
from Pupil_Camera import Pupil_Camera
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

while(stopHeadMountCalibration == False):
    pass
# #	print('Starting CAmeras')
# 	frame1,frame2 = p.read()
# 	frame1_pic,_ = p.blobFinder(model.predict(frame1))
# 	frame2_pic,_ = p.blobFinder(model.predict(frame2))
# 	cv2.imshow('Predicted_F1',frame1_pic)
# #	cv2.waitKey(1)
# 	cv2.imshow('Predicted_F2',frame2_pic)
# #	euler = sensor.euler
# #	print(np.hstack((quaternion,euler)))
# 	cv2.waitKey(1)


print("Finished Eye Check")

initialQuaternion = np.array([None, None, None, None])
t_data = threading.Thread(target=sensor.getData, args=())
t_data.daemon = True
t_data.start()
while(startCalibPoint == False):
	pass

while(stopCalibPoint == False):
	if(initialQuaternion.any() == None):
		initialQuaternion = sensor.quaternion
	else:
		initialQuaternion = np.vstack((initialQuaternion,sensor.quaternion))

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

t_data =threading.Thread(target=sensor.getQuart(), args=())
t_data.daemon = True

start = time.time()
j = 1
p = Pupil_Camera()
os.mkdir(dirPath + str(j))
imgPath = dirPath + str(j) + '/images/'
sensPath = dirPath + str(j) + '/recording/'
os.mkdir(imgPath)
os.mkdir(sensPath)
frame1Path = imgPath + 'frame1/'
frame2Path = imgPath + 'frame2/'
os.mkdir(frame1Path)
os.mkdir(frame2Path)
p.assignVideoCaps(frame1Path,frame2Path)
p.start()
t_data.start()
newStart = None
while (stopRecording == False):
    quaternion = sensor.quaternion
    #	print(euler.shape)
    # linAccel = sensor.linAccel
    #	print(linAccel.shape)
    # compAccel = sensor.compAccel
    #	print(compAccel.shape)
    if (newStart is None and startDataTake == True):
        newStart = 1
        if(j>1):
            os.mkdir(dirPath + str(j))
            imgPath = dirPath + str(j) + '/images/'
            sensPath = dirPath + str(j) + '/recording/'
            os.mkdir(imgPath)
            os.mkdir(sensPath)
            frame1Path = imgPath + 'frame1/'
            frame2Path = imgPath + 'frame2/'
            os.mkdir(frame1Path)
            os.mkdir(frame2Path)
            p.assignVideoCaps(frame1Path, frame2Path)
            p.start()
            t_data.start()

    elif (stopDataTake == True):
        p.stop()
        data = sensor.quartData
        t_data.join()
        recPath = sensPath + str(j) + '.csv'
        np.savetxt(recPath, np.transpose(data), delimiter=",")
        stopDataTake = False
        print("Wrote " + str(j) + ".csv")
        print(data.shape)
        newStart = None
        j = j + 1
    else:
        pass

data = sensor.quartData
t_data.join()
p.stop()
recPath = dirPath + str(j) + '.csv'
np.savetxt(recPath,np.transpose(data),delimiter = ",")
print("Finished Recording")