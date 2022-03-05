# This code is subscribed to the Topic Actuators
# which based on the values control the actuators respectively

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) # to disable GPIO warnings at run time
conveyorPIN = 17
sorterPIN = 22

GPIO.setmode (GPIO.BCM)
GPIO.setup (conveyorPIN, GPIO.OUT)
GPIO.setup (sorterPIN, GPIO.OUT)

conveyorPWM = GPIO.PWM (conveyorPIN, 50) # GPIO 17 as PWM with 50Hz
conveyorPWM.start (0) # initialization
sorterPWM = GPIO.PWM (sorterPIN, 50) # GPIO 22 as PWM with 50Hz
sorterPWM.start (0) # initialization
 
MQTT_SERVER = "localhost"
MQTT_PATH = "Actuators"

conveyor = 0
sorter = 0
whiteBottle = 0
greenBottle = 0
brownBottle = 0
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    client.subscribe(MQTT_PATH)
 

def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))
    global conveyor, sorter, whiteBottle, greenBottle, brownBottle
    
    payloadData = msg.payload.decode('utf-8')
    payloadDataValues = payloadData[1:len(payloadData)-1].split(',')
#    print(payloadDataValues)
    
    conveyor = payloadDataValues[0]
    sorter = payloadDataValues[1]
    
    print("Conveyor :" + conveyor)
    print("Sorter :" + sorter)
    
#    sorter motor control
    sorterAngle = 6
    if(int(sorter) == 30): # left 30
        while(sorterAngle < 8):
            sorterAngle = sorterAngle+2
            sorterPWM.ChangeDutyCycle(sorterAngle)
            time.sleep(0.1)
        time.sleep(2)
        #    conveyor motor control
        conveyorAngle = 5
        if(int(conveyor) == 90):
            while(conveyorAngle < 12): #90-180
                conveyorAngle = conveyorAngle+2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
            while(conveyorAngle > 6): #180-90
                conveyorAngle = conveyorAngle-2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
        else:
            while(conveyorAngle>1): #90-0
                conveyorAngle = conveyorAngle-2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
            while(conveyorAngle < 5): #0-90
                conveyorAngle = conveyorAngle+2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
        while(sorterAngle > 4): # right 30
            sorterAngle = sorterAngle-2
            sorterPWM.ChangeDutyCycle(sorterAngle)
            time.sleep(0.1)
        time.sleep(2)
    elif(int(sorter) == 90):
        while(sorterAngle>1): # right 30
            sorterAngle = sorterAngle-2
            sorterPWM.ChangeDutyCycle(sorterAngle)
            time.sleep(0.1)
        time.sleep(2)
        #    conveyor motor control
        conveyorAngle = 5
        if(int(conveyor) == 90):
            while(conveyorAngle < 12): #90-180
                conveyorAngle = conveyorAngle+2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
            while(conveyorAngle > 6): #180-90
                conveyorAngle = conveyorAngle-2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
        else:
            while(conveyorAngle>1): #90-0
                conveyorAngle = conveyorAngle-2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
            while(conveyorAngle < 5): #0-90
                conveyorAngle = conveyorAngle+2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
        while(sorterAngle < 4): # left 30
            sorterAngle = sorterAngle+2
            sorterPWM.ChangeDutyCycle(sorterAngle)
            time.sleep(0.1)
        time.sleep(2)
    else:
        #    conveyor motor control
        conveyorAngle = 5
        if(int(conveyor) == 90):
            while(conveyorAngle < 12): #90-180
                conveyorAngle = conveyorAngle+2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
            while(conveyorAngle > 6): #180-90
                conveyorAngle = conveyorAngle-2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
        else:
            while(conveyorAngle>1): #90-0
                conveyorAngle = conveyorAngle-2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)
            while(conveyorAngle < 5): #0-90
                conveyorAngle = conveyorAngle+2
                conveyorPWM.ChangeDutyCycle(conveyorAngle)
                time.sleep(0.1)
            time.sleep(2)       

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
