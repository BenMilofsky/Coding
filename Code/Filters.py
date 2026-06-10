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

"""def deadband(row,thresh):# debounce has it be on for 3 samples
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
            if (end-start)>0.0002:#0.0002
                row_d[i]= row_s[i-m]

                if (abs(row_d[i]-row_s[i])>thresh):
                    row_d[i]=(row_d[i]+((row_d[i]-row_s[i])/m))  #row_s[i]# abs
            else: 
                pass
        else:
            start = time.time()
            m=0
           
    return row_d"""
def deadband(row,thresh):
    row = row.to_numpy()
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

def movingaverage(data,MA_coeff):
    #MA_coeff=4#16#5
    MA=np.ones(MA_coeff)/MA_coeff #Higher number more smoothing but smooths out fast pedal strokes no good number
    y_ma= filtfilt(MA,1,data)
    return y_ma




""""Debounce filter:\n"
                "The debounce (deadband) filter reduces small rapid changes (jitter/noise) in the signal. "
                "A new value is only accepted if the change is greater than the threshold.\n\n"

                "Threshold ('thresh'):\n"
                "- Smaller threshold = more sensitive to small changes, less smoothing.\n"
                "- Larger threshold = ignores more small fluctuations, more smoothing.\n"
                "- Start slightly above the normal noise level in the signal.\n"
                "- Example: if noise varies by about ±0.2, try a threshold around 0.25–0.3.\n\n"

                "Butterworth filter:\n"
                "The Butterworth filter smooths the signal by reducing high-frequency noise while keeping the overall shape of the data smooth.\n\n"

                "Filter order:\n"
                "- Higher order = stronger filtering and steeper cutoff.\n"
                "- Lower order = lighter smoothing with faster response.\n"
                "- Order 4 is a good general starting point.\n\n"

                "Critical frequency:\n"
                "The critical frequency controls when the filter starts reducing higher-frequency signal content.\n"
                "In Python's butter() function, the value must be normalised between 0 and 1:\n"
                "Crit_f = fc / (fs / 2)\n"
                "where:\n"
                "- fc = desired cutoff frequency\n"
                "- fs = sampling frequency\n\n"

                "Smaller critical frequency values give stronger smoothing.\n"
                "Larger values keep more signal detail.\n"
                "A good starting point is around 0.1–0.3, then adjust depending on the amount of noise reduction needed.","""
                
                