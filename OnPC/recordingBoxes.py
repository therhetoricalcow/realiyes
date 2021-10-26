import cv2
import paho.mqtt.client as mqtt
from pynput import keyboard
global i
import os.path
from os import path
import Mouse_Gui
import numpy as np
m = Mouse_Gui.Mouse_Gui(1920,1080)

def on_press(key):
    global i
    if key == keyboard.Key.esc:
            return False
    try:
        k = key.char
    except:
        k = key.name
    print('Key pressed: ' + k)
    if(k == 'q'):
        i = i+1
        print(i)
        if(i == 1):
            client.publish("record","startCalib")
        if(i == 2):
            client.publish("record","stopCalib")
        if(i == 3):
            client.publish("record","startCheckeye")

        if(i == 4):
            client.publish("record","stopCheckeye")

        if(i==5):
            client.publish("record","startCalibPoint")
            m.startCalibPoint = True
        if(i==6):
            client.publish("record","stopCalibPoint")
            m.stopCalibPoint = True
        if(i == 7):
            client.publish("record","startRecording")
        if (i >7):
            if (m.getDataFlags() == (False,False)):
                client.publish("record","start")
                m.startData()
            else:
                client.publish("record","stop")
                m.stopData()



def on_connect(client,user,flags,rc):
    client.subscribe("record")

def on_message(client,userdata,message):
    info = message.payload.decode()
    print(info)

broker_address = "192.168.0.15"
client = mqtt.Client()
client.connect(broker_address)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()
listener = keyboard.Listener(on_press=on_press)
listener.start()
i = 0

recNum = 1
dirpath = '/home/avaneesh/Desktop/Recordings/' + str(recNum) + '/'
while(path.exists(dirpath)==True):
    recNum = recNum + 1
    dirpath = '/home/avaneesh/Desktop/Recordings/' + str(recNum) + '/'

os.mkdir(dirpath)
print("Folder Created")
while(i<4):
    pass

m.centerBox()
cv2.destroyAllWindows()
while(i<=6):
    pass
m.boxRecord(dirpath)

client.publish("record",'6')

