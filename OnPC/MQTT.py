import paho.mqtt.client as mqtt
import time
class MQTT:
    def __init__(self,Desktop_IP,RPI_IP,topic):
        self.locahost = Desktop_IP
        self.rpiIP = RPI_IP
        self.topic = topic
        self.client = mqtt.Client()
        self.client.connect("localhost")

    def publish(self,message):
        self.client.publish(self.topic,message)

    def getClient(self):
        return self.client

    def on_connect(self,userdata,flags,rc):
        print("Connected with result code" + str(rc))
        self.client.subscribe(self.topic)

    # def on_message(self,userdata,msg):
        ,