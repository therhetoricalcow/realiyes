import numpy as np
from sensorData import sensorData
import threading

global sensor 
sensor = sensorData()

calib = threading.Thread(target = sensor.getInitialEuler,args = ())
calib.daemon = True
calib.start()


while(sensor.calibrationValues[1]!=3 or sensor.calibrationValues[2]!=3 or sensor.calibrationValues[3]!=3):
	print(sensor.calibrationValues)
	pass

sensor.stopInitializingEuler = True
calib.join()

rec = threading.Thread(target = sensor.getData,args=())
rec.daemon = True
rec.start()


while(True):
	quat = sensor.quaternion
	print(quat)

