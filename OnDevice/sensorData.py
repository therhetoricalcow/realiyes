import pickle
import numpy as np
import board
import busio
import adafruit_bno055
import os
##from gps import *
import time
import threading

class sensorData:
	def __init__(self):
		i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_bno055.BNO055_I2C(i2c)
#		self.gpsd = gps(mode=WATCH_ENABLE)
		self.Coord = None
		self.initialEuler = np.array([[None],[None],[None]])
		self.euler = None
		self.compAccel = None
		self.linAccel = None
		self.quaternion = None
		self.stopRecording = False
		self.initialCoord = None
		self.stopInitializingEuler = False
		self.initialEulerPrint = True
		self.calibrationValues = np.array([None,None,None,None])
		with open('calib.pickle','rb') as f:
			off_acc,off_mag,off_gyro,rad_acc,rad_mag = pickle.load(f)
		self.sensor.mode = adafruit_bno055.CONFIG_MODE
		self.sensor._write_register(0x55,off_acc)
		self.sensor._write_register(0x5B,off_mag)
		self.sensor._write_register(0x61,off_gyro)
		self.sensor._write_register(0x67,rad_acc)
		self.sensor._write_register(0x69,rad_mag)
		self.sensor.mode = adafruit_bno055.NDOF_MODE
	def getInitialEuler(self):
		print("Started")
		while(self.stopInitializingEuler == False):
			a,b,c = self.sensor.euler
#			print(a,b,c)
			if(self.initialEuler.any() == None and a != None):
#				self.initialCoord = np.array([[self.gpsd.fix.latitude*111139],[self.gpsd.fix.latitude*111139],[self.gpsd.fix.altitude]])
				self.initialEuler = np.array([[a],[b],[c]])*(np.pi/180)
			if(a != None):
#				self.initialCoord = np.hstack((self.initialCoord,np.array([[self.gpsd.fix.latitude*111139],[self.gpsd.fix.longitude*111139],[self.gpsd.fix.altitude]]))
				self.initialEuler = np.hstack((self.initialEuler,np.array([[a],[b],[c]])*(np.pi/180)))
		
			sys,gyro,mag,accel = self.sensor.calibration_status
			self.calibrationValues = np.array([sys,gyro,mag,accel])
			print(self.calibrationValues)
		print('Finished Initializing Euler/GPS')
		self.inititalEuler = np.mean(self.initialEuler[-50:],axis = 1)
#		self.initialCoord = np.mean(self.initialCoord[-100:],axis = 1)
	def calibrate(self):
#		start = time.time()
#		while(time.time() - start < t_take):
#			print(self.sensor.euler)
#			print(self.sensor.calibration_status)
		self.sensor.mode = adafruit_bno055.CONFIG_MODE
		off_acc = self.sensor._read_register(0x55)
		off_mag = self.sensor._read_register(0x5B)
		off_gyro = self.sensor._read_register(0x61)
		rad_acc = self.sensor._read_register(0x67)
		rad_mag = self.sensor._read_register(0x69)
		self.sensor.mode = adafruit_bno055.NDOF_MODE
		with open('calib.pickle','wb') as f:
			pickle.dump([off_acc,off_mag,off_gyro,rad_acc,rad_mag], f)
	
	def getCalibrate(self):
		with open('calib.pickle','rb') as f:
			off_acc,off_mag,off_gyro,rad_acc,rad_mag = pickle.load(f)
		self.sensor.mode = adafruit_bno055.CONFIG_MODE
		self.sensor._write_register(0x55,off_acc)
		self.sensor._write_register(0x5B,off_mag)
		self.sensor._write_register(0x61,off_gyro)
		self.sensor._write_register(0x67,rad_acc)
		self.sensor._write_register(0x69,rad_mag)
		self.sensor.mode = adafruit_bno055.NDOF_MODE
		while(True):
			print(self.sensor.euler)
			print(self.sensor.calibration_status)
	def getData(self):
		while(self.stopRecording == False):

			qa,qb,qc,qd = self.sensor.quaternion
			a,b,c = self.sensor.euler
			linAccel = self.sensor.linear_acceleration
#			print(qa,qb,qc,qd)
#			print(a,b,c)
#			print(linAccel)
			if(qa is not None and qb is not None and qc is not None and qd is not None and a is not None and b is not None and c is not None and linAccel[0] is not  None and linAccel[1] is not None and linAccel[2] is not None):

				self.linAccel = np.array([[linAccel[0]],[linAccel[1]],[linAccel[2]]])
				self.euler = np.array([[a,b,c]])
				self.quaternion = np.array([[qa,qb,qc,qd]])
#				print(self.euler)
#				print(self.sensor.calibration_status)
				a = a*(np.pi/180)
				b = b*(np.pi/180)
				c = c*(np.pi/180)

				Rz = np.array([[np.cos(-c),-np.sin(-c),0],[np.sin(-c),np.cos(-c),0],[0,0,1]])
				Ry = np.array([[np.cos(-b),0,-np.sin(-b)],[0,1,0],[np.sin(-b),0,np.cos(-b)]])
				Rx = np.array([[1,0,0],[0,np.cos(-a),-np.sin(-a)],[0,np.sin(-a),np.cos(-a)]])
				self.compAccel =  Rz @ Ry @ Rx @ self.linAccel
#			self.Coord = np.array([[self.gpsd.fix.latitude*111139],[self.gpsd.fix.longitude*111139],[self.gpsd.fix.altitude]]) - self.initialCoord
			else:
				pass
