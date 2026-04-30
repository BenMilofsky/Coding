import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.signal import remez,filtfilt,butter


fs=22 #22.7757184
fp= 3#6
fsb= 5#10 
ap= 0.5
As= 60
N= 16

cols = ["timestamps","CAN1.OBD2.S01PID11_ThrottlePosition","CAN1.OBD2.S01PID05_EngineCoolantTemp"]

df= pd.read_csv('TPS1_Dirty.csv',header=[0,1]) #only faster with over 500k values with 50k or less numpy is better
#df= np.genfromtxt('TPS1.csv',delimiter=',',skip_header=1,filling_values=0,names=True)
#t= df[]#np.take_along_axis(df,1,axis=1)
t= df['timestamps'].values #pandas
tps= df['CAN1.OBD2.S01PID11_ThrottlePosition'].values #pandas
#tps=np.take_along_axis(df,2,axis=1)
temp= df['CAN1.OBD2.S01PID05_EngineCoolantTemp'].values
#temp = np.take_along_axis(df,3,axis=1)
tps= np.asarray(tps).flatten()
temp = np.asarray(temp).flatten()
tps = np.ascontiguousarray(tps) #These 2 lines make tps into 1-D array to fit in filtfilt
temp = np.ascontiguousarray(temp)
print(df[cols]) #To test if getting resonable values

#Park-McClellan(PM) Filter
B_TPS=[0,fp,fsb,10]
gain=[1,0]
Tps_filter= remez(N,B_TPS,gain,weight=[1,2.65],fs=fs)#Does very little to current dataset adds a little jitter 
ytps= filtfilt(Tps_filter,1,tps)

plt.figure(1)
plt.plot(t,tps, linewidth=0.7,label='raw') #,'g--'
plt.plot(t,ytps,'r',linewidth=1, label='filtered')
plt.title('Parks McClellan raw vs filtered')
#PM end

#Moving average(MA) Filter
TPSMA=4#16#5
MA=np.ones(TPSMA)/TPSMA #Higher number more smoothing but smooths out fast pedal strokes no good number
y_ma= filtfilt(MA,1,tps)

plt.figure(2)
plt.plot(t,tps)#,'b--')
plt.plot(t,y_ma,linewidth =2)
plt.title('Moving average Raw vs Filtered')
#MA end




#2nd Order butterworth (BW)
b, TPS_butter= butter(2,0.45) #Output is quite similar to PM 2
y_but = filtfilt(b,TPS_butter,tps)

plt.figure(3)
plt.plot(t,tps)#,'b--')
plt.plot(t,y_but,linewidth=2)
plt.title('2nd Order Butterworth')



#Temps_Moving average filter
TempMA=200
MA2=np.ones(TempMA)/TempMA #Higher number more smoothing but smooths out fast pedal strokes no good number
Temp_ma= filtfilt(MA2,1,temp)
plt.figure(4)
plt.plot(t,temp)
plt.plot(t,Temp_ma,'r:', linewidth= 2)
plt.title('Engine temps')
#Temp_MA end

b, TPS_butter= butter(2,0.45) #Output is quite similar to PM 2
y_but = filtfilt(b,TPS_butter,temp)

plt.figure(5)
plt.plot(t,temp)#,'b--')
plt.plot(t,y_but,linewidth=2)
plt.title('2nd Order Butterworth')
plt.show()


