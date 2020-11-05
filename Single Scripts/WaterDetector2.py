
import RPi.GPIO as GPIO
import time

channel = 26

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)


def Check_Weather():
   return GPIO.input(channel)


if __name__ == '__main__':
    try:
        while 1:
            time.sleep(5)
            x = Check_Weather()
            if x==1:
                print ("WATER DETECTOR 2 :: NO water detected")
            elif x==0:
                print ("WATER DETECTOR 2 :: Water detected")
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()



