import paho.mqtt.client as mqtt
from sensorData import sensorData
from Pupil_Tracker import Pupil_Tracker
from tflite_model import tflite_model


sensor = sensorData()
p = Pupil_Tracker(-1,2)
model = tflite_model(model_file='../../Downloads/model_edgetpu_25.tflite')
p.start()

sensorCalibration = False
cameraCalibration = False
startRecording = False
stopRecording = False
endCalibration = False
def on_connect(client,user,flags,rc):
	client.subscribe("record")

def on_message(client,userdata,message):
	info = message.payload.decode()
	print(info)
	global sensorCalibration
	global cameraCalibration
	global startRecording
	global stopRecording
	global endCalibration
	if(str(info) == 'Start Calibration Sensors'):
		sensorCalibration = True
	if(str(info) == 'Start Calibration Camera'):
		cameraCalibration = True
	if(str(info) == 'End Calibration'):
		endCalibration = True
	if(str(info) == 'Start Recording'):
		startRecording = True
	if(str(info) == 'Stop Recording'):
		stopRecording = True

broker_address = "localhost"
client = mqtt.Client()
client.connect(broker_address)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

while(sensorCalibration == False):
	pass

sensor.getInitialEuler(100)

while(cameraCalibration == False):
	pass
t = threading.Thread(target=sensor.getInitialEuler, args=[100])
t.start()
initialCoord1 = None
initialCoord2 = None
while(endCalibration == False):
	frame1,frame2 = p.preprocess()
	frame1_ellipse = p.blobEllipse(model.predict(frame1))
	frame2_ellipse = p.blobEllipse(model.predict(frame2))
	if(initialCoord1 == None):
		initialCoord1 = np.array([[frame1_ellipse[0]],[frame1_ellipse[1]]])
		initialCoord2 = np.array([[frame2_ellipse[0]],[frame2_ellipse[1]]])
	else:
		initialCoord1 = np.mean(np.hstack((initialCoord1,np.array([[frame1_ellipse[0]],[frame1_ellipse[1]]]))),axis = 1)
		initialCoord2 = np.mean(np.hstack((initialCoord2,np.array([[frame2_ellipse[0]],[frame2_ellipse[1]]]))),axis = 1)

t.join()
while(startRecording == False):
	pass

t_data =threading.Thread(target=sensor.getData, args=()) 
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
	euler = sensor.euler
	linAccel = sensor.linAccel
	compAccel = sensor.compAccel
	i = np.array([time.time() - start])
	if(data == None):
		data = np.vstack((i,frame1_ellipse,frame2_ellipse,euler,linAccel,compAccel))
	else:
		arry = np.vstack((i,frame1_ellipse,frame2_ellipse,euler,linAccel,compAccel))
		data = np.hstack((data,arry))

t_data.join()
np.savetxt("data.csv",data,delimiter = ",")
