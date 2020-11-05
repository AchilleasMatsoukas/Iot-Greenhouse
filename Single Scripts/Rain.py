
import RPi.GPIO as GPIO
import time

channel = 19

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
                print ("RAIN SESNSOR :: NOT Raining")
            elif x==0:
                print ("RAIN SENSOR :: Raining")
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()

