#!/usr/bin/python3
import datetime
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

#Temp sensor
def Tempmeasure():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    return temperature, humidity
#Temp END


#Soil Temp sensor
def SoilTempmeasure():
    soilhumidity, soiltemperature = Adafruit_DHT.read_retry(11, 3)
    #print('Soil Temp: {0:0.1f} C  Soil Humidity: {1:0.1f} %'.format(soiltemperature, soilhumidity))
    return soiltemperature, soilhumidity
#Soil Temp END
    

if __name__ == '__main__':
    try:
        while 1:
            t = datetime.datetime.today()
            ymd = "Data/" + str(datetime.date.today()) + ".txt"
            datastream = open(ymd, "a")
            #datastream.write(str(datetime.datetime.now()) + "\n")
            datastream.close()
            count = 0
            while 1:
                #main programm
                datastream = open(ymd, "a")
                temperature, humidity = Tempmeasure()
                soiltemperature, soilhumidity = SoilTempmeasure()
                data = str(temperature) + "," + str(humidity) + "," +str(soiltemperature) + "\n"
                if not ((temperature is None) | (humidity is None) | (soiltemperature is None)):
                    if not (((temperature <= 14) | (humidity >= 100) | (soiltemperature <= 14) | (str(temperature) == 'None') | (str(soiltemperature) == "None"))):   
                        datastream.write(data)
                        datastream.close()
                        print("THREAD WRITING FILE :: " + str(datetime.date.today()) + " :: Temp:" + str(temperature) + "C : Humidity:" + str(humidity) + "% : Soil Temperature:" + str(soiltemperature) +"C")
                time.sleep(60)
                if ((datetime.datetime.now() > datetime.datetime(t.year,t.month,t.day,23,54,0)) and (datetime.datetime.now() < datetime.datetime(t.year,t.month,t.day,23,59,59))):
                    time.sleep(380)
                    break
        GPIO.cleanup()
    except KeyboardInterrupt:
        datastream.close()
        GPIO.cleanup()
