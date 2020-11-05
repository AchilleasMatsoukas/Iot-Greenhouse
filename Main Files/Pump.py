import RPi.GPIO as GPIO
import time
import datetime
import pause

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
        while 1:
            if (datetime.datetime.now().month in [1, 2, 10, 11, 12]):
                t = datetime.datetime.today()
                if (datetime.datetime.now() < datetime.datetime(t.year,t.month,t.day,12,0,0)):
                    print("THREAD PUMP :: WINTER :: Module Loaded")
                    pause.until(datetime.datetime(t.year,t.month,t.day,12,0))
                    Winter()
                else:
                    pause.until(datetime.datetime(t.year,t.month,t.day+1,1,0,0))
            if (datetime.datetime.now().month in [3, 4, 5]):
                t = datetime.datetime.today()
                if (datetime.datetime.now() < datetime.datetime(t.year,t.month,t.day,12,0,0)):
                    print("THREAD PUMP :: SPRING :: Module Loaded")
                    pause.until(datetime.datetime(t.year,t.month,t.day,10,0))
                    Spring()
                else:
                    pause.until(datetime.datetime(t.year,t.month,t.day+1,1,0,0))
            if (datetime.datetime.now().month in [6, 7, 8, 9]):
                t = datetime.datetime.today()
                if (datetime.datetime.now() < datetime.datetime(t.year,t.month,t.day,7,0,0)):
                    print("THREAD PUMP :: SUMMER :: Module Loaded")
                    pause.until(datetime.datetime(t.year,t.month,t.day,7,0,0))
                    Summer()
                else:
                    pause.until(datetime.datetime(t.year,t.month,t.day+1,1,0,0))
    except KeyboardInterrupt:
        GPIO.cleanup()

