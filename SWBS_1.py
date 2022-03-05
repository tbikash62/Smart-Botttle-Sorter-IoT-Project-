# This code is used to read data serially from arduino
# and publish it to the MQTT broker under the topic Sensors

import serial
import paho.mqtt.publish as publish
from time import sleep

# reading from arduino
ser = serial.Serial('/dev/ttyUSB0',9600)

MQTT_SERVER = "localhost"
MQTT_PATH = "Sensors"

s = [0]
data = []
lightSensor = 0
vibrationSensor = 0
colorSensor = 0
whiteBin = 0
greenBin = 0
brownBin = 0

#   read serial data present between '$' 
def readSerialData():
    
    s[0] = ser.readline().decode('utf-8').rstrip()
    if(s[0] == '$'):
        s[0] = ser.readline().decode('utf-8').rstrip()
        while(s[0] != '$'):
            data.append(s[0])
            s[0] = ser.readline().decode('utf-8').rstrip()
        
#   Processing the data

    global lightSensor, vibrationSensor, colorSensor, whiteBin, greenBin, brownBin
    lightSensor = data[0]
    vibrationSensor = data[1]
    colorSensor = data[2]
    whiteBin = data[3]
    greenBin = data[4]
    brownBin = data[5]
    
while True:
    readSerialData()
    payload = str(data)
    print(payload)
    publish.single(MQTT_PATH, payload, hostname=MQTT_SERVER)
    data.clear()
    
    
    