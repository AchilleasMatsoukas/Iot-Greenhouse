import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

Reverser_Global = 0
#Reverse MOTOR script
IN7 = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN7, GPIO.OUT)

IN8 = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN8, GPIO.OUT)

def Reverser_on(pin1,pin2):
    global Reverser_Global
    if (Reverser_Global == 0): 
        GPIO.output(pin1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(pin2, GPIO.HIGH)
        print("RELAY REVERSER :: ACTIVATED")
        time.sleep(3.4)
        breakrotation(pin1,pin2)
        Reverser_Global = 1

def Reverser_off(pin1,pin2):
    global Reverser_Global
    if (Reverser_Global == 1):
        GPIO.output(pin1, GPIO.LOW)
        time.sleep(0.00001)
        GPIO.output(pin2, GPIO.LOW)
        print("RELAY REVERSER :: ACTIVATED")
        time.sleep(3.1)
        breakrotation(pin1,pin2)
        Reverser_Global = 0

def breakrotation(pin1,pin2):
    GPIO.output(pin1, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(pin2, GPIO.LOW)
    print("RELAY REVERSER :: STOP")
#reverse MOTOR END
    
if __name__ == '__main__':
    try:
        #while 1:
            time.sleep(10)
            Reverser_on(IN7,IN8)
            time.sleep(3)
            #Reverser_off(IN7,IN8)
            time.sleep(5)
        
        #GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
