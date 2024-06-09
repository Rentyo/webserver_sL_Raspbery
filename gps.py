import serial
import pynmea2
from sensor.mqttserver import get_client, send_data
from datetime import datetime
from sensor.db import dbConnect


def parseGPS(str,client,state):
    topic = "sensor/gps"
    if str.find('GGA')>0:
        print(str)
        msg = pynmea2.parse(str)
        now = datetime.now()
        #print("Timestamp: %s -- Lat: %s %s -- Lon : %s %s -- Altitude : %s. %s" %(msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))
        print(msg.latitude, msg.longitude)
        if(msg.latitude and msg.longitude):
            data = {'lati' : msg.latitude, 'long' : msg.longitude ,'date' : now.date(), 'time' : now.time() }
            send_data(topic,client,data)
        if (state['db_on'] and now.day == 1 and now.hour == 0 and now.minute == 0 and msg.latitude and msg.longitude):
            dbConnect('gps', data)
            state['db_on'] = False
        if(now.minute == 1):
            state['db_on'] = True
serialPort = serial.Serial("/dev/ttyS0" , 9600, timeout= 0.5)

def activate_gps(client):
    state = {'db_on': False}
    while True:
        byte_data = serialPort.readline()
        str_data = byte_data.decode('ascii', errors='replace').strip()
        print(str_data)
        parseGPS(str_data, client,state)
              
