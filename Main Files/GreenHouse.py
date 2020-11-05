# univariate data preparation
import numpy as np
import datetime
import statistics
import math
import time
# univariate lstm example
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from durable.lang import *
import tensorflow as tf
tf.get_logger().setLevel('FATAL')
#GPIO
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT
import threading
from subprocess import call
GPIO.setwarnings(False)

Reverser_Global = 1
Air_Global = 0

def thread_writing():
    call(["python", "Sensors.py"])

def thread_pump():
    time.sleep(120)
    call(["python", "Pump.py"])

#Reverse MOTOR section
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
        time.sleep(3.3)
        breakrotation(pin1,pin2)
        Reverser_Global = 0

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


#Water Detectors Section
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)


def Check_Water1():
    return GPIO.input(16)


GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)


def Check_Water2():
    return GPIO.input(26)
#Water Detectors END


#Fan Section
IN1 = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)


def Air_off(pin1):
    global Air_Global
    if (Air_Global == 1): 
        GPIO.output(pin1, GPIO.HIGH)
        print("FAN :: DEACTIVATED")
        Air_Global = 0

def Air_on(pin1):
    global Air_Global
    if (Air_Global == 0): 
        GPIO.output(pin1, GPIO.LOW)
        print("FAN :: ACTIVATED")
        Air_Global = 1
#Fan END


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
    

#Rain Sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN)


def Check_Rain():
    return GPIO.input(19)
#Rain Sensor END

Res = []
with ruleset('cabbage'):
    @when_all(m.SoilTemp >= 30.0)
    def FirstRule(c):
        #print ('Rule1 is Activated : with {0}'.format(c.m.SoilTemp))
        Res.append(1)

    @when_all((m.Temp <= 17.0) | ((m.Humidity >= 0) & (m.Humidity <= 30.0)))
    def SecondRule(c):
        #print ('Rule2 is Activated : with {0} {1} {2}'.format(c.m.SoilTemp,c.m.Temp,c.m.Humidity))
        Res.append(2)
        
    @when_all(((m.SoilTemp >= 10.0) & (m.SoilTemp <= 24.0)) | (((m.Temp >= 17.0) & (m.Temp <= 23.0))) | ((m.Humidity >= 30.0) & (m.Humidity <= 80.0)))
    def ThirdRule(c):
        #print ('Rule3 is Activated : with {0} {1} {2}'.format(c.m.SoilTemp,c.m.Temp,c.m.Humidity))
        Res.append(3)
        
    @when_all(((m.Temp >= 23.0) & (m.Temp <= 30.0)) | ((m.SoilTemp >= 24.0) & (m.SoilTemp <= 30.0)))
    def FourthRule(c):
        #print ('Rule4 is Activated : with {0} {1}'.format(c.m.SoilTemp,c.m.Temp))
        Res.append(4)
    
    @when_all(((m.Humidity >= 80.0) & (m.Humidity <= 100)) | (m.Temp >= 30.0))
    def FifthRule(c):
        #print ('Rule5 is Activated : with {0} {1}'.format(c.m.Humidity, c.m.Temp))
        Res.append(5)


def First():
    #print("First")
    Pump_on(IN2)
    time.sleep(10)
    Pump_off(IN2)

def Second():
    #print("Second")
    Reverser_off(IN7,IN8)
    Air_off(IN1)


def Third():
    #print("Third")
    Air_off(IN1)


def Fourth():
    #print("Fourth")
    Reverser_on(IN7,IN8)


def Fifth():
    #print("Fifth")
    Air_on(IN1)
    Reverser_on(IN7,IN8)

def Result(S, T, H):
    global Res
    post('cabbage', {'SoilTemp' : S})
    post('cabbage', {'Temp' : T})
    post('cabbage', {'Humidity' : H})
    res = []
    for i in Res: 
        if i not in res: 
            res.append(i)
    for i in res:
        if i == 1:
            First()
        elif i == 2:
            Second()
        elif i == 3:
            Third()
        elif i == 4:
            Fourth()
        elif i == 5:
            Fifth()
    #print(Res)
    #print(res)
    Res = []


def tail(file, n=3, bs=1024):
    f = open(file)
    f.seek(0, 2)
    l = 1-f.read(1).count('\n')
    B = f.tell()
    while n >= l and B > 0:
        block = min(bs, B)
        B -= block
        f.seek(B, 0)
        l += f.read(block).count('\n')
    f.seek(B, 0)
    l = min(l, n)
    lines = f.readlines()[-l:]
    f.close()
    return lines


# split a univariate sequence into samples
def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


if __name__ == '__main__':
    try:
        processThread1 = threading.Thread(target=thread_writing)
        processThread1.start()
        time.sleep(0.5)
        processThread2 = threading.Thread(target=thread_pump)
        processThread2.start()
        time.sleep(120)
        print("MAIN PROGRAMM :: STARTING SETUP")
        ATemperature = []
        ASoilTemperature = []
        AHumidity = []
        print("MAIN PROGRAMM :: Reading File RDataset for training")
        with open("Data/RDataset.txt") as file:
            for line in file:
                line = line.split(",")
                ATemperature.append(float(line[0]))
                ASoilTemperature.append(float(line[1]))
                AHumidity.append(float(line[2]))

        Temperature_Deviation = np.std(ATemperature)
        Temperature_Mean = np.mean(ATemperature)
        Values = 500
        # print(data)
        # print(Temperature_Deviation)
        # print(Temperature_Mean)
        raw_seq1 = np.random.normal(
            Temperature_Mean, Temperature_Deviation, Values)
        # print(raw_seq1)

        max1 = -1.0
        min1 = 99999.0
        for i in range(Values):
            if raw_seq1[i] > max1:
                max1 = raw_seq1[i]
            if raw_seq1[i] < min1:
                min1 = raw_seq1[i]

        for i in range(Values):
            raw_seq1[i] = (raw_seq1[i] - min1) / (max1 - min1)

        # print(raw_seq1)
        n_steps = 3
        # split into samples
        X, y = split_sequence(raw_seq1, n_steps)
        # reshape from [samples, timesteps] into [samples, timesteps, features]
        n_features = 1
        X = X.reshape((X.shape[0], X.shape[1], n_features))
        # define model
        model1 = Sequential()
        model1.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
        model1.add(Dense(1))
        model1.compile(optimizer='adam', loss='mse')
        # fit model
        start = datetime.datetime.now()
        model1.fit(X, y, epochs=10, verbose=0)
        end = datetime.datetime.now()
        totalTime = end - start
        print("MAIN PROGRAMM :: Training time : ", totalTime, " seconds")

        ############################# mexri edw einai to training ##################################

        SoilTemperature_Deviation = np.std(ASoilTemperature)
        SoilTemperature_Mean = np.mean(ASoilTemperature)
        Values = 500
        raw_seq2 = np.random.normal(
            SoilTemperature_Mean, SoilTemperature_Deviation, Values)

        max1 = -1.0
        min1 = 99999.0
        for i in range(Values):
            if raw_seq2[i] > max1:
                max1 = raw_seq2[i]
            if raw_seq2[i] < min1:
                min1 = raw_seq2[i]

        for i in range(Values):
            raw_seq2[i] = (raw_seq2[i] - min1) / (max1 - min1)

        # print(raw_seq1)
        n_steps = 3
        # split into samples
        X, y = split_sequence(raw_seq2, n_steps)
        # reshape from [samples, timesteps] into [samples, timesteps, features]
        n_features = 1
        X = X.reshape((X.shape[0], X.shape[1], n_features))
        # define model
        model2 = Sequential()
        model2.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
        model2.add(Dense(1))
        model2.compile(optimizer='adam', loss='mse')
        # fit model
        start = datetime.datetime.now()
        model2.fit(X, y, epochs=10, verbose=0)
        end = datetime.datetime.now()
        totalTime = end - start
        print("MAIN PROGRAMM :: Training time : ", totalTime, " seconds")

        ############################# mexri edw einai to training ##################################

        Humidity_Deviation = np.std(AHumidity)
        Humidity_Mean = np.mean(AHumidity)
        Values = 500
        # print(data)
        # print(Temperature_Deviation)
        # print(Temperature_Mean)
        raw_seq3 = np.random.normal(
            Humidity_Mean, Humidity_Deviation, Values)
        # print(raw_seq1)

        max1 = -1.0
        min1 = 99999.0
        for i in range(Values):
            if raw_seq3[i] > max1:
                max1 = raw_seq3[i]
            if raw_seq3[i] < min1:
                min1 = raw_seq3[i]

        for i in range(Values):
            raw_seq3[i] = (raw_seq3[i] - min1) / (max1 - min1)

        # print(raw_seq1)
        n_steps = 3
        # split into samples
        X, y = split_sequence(raw_seq3, n_steps)
        # reshape from [samples, timesteps] into [samples, timesteps, features]
        n_features = 1
        X = X.reshape((X.shape[0], X.shape[1], n_features))
        # define model
        model3 = Sequential()
        model3.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
        model3.add(Dense(1))
        model3.compile(optimizer='adam', loss='mse')
        # fit model
        start = datetime.datetime.now()
        model3.fit(X, y, epochs=10, verbose=0)
        end = datetime.datetime.now()
        totalTime = end - start
        print("MAIN PROGRAMM :: Training time : ", totalTime, " seconds")

        ############################# mexri edw einai to training ##################################
        while 1:
            t = datetime.datetime.today()
            if ((datetime.datetime.now() > datetime.datetime(t.year,t.month,t.day,23,54,0)) and (datetime.datetime.now() < datetime.datetime(t.year,t.month,t.day,23,59,59))):
                time.sleep(600)
            ymd = "Data/" + str(datetime.date.today()) + ".txt"
            last_3 = tail(ymd)
            sample1 = last_3[0].split(",")
            sample2 = last_3[1].split(",")
            sample3 = last_3[2].split(",")

            Temperature_last3 = [float(sample1[0]), float(sample2[0]), float(sample3[0])]
            Temperature_last3_Mean = np.mean(Temperature_last3)
            Temp_input = array([Temperature_last3[0]-Temperature_last3_Mean, Temperature_last3[1]-Temperature_last3_Mean, Temperature_last3[2]-Temperature_last3_Mean])
            Temp_input = Temp_input.reshape((1, n_steps, n_features))
            Temp_Predict = model1.predict(Temp_input, verbose=0)
            T1 = float(Temp_Predict[0] + Temperature_last3_Mean)
            print("MAIN PROGRAMM :: Predict for Temperature : ",T1)

            SoilTemperature_last3 = [float(sample1[2]), float(sample2[2]), float(sample3[2])]
            SoilTemperature_last3_Mean = np.mean(SoilTemperature_last3)
            SoilTemp_input = array([SoilTemperature_last3[0]-SoilTemperature_last3_Mean, SoilTemperature_last3[1]-SoilTemperature_last3_Mean, SoilTemperature_last3[2]-SoilTemperature_last3_Mean])
            SoilTemp_input = SoilTemp_input.reshape((1, n_steps, n_features))
            SoilTemp_Predict = model2.predict(SoilTemp_input, verbose=0)
            S2 = float(SoilTemp_Predict[0] + SoilTemperature_last3_Mean)
            print("MAIN PROGRAMM :: Predict for Soil Temperature : ",S2)

            Humidity_last3 = [float(sample1[1]), float(sample2[1]), float(sample3[1])]
            Humidity_last3_Mean = np.mean(Humidity_last3)
            Humidity_input = array([Humidity_last3[0]-Humidity_last3_Mean, Humidity_last3[1]-Humidity_last3_Mean, Humidity_last3[2]-Humidity_last3_Mean])
            Humidity_input = Humidity_input.reshape((1, n_steps, n_features))
            Humidity_Predict = model3.predict(Humidity_input,verbose=0)
            H3 = float(Humidity_Predict[0] + Humidity_last3_Mean)
            print("MAIN PROGRAMM :: Predict for Humidity : ",H3)
            
            time.sleep(1)
            #Result(SoilTemp,Temp,Humidity)
            #Result(24, 27, 59)
            #print(Res)
            Result(S2, T1, H3)
            #exit(0)
            time.sleep(195)
    except KeyboardInterrupt:
        exit()
