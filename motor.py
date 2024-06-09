import RPi.GPIO as GPIO
import time

def activate_motor(msg):
    # 핀 설정
    IN1 = 17
    IN2 = 18
    PWMA = 27  # PWMA 핀에 PWM 신호를 보냄

    # GPIO 모드 설정
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(PWMA, GPIO.OUT)

    # PWM 설정
    pwm = GPIO.PWM(PWMA, 1000)  # 주파수 1kHz
    pwm.start(0)

    if(msg == "forward"):
        try:
            set_motor(50, IN1, IN2, pwm)  # 모터를 50% 속도로 정방향 회전
            time.sleep(5)
            set_motor(0, IN1, IN2, pwm)   # 모터 정지
            time.sleep(5)
        except KeyboardInterrupt:
            pass
    elif(msg == "backward"):
        try:
            set_motor(-50, IN1, IN2, pwm)  # 모터를 50% 속도로 역방향 회전
            time.sleep(5)
            set_motor(0, IN1, IN2, pwm)   # 모터 정지
            time.sleep(5)
        except KeyboardInterrupt:
            pass

    pwm.stop()
    GPIO.cleanup()

def set_motor(speed, IN1, IN2, pwm):
    if speed > 0:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    elif speed < 0:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
    
    pwm.ChangeDutyCycle(abs(speed))

