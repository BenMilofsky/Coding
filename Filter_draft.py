import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.signal import remez,filtfilt,butter
import time

fs=22 #22.7757184 //describe each value and its formula
fp= 3#6
fsb= 5#10 
ap= 0.5
As= 60
N= 16


def butterworth(data,Order,Critical_frequency):

    b, f_butter = butter(Order,Critical_frequency) #2,0.45 are basic values
    y_but = filtfilt(b,f_butter,data)

    return y_but

def deadband(row,thresh):# debounce has it be on for 3 samples
    row = row.to_numpy()
    change = np.diff(row,prepend=row[0])
    #change = np.insert(change,0,False,axis=0)
    row_d = row.copy()
    row_s = row.copy()
    start = time.time()
    m=0
    #row_d[change<thresh]= np.roll(row_d,1)[change<thresh]
    for i in range(1,len(row_d)):
        change[i] =np.abs(change[i])
        
        
        if change[i] <thresh:# and change[i]!=0:
            end=time.time()
            m+=1
            if (end-start)>0.0002:
                row_d[i]= row_s[i-m]

                if (abs(row_d[i]-row_s[i])>thresh):
                    row_d[i]=(row_d[i]+((row_d[i]-row_s[i])/m))  #row_s[i]# abs
            else: 
                #print(start)
                pass
        else:
            start = time.time()
            m=0
           
    return row_d

def movingaverage(data,MA_coeff):
    #MA_coeff=4#16#5
    MA=np.ones(MA_coeff)/MA_coeff #Higher number more smoothing but smooths out fast pedal strokes no good number
    y_ma= filtfilt(MA,1,data)
    return y_ma