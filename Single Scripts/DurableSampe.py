from durable.lang import *

Res = []
with ruleset('cabbage'):
    @when_all(m.SoilTemp >= 29)
    def FirstRule(c):
        #print ('Rule1 is Activated :  with {0}'.format(c.m.SoilTemp))
        Res.append(1)

    @when_all((m.Temp <= 17) | ((m.Humidity >= 0) & (m.Humidity <= 49)))
    def SecondRule(c):
        #print ('Rule2 is Activated : with {0} {1} {2}'.format(c.m.SoilTemp,c.m.Temp,c.m.Humidity))
        Res.append(2)
        
    @when_all(((m.SoilTemp >= 10) & (m.SoilTemp <= 20)) | (((m.Temp >= 10) & (m.Temp <= 23))) | ((m.Humidity >= 50) & (m.Humidity <= 80)))
    def ThirdRule(c):
        #print ('Rule3 is Activated : with {0} {1} {2}'.format(c.m.SoilTemp,c.m.Temp,c.m.Humidity))
        Res.append(3)
        
    @when_all(((m.Temp >= 24) & (m.Temp <= 30)) | ((m.SoilTemp >= 21) & (m.SoilTemp <= 28)))
    def FourthRule(c):
        #print ('Rule4 is Activated : with {0} {1}'.format(c.m.SoilTemp,c.m.Temp))
        Res.append(4)
    
    @when_all(((m.Humidity >= 81) & (m.Humidity <= 100)) | (m.Temp >= 31))
    def FifthRule(c):
        #print ('Rule5 is Activated : with {0} {1}'.format(c.m.Humidity, c.m.Temp))
        Res.append(5)

def First():
    print("First")
    #Pump_on(250ml)

def Second():
    print("Second")
    #Reverser_off()
    #Air_off()

def Third():
    print("Third")
    pass

def Fourth():
    print("Fourth")
    #Reverser_on()
    
def Fifth():
    print("Fifth")
    #Air_on()
    #Reverser_on()

def Result(S, T, H):
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
    Res.clear()

Result(24.32800, 27.29659, 59.67988)
