import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

#Reverse MOTOR script
IN1 = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)


def Air_off(pin1):
    GPIO.output(pin1, GPIO.HIGH)
    print("FAN :: DEACTIVATED")

def Air_on(pin1):
    GPIO.output(pin1, GPIO.LOW)
    print("FAN :: ACTIVATED")

if __name__ == '__main__':
    try:
        time.sleep(10)
        Air_on(IN1)
        time.sleep(5)
        Air_off(IN1)
        time.sleep(5)
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
