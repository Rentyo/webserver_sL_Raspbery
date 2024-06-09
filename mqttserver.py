#MQTT settings
import json
import paho.mqtt.client as mqtt
import base64
import time
from sensor.motor import activate_motor

MQTT_BROKER = "Broker_IP"
MQTT_PORT = 1883
MQTT_TOPICS = ['topic/shadeOn','topic/shadeOff']
def send_data(topic, client, data):
    if data is not None:
        client.publish(topic, json.dumps(data,default=str))    
    else :
        print('전송 실패')

def send_image(topic, client, src):
    with open(src, 'rb') as image_file:
        jpg_as_text = base64.b64encode(image_file.read())

    # MQTT로 전송
    client.publish(topic, jpg_as_text)


def on_message(client, userdata, message):
    if(message.topic == "topic/shadeOn" or message.topic == "topic/shadeOff"):
        activate_motor(str(message.payload.decode("utf-8")))
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic= ", message.topic)
    print("message qos=", message.qos)
    print("message retain flag= ", message.retain)

def get_client(): 
    client = mqtt.Client()
     # Connect to the broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    for topic in MQTT_TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to topic {topic}")
    # Start the loop to process received messages and maintain connections
    client.on_message = on_message

    client.loop_start()
    # Example data to send
    return client

