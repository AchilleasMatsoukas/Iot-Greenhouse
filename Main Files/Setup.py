#!/usr/bin/python3
import datetime
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

#Reverse MOTOR section
IN7 = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN7, GPIO.OUT)

IN8 = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN8, GPIO.OUT)

def breakrotation(pin1,pin2):
    GPIO.output(pin1, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(pin2, GPIO.LOW)
    print("RELAY REVERSER :: STOP")
#reverse MOTOR END
    
#Pump MOTOR script
IN2 = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN2, GPIO.OUT)


def Pump_off(pin1):
    GPIO.output(pin1, GPIO.HIGH)
    print("PUMP :: DEACTIVATED")

def Pump_on(pin1):
    GPIO.output(pin1, GPIO.LOW)
    print("PUMP :: ACTIVATED")
#Pump MOTOR END
    

#Fan Section
IN1 = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)


def Air_off(pin1):
    GPIO.output(pin1, GPIO.HIGH)
    print("FAN :: DEACTIVATED")

def Air_on(pin1):
    GPIO.output(pin1, GPIO.LOW)
    print("FAN :: ACTIVATED")
#Fan END

if __name__ == '__main__':
    try:
        print("RPi set up...")
        Air_off(IN1)
        time.sleep(0.2)
        breakrotation(IN7,IN8)
        time.sleep(0.2)
        Pump_off(IN2)
        time.sleep(0.2)
        print("RPi set up completed!")
    except KeyboardInterrupt:
        GPIO.cleanup()