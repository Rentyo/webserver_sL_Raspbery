import time
import board
import adafruit_dht
from sensor.mqttserver import get_client, send_data
from datetime import datetime
from sensor.db import dbConnect 


def check_tem_hum(client):
    dhtDevice = adafruit_dht.DHT22(board.D4)
    topic = "sensor/tem_hum"
    db_on = True
    #client = get_client()
    while True:
        try:
            now = datetime.now()
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9/5) +32
            humidity = dhtDevice.humidity
            data = {'temp' :[temperature_c,temperature_f], 'hum' : humidity, 'date' : now.date(), 'time' : now.time() }
            send_data(topic,client,data)
            if ((now.minute == 0 or now.minute == 30) and db_on ):
                dbConnect('tem_hum', data)
                db_on = False

            if((now.minute == 1 or now.minute == 31)):
                db_on = True    
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        finally :
            time.sleep(5.0)



    


