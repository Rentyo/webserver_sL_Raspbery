import RPi.GPIO as GPIO 
import time
from datetime import datetime
import os
from sensor.mqttserver import send_data
import base64
from sensor.db import dbConnect 
def check_ring(client):
    topic = "sensor/crash"
    #client = get_client()
    # GPIO 핀 번호 설정
    VIBRATION_PIN = 23
    # GPIO 모드 설정
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(VIBRATION_PIN, GPIO.IN)

    try:
        while True:
            if GPIO.input(VIBRATION_PIN) == 0:
                now = datetime.now()
                print("진동이 발생했습니다")
                capture_crash()

                with open("sensor/log_image/test.jpg", 'rb') as image_file:
                    image_file = image_file.read()  
                encodedData = base64.b64encode(image_file)
                data = {"time": now ,"log" : "crashed" , "image" : encodedData }
                db_data = {"time": now ,"log" : "crashed" , "image" : image_file }
                send_data(topic,client,data)
                dbConnect('crash', db_data)
                time.sleep(5)
            time.sleep(0.1)  # 100ms 간격으로 체크
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

def capture_crash():
    os.system("libcamera-jpeg -o sensor/log_image/test.jpg -t 500 --width 640 --height 480")
    print("촬영 완료")
    
    
