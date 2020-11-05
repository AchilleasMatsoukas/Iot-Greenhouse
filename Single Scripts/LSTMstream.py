import time
# univariate data preparation
import numpy as np
import datetime
import statistics
import math
import tensorflow as tf
tf.get_logger().setLevel('FATAL')
# univariate lstm example
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

def tail(file, n=3, bs=1024):
    f = open(file)
    f.seek(0,2)
    l = 1-f.read(1).count('\n')
    B = f.tell()
    while n >= l and B > 0:
            block = min(bs, B)
            B -= block
            f.seek(B, 0)
            l += f.read(block).count('\n')
    f.seek(B, 0)
    l = min(l,n)
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
        if end_ix > len(sequence) - 1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


def training(raw_seq, Values, array1):
    max1 = -1.0
    min1 = 99999.0
    for i in range(Values):
        if raw_seq[i] > max1:
            max1 = raw_seq[i]
        if raw_seq[i] < min1:
            min1 = raw_seq[i]

    for i in range(Values):
        raw_seq[i] = (raw_seq[i] - min1) / (max1 - min1)

    n_steps = 3
    # split into samples
    X, y = split_sequence(raw_seq, n_steps)
    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    # define model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    start = datetime.datetime.now()
    model.fit(X, y, epochs=10, verbose=0)
    end = datetime.datetime.now()
    totalTime = end - start
    print("LSTM :: TRAINING TIME :: ", totalTime, " seconds")
    ############################# mexri edw einai to training ##################################
    x_input = array(array1)
    x_input = x_input.reshape((1, n_steps, n_features))
    yhat = model.predict(x_input, verbose=0)
    #print(yhat)
    return yhat


if __name__ == '__main__':
    try:
        while 1:
            print("--------------------------//--------------------------")
            ymd = str(datetime.date.today()) + ".txt"
            last_3 = tail(ymd)
            sample1 = last_3[0].split(",")
            sample2 = last_3[1].split(",")
            sample3 = last_3[2].split(",")
            Temperature = [float(sample1[0]), float(sample2[0]), float(sample3[0])]
            Temperature = np.array(Temperature)
            Humidity = [float(sample1[1]), float(sample2[1]), float(sample3[1])]
            Humidity = np.array(Humidity)
            Soiltemperature = [float(sample1[2]), float(sample2[2]), float(sample3[2])]
            Soiltemperature = np.array(Soiltemperature)
            SoilHumidity = [float(sample1[3]), float(sample2[3]), float(sample3[3])]
            SoilHumidity = np.array(SoilHumidity)

            Temperature_Deviation = np.std(Temperature)
            Temperature_Mean = (float(sample1[0]) + float(sample2[0]) + float(sample3[0])) / 3

            Humidity_Deviation = np.std(Humidity)
            Humidity_Mean = (float(sample1[1]) + float(sample2[1]) + float(sample3[1])) / 3

            Soiltemperature_Deviation = np.std(Soiltemperature)
            Soiltemperature_Mean = (float(sample1[2]) + float(sample2[2]) + float(sample3[2])) / 3

            SoilHumidity_Deviation = np.std(SoilHumidity)
            SoilHumidity_Mean = (float(sample1[3]) + float(sample2[3]) + float(sample3[3])) / 3

            Values = 500

            raw_seq_Temp = np.random.normal(Temperature_Mean, Temperature_Deviation, Values)
            x1 = training(raw_seq_Temp, Values, Temperature)
            print("LSTM :: PREDICTION :: Temperature:" + str(float(x1[0])))
            raw_seq_Humidity = np.random.normal(Humidity_Mean, Humidity_Deviation, Values)
            x2 = training(raw_seq_Humidity, Values, Humidity)
            print("LSTM :: PREDICTION :: Humidity:" + str(float(x2[0])))
            raw_seq_Soil_Temperature = np.random.normal(Soiltemperature_Mean, Soiltemperature_Deviation, Values)
            x3 = training(raw_seq_Soil_Temperature, Values, Soiltemperature)
            print("LSTM :: PREDICTION :: Soil Temperature:" + str(float(x3[0])))
            raw_seq_Soil_Humidity = np.random.normal(SoilHumidity_Mean, SoilHumidity_Deviation, Values)
            x4 = training(raw_seq_Soil_Humidity, Values, SoilHumidity)
            print("LSTM :: PREDICTION :: Soil Humidity:" + str(float(x4[0])))
            time.sleep(5*60)
    except KeyboardInterrupt:
        exit()
