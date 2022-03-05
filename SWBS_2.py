# This code is subscribed to the topic Sensors,whenever
# values get updated it execute the AI Planning and
# publish the result to the topic Actuators and data
# which is used for visualisation is send to the topic
# visualise

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import requests

MQTT_SERVER = "localhost"
MQTT_PATH = "Sensors"
MQTT_PATH2 = "Actuators"
MQTT_PATH3 = "Visualise"

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
    
    global conveyor, sorter, whiteBottle, greenBottle, brownBottle
#    print(msg.topic+" "+str(msg.payload))
    payloadData = msg.payload.decode('utf-8')
#    print(payloadData)
    payloadDataValues = payloadData[1:len(payloadData)-1].split(',')
#    print(payloadDataValues[0][1:len(payloadDataValues)-1])
#    copy data to local variables
    lightSensor = payloadDataValues[0][1:len(payloadDataValues[0])-1]
    vibrationSensor = payloadDataValues[1][2:len(payloadDataValues[1])-1]
    colorSensor = payloadDataValues[2][2:len(payloadDataValues[2])-1]
    whiteBin = payloadDataValues[3][2:len(payloadDataValues[3])-1]
    greenBin = payloadDataValues[4][2:len(payloadDataValues[4])-1]
    brownBin = payloadDataValues[5][2:len(payloadDataValues[5])-1]
    print(lightSensor)
    print(vibrationSensor)
    print(colorSensor)
    print(whiteBin)
    print(greenBin)
    print(brownBin)
    
    # mapping the distance to percentage
    
    whiteBin = (100 - (int(whiteBin) * 20))
    greenBin = (100 - (int(greenBin) * 20))
    brownBin = (100 - (int(brownBin) * 20))
    
    domainfile = "bottlesortingdomain.pddl"

    if((int(lightSensor) >= 400) & (int(lightSensor) <= 1290) ):
        if(bool(vibrationSensor) == True):
            if(int(colorSensor) >= 800):
                if(int(whiteBin) <= 10):
                    print("White")
                    ++whiteBottle 
                    problemfile = "whiteproblem.pddl"
                else:
                    print("Remove Bottle white")
                    problemfile = "checkclean.pddl"
            elif((int(colorSensor) >= 680) & (int(lightSensor) <= 1290)):
                if(int(greenBin) <= 10):
                    print("Green")
                    ++greenBottle
                    problemfile = "greenproblem.pddl"
                else:
                    print("Remove Bottle green")
                    problemfile = "checkclean.pddl"
            elif((int(colorSensor) >= 500) & (int(lightSensor) <= 1290)):
                if(int(brownBin) <= 10):
                    print("Brown")
                    ++brownBottle
                    problemfile = "brownproblem.pddl"
                else:
                    print("Remove Bottle brown")
                    problemfile = "checkclean.pddl"
        else:
            print("Remove Bottle all")
            problemfile = "checkclean.pddl"
    else:
        print("Remove Bottle all")
        problemfile = "checkclean.pddl"

    #     AI planning

#    problemfile = "plasticdetection.pddl"
#    problemfile = "brownproblem.pddl"
    
    data = {'domain': open(domainfile, 'r').read(),
        'problem': open(problemfile, 'r').read()}

    response = requests.post('http://solver.planning.domains/solve', json=data).json()

    actresult = []
    
    for act in response['result']['plan']:
       step = act['name']
       actuations = step[1:len(step)-1].split(' ')
       actresult.append(actuations)
         
    if 'rgbsensewhite1' in str(actresult):
        print('send white')
        conveyor = 90;
        sorter = 30;
        whiteBottle = whiteBottle + 1
    elif 'rgbsensegreen1' in str(actresult):
        print('send green')
        conveyor = 90;
        sorter = 60;
        greenBottle = greenBottle + 1
    elif 'rgbsensebrown1' in str(actresult):
        print('send brown')
        conveyor = 90;
        sorter = 90;
        brownBottle = brownBottle + 1
    else:
        print('send remove')
        conveyor = 30;
        sorter = 0;
        
    actPayload = "[" + str(conveyor)+ "," + str(sorter)+ "]"
    print(actPayload)
#    print(type(actPayload))
    publish.single(MQTT_PATH2, actPayload, hostname=MQTT_SERVER)
        
    visPayload = "[" + str(whiteBin)+ "," + str(greenBin)+ "," + str(brownBin)+ "," + str(whiteBottle)+ ","+ str(greenBottle)+ ","+ str(brownBottle)+ "]"
    print(visPayload)
    publish.single(MQTT_PATH3, visPayload, hostname=MQTT_SERVER)
    
    actresult.clear()
    
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
