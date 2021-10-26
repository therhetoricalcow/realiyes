import paho.mqtt.client as mqtt
from pynput import keyboard
import os.path
from os import path
import Mouse_Gui
import cv2
m = Mouse_Gui.Mouse_Gui(1920,1080)
i = 0
from tkinter import *

win = Tk()
doneRecording = False
realtime = False
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

        if(i == 1):
            client.publish("data","startCalib")
        if(i == 2):
            client.publish("data","stopCalib")
        if(i == 3):
            client.publish("data","startCheckeye")
        if(i == 4):
            client.publish("data","stopCheckeye")
        if(i==5):
            client.publish("data","startCalibPoint")
            m.startCalibPoint = True
        if(i==6):
            client.publish("data","stopCalibPoint")
            m.stopCalibPoint = True
        if (i == 7):
            client.publish("data", "startShiftCalib")
            m.startCalibPoint = True
        if (i == 8):
            client.publish("data", "stopShiftCalib")
            m.stopCalibPoint = True

        if(i ==9):
            client.publish("data","sendData")
        if(i == 10):
            client.publish("data","stopData")



def on_connect(client, user, flags, rc):
    client.subscribe("data")

def on_message(client, userdata, message):
    info = message.payload.decode()
    try:
        info = str(info)
        num = info.split(",")
        m.pointx = int(float(num[0]))
        m.pointy = int(float(num[1]))
    except:
        pass

broker_address = "192.168.0.23"
client = mqtt.Client()
client.connect(broker_address)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()
listener = keyboard.Listener(on_press=on_press)
listener.start()

while(i < 4):
    pass

m.centerBox()
m.centerBox()
cv2.destroyAllWindows()
while(i<=8):
    pass

m.realtimebox()
