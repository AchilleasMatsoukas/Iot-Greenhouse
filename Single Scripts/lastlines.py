import datetime
import time
import statistics

def tail(file, n=5, bs=1024):
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


if __name__ == '__main__':
    try:
        while 1:
            ymd = str(datetime.date.today()) + ".txt"
            last_5 = tail(ymd)
            sample1 = last_5[0].split(",")
            sample2 = last_5[1].split(",")
            sample3 = last_5[2].split(",")
            sample4 = last_5[3].split(",")
            sample5 = last_5[4].split(",")
            
            Temperature = (float(sample1[0]), float(sample2[0]), float(sample3[0]), float(sample4[0]), float(sample5[0]))
            Humidity = (float(sample1[1]), float(sample2[1]), float(sample3[1]), float(sample4[1]), float(sample5[1]))
            Soiltemperature = (float(sample1[2]), float(sample2[2]), float(sample3[2]), float(sample4[2]), float(sample5[2]))
            SoilHumidity = (float(sample1[3]), float(sample2[3]), float(sample3[3]), float(sample4[3]), float(sample5[3]))
            
            Temperature_Deviation = statistics.stdev(Temperature)
            Temperature_Mean = (float(sample1[0]) + float(sample2[0]) + float(sample3[0]) + float(sample4[0]) + float(sample5[0]))/5
            
            Humidity_Deviation = statistics.stdev(Humidity)
            Humidity_Mean = (float(sample1[1]) + float(sample2[1]) + float(sample3[1]) + float(sample4[1]) + float(sample5[1]))/5
            
            Soiltemperature_Deviation = statistics.stdev(Soiltemperature)
            Soiltemperature_Mean = (float(sample1[2]) + float(sample2[2]) + float(sample3[2]) + float(sample4[2]) + float(sample5[2]))/5
            
            SoilHumidity_Deviation = statistics.stdev(SoilHumidity)
            SoilHumidity_Mean = (float(sample1[3]) + float(sample2[3]) + float(sample3[3]) + float(sample4[3]) + float(sample5[3]))/5
            
            print(Temperature_Deviation)
            print(Temperature_Mean)
            print(Humidity_Deviation)
            print(Humidity_Mean)
            print(Soiltemperature_Deviation)
            print(Soiltemperature_Mean)
            print(SoilHumidity_Deviation)
            print(SoilHumidity_Mean)
            
            time.sleep(5*60)
            
            
           
    except KeyboardInterrupt:
        #datastream.close()
        exit()