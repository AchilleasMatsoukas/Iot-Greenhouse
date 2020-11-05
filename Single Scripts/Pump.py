import RPi.GPIO as GPIO
import time
import datetime
#import pause

#1ml == 0,08sec

GPIO.setwarnings(False)

IN2 = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN2, GPIO.OUT)


def Pump_off(pin1):
    GPIO.output(pin1, GPIO.HIGH)
    print("PUMP :: DEACTIVATED")

def Pump_on(pin1):
    GPIO.output(pin1, GPIO.LOW)
    print("PUMP :: ACTIVATED")

def Winter():
    ml = 10000
    for i in range(0,4):
        print("THREAD PUMP :: Opening for " + str(ml/5) + " ml")
        Pump_on(IN2)
        time.sleep(0.08*ml/10)
        Pump_off(IN2)
        time.sleep(3600)

def Spring():
    ml = 10000
    for i  in range(0,4):
        print("THREAD PUMP :: Opening for " + str(ml/5) + " ml")
        Pump_on(IN2)
        time.sleep(0.08*ml/2/6)
        Pump_off(IN2)
        time.sleep(3600)
    time.sleep(28800)
    print("THREAD PUMP :: Opening for " + str(ml/10) + " ml")
    Pump_on(IN2)
    time.sleep(0.08*ml/2/10)
    Pump_off(IN2)

def Summer():
    ml = 10000
    for i in range(0,4):
        print("THREAD PUMP :: Opening for " + str(ml/5/2) + " ml")
        Pump_on(IN2)
        time.sleep(0.08*ml/2/10)
        Pump_off(IN2)
        time.sleep(3600)
    time.sleep(25200)
    for i in range(0,4):
        print("THREAD PUMP :: Opening for " + str(ml/5/2) + " ml")
        Pump_on(IN2)
        time.sleep(0.08*ml/2/10)
        Pump_off(IN2)
        time.sleep(3600)
        

if __name__ == '__main__':
    try:
        #while 1:
        time.sleep(10)
        print("Pumping Water for 5seconds...")
        Pump_on(IN2)
        time.sleep(5)
        Pump_off(IN2)
    except KeyboardInterrupt:
        GPIO.cleanup()

