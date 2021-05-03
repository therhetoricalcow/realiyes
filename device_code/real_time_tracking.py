import paho.mqtt.client as mqtt
from sensorData import sensorData
from Pupil_Tracker import Pupil_Tracker
from multi_tflite import multi_tflite
import threading
import cv2
import numpy as np
import os
from sklearn.linear_model import LinearRegression

global sensor
sensor = sensorData()
pupil_model_dir = '../../Downloads/model_edgetpu_25.tflite'
point_model_dir = '../../Downloads/point_model_edge.tflite'
model =  multi_tflite(ellipse_model = pupil_model_dir,point_model = point_model_dir)

startSensorCalib = False
stopSensorCalib = False
startCheckImage  = False
stopCheckImage = False
startPointCalib = False
stopPointCalib = False
sendData = False
stopData = False
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
	if(str(info) == "startCalib"):
		startSensorCalib = True

	if(str(info) == "stopCalib"):
		stopSensorCalib = True
		sensor.stopInitializingEuler = True
	if(str(info) == "startCheckeye"):
		startCheckImage = True
	if(str(info) == "stopCheckeye"):
		stopCheckImage = True
	if(str(info) == "startPointCalib"):
		startPointCalib = True
		stopPointCalib = False
	if(str(info) == 'stopPointCalib'):
		stopPointCalib = True
		startPointCalib = False
	if(str(info) == 'sendData'):
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

t = threading.Thread(targeet=sensor.getInitialEuler, args = ())
t.daemon = True
t.start()
p = Pupil_Tracker()
p.daemon = True
p.start()

while(stopCheckImage = False):
	frame1, frame2 = p.read()
	frame1_pic,_ = p.blobFinder(model.predict_img(frame1))
	frame2_pic,_ = p.blobFinder(model.predict_img(frame2))
	cv2.imshow('Predicted_F1',frame1_pic)
	cv2.imshow('Predicted_F2',frame2_pic)
	cv2.waitKey(1)

cv2.destroyAllWindows()
print('Done Pupil Check')

t.join()

calibNum = 1
calibPath = '/home/pi/Desktop/Recordings/calibrations/' + str(calibNum) + '/'
while(os.path.exists(calibPath) == True):
	calibNum = 1 + calibNum
	calibPath = '/home/pi/Desktop/Recordings/calibrations/' + str(calibNum) + '/'
os.mkdir(calibPath)
print('Calib Folder Created')
t_data = threading.Thread(target = sensor.getData, args())
t_data.daemon = True
t_data.start()
rawData = np.array([None])
trueData = np.array([None])
points = np.array([[120,120],[120,1200-120],[1920-120,120],[1920-120,1200-120]])
print('Waiting to Start Point Calibration')
while(startPointCalib == False):
	pass


print('Starting Calibration')
pointNum = 0
while(sendData == False)
	frame1,frame2 = p.read()
	frame1_ellipse = p.blobEllipse(model.predict_img(frame1))
	frame2_ellipse = p.blobEllipse(model.predict_img(frame2))
	euler = sensor.euler
	quaternion = sensor.quaternion
	input_arr = np.hstack((frame1_ellipse,frame2_ellipse,quaternion,euler))
	output_arr = model.predict_point(input_arr)
	output_arr = output_arr.reshape((1,2))
	if(rawData.any() == None and startPointCalib == True and trueData.any() = None):
		rawData = output_arr
		trueData = np.array([points[pointNum]])
	elif(startPointCalib == True):
		arr = output_arr
		rawData = np.vstack((rawData,arr))
		trueData = np.vstack((trueData,np.array([points[pointNum]])))
	elif(stopPointCalib == True):
		print(rawData.shape)
		pointNum = pointNum + 1
	else:
		pass


print('Finished Calibration')

linear_model = LinearRegression()
linear_model.fit(rawData,trueData)


while(stopData == False):
	frame1,frame2 = p.read()
	frame1_ellipse = p.blobEllipse(model.predict_img(frame1))
	frame2_ellipse = p.blobEllipse(model.predict_img(frame2))
	euler = sensor.euler
	quaternion = sensor.quaternion 
	input_arr = np.hstack((frame1_ellipse,frame2_ellipse,quaternion,euler))
	output_arr = model.predict_point(input_arr)
	output_arr = output_arr.reshape((1,2))
	pred = linear_model.predict(output_arr)
	client.publish("data",str(pred[0]) + ","+str(pred[1]))


