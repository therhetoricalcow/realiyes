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
		self.inititalEuler = None
		self.euler = None
		self.compAccel = None
		self.linAccel = None
		self.stopRecording = False
		self.initialCoord = None
	def getInititalEuler(self,t_take):
		start = time.time()
		while(time.time() - start < t_take):
			a,b,c = self.sensor.euler
			if(self.inititalEuler = None and a != None):
#				self.initialCoord = np.array([[self.gpsd.fix.latitude*111139],[self.gpsd.fix.latitude*111139],[self.gpsd.fix.altitude]])
				self.initialEuler = np.array([[a],[b],[c]])*(np.pi/180)
			if(a != None):
#				self.initialCoord = np.hstack((self.initialCoord,np.array([[self.gpsd.fix.latitude*111139],[self.gpsd.fix.longitude*111139],[self.gpsd.fix.altitude]]))
				self.inititalEuler = np.hstack((self.initialEuler,np.array([[a],[b],[c]])*(np.pi/180)))
			print(self.sensor.calibration_status)
			
		self.inititalEuler = np.mean(self.initialEuler[-50:],axis = 1)
#		self.initialCoord = np.mean(self.initialCoord[-100:],axis = 1)
	def getData(self):
		while(self.stopRecording == False):
			a,b,c = self.sensor.euler
			a = a*(np.pi/180)
			b = b*(np.pi/180)
			c = c*(np.pi/180)
			self.euler = np.array([[a],[b],[c]]) - self.initialEuler
			linAccel = self.sensor.linear_acceleration
			self.linAccel = np.array([[linAccel[0]],[linAccel[1]],[linAccel[2]]])
			Rz = np.array([[np.cos(-c),-np.sin(-c),o],[np.sin(-c),np.cos(-c),0],[0,0,1]])
			Ry = np.array([[np.cos(-b),0,-np.sin(-b)],[0,1,0],[np.sin(-b),0,np.cos(-b)]])
			Rx = np.array([[1,0,0],[0,np.cos(-a),-np.sin(-a)],[0,np.sin(-a),np.cos(-a)]])
			R = Rz @ Ry @ Rx
			self.compAccel = R @ self.linAccel
#			self.Coord = np.array([[self.gpsd.fix.latitude*111139],[self.gpsd.fix.longitude*111139],[self.gpsd.fix.altitude]]) - self.initialCoord
