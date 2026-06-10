import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import scipy 
from scipy.signal import remez,filtfilt,butter


fs=22 #22.7757184
fp= 3#6
fsb= 5#10 
ap= 0.5
As= 60
N= 16

df= pd.read_csv('TPS1_Dirty.csv',header=[0,1]) 

t= df['timestamps'].values #pandas
tps= df['CAN1.OBD2.S01PID11_ThrottlePosition'].values #pandas
tps= np.asarray(tps).flatten()
tps = np.ascontiguousarray(tps) #These 2 lines make tps into 1-D array to fit in filtfilt


"""#Park-McClellan(PM) Filter
B_TPS=[0,fp,fsb,10]
gain=[1,0]
Tps_filter= remez(87,B_TPS,gain,weight=[1,10],fs=fs)#2.65
ytps= filtfilt(Tps_filter,1,tps)

plt.figure(1)
plt.plot(t,tps,label='Raw data') #,'g--'
plt.plot(t,ytps,linewidth=1.4, label='Filtered')
plt.xlabel("Time (s)")
plt.ylabel("Throttle position (%)")
plt.legend()
plt.title('Parks McClellan')
#PM end

#Moving average(MA) Filter
TPSMA=5#16#7
MA=np.ones(TPSMA)/TPSMA #Higher number more smoothing but smooths out fast pedal strokes no good number
y_ma= filtfilt(MA,1,tps)

plt.figure(2)

plt.plot(t,tps,label="Raw data")#,'b--')
plt.plot(t,y_ma,linewidth =2,label= "Filtered")
plt.xlabel("Time (s)")
plt.ylabel("Throttle position (%)")
plt.legend()
plt.title('Moving average Raw vs Filtered')
#MA end"""


#2nd Order butterworth (BW)

b, TPS_butter= butter(4,0.225) 
y_but = filtfilt(b,TPS_butter,tps)
plt.figure(1)
plt.plot(t,tps,label="Raw data")#,'b--')
plt.plot(t,y_but,linewidth=2,label= "Filtered")
plt.xlabel("Time (s)")
plt.ylabel("Throttle position (%)")
plt.legend()
plt.title('Butterworth')

#Hybrid deadband debounce filter
def deadband(row,thresh):
    #row = row.to_numpy()
    #change = np.diff(row,prepend=row[0])
    #change = np.insert(change,0,False,axis=0)
    row_d = row.copy()
    row_s = row.copy()
    last_trusted = row_d[0]
    #start = time.time()
    m=0
    #row_d[change<thresh]= np.roll(row_d,1)[change<thresh]
    for i in range(1,len(row_d)):
        change = abs(row_d[i]- last_trusted)
        
        
        if change >= thresh:# and change[i]!=0:
            #row_d[i]=(row_d[i]+((row_d[i]-row_s[i])/m)) 
            last_trusted = row_d[i]
            m=0
            
            
            
        else:
            m+=1
            correction = (row_d[i] - last_trusted) / (m + 1)
            last_trusted += correction 
           
        row_s[i] = last_trusted
    return row_s

Debounce = deadband(tps,0.4) #0.4 0.25
plt.figure(3)
plt.plot(t,tps,label="Raw data")#,'b--')
plt.plot(t,Debounce,linewidth=2,label= "Filtered")
plt.xlabel("Time (s)")
plt.ylabel("Throttle position (%)")
plt.legend()
plt.title('Hybrid deadband temporal smoothing filter')

Debounce = deadband(tps,0.25) #0.4 0.25
plt.figure(2)
plt.plot(t,tps,label="Raw data")#,'b--')
plt.plot(t,Debounce,linewidth=2,label= "Filtered")
plt.xlabel("Time (s)")
plt.ylabel("Throttle position (%)")
plt.legend()
plt.title('Hybrid deadband temporal smoothing filter')


plt.show()