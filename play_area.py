import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import scipy as sp
import tkinter as tk
from tkinter import *
from tkinter import ttk
from scipy.signal import remez,filtfilt,butter

cols = ["timestamps","CAN1.OBD2.S01PID11_ThrottlePosition","CAN1.OBD2.S01PID05_EngineCoolantTemp"]

df= pd.read_csv('TPS1.csv',header=[0,1]) #only faster with over 500k values with 50k or less numpy is better
t= df['timestamps'].values #pandas
tps= df['CAN1.OBD2.S01PID11_ThrottlePosition'].values #pandas
temp= df['CAN1.OBD2.S01PID05_EngineCoolantTemp'].values
tps= np.asarray(tps).flatten()
temp = np.asarray(temp).flatten()
tps = np.ascontiguousarray(tps) #These 2 lines make tps into 1-D array to fit in filtfilt
temp = np.ascontiguousarray(temp)
print(df[cols]) #To test if getting resonable values


window = Tk()
#root = Tk() #Sets up window
window.geometry("500x500")
window.title("Plots")

def StartPage():
    home = Tk()
#root = Tk() #Sets up window
    home.geometry("500x500")
    home.title("Plots")

def plot_before():
    fig = Figure(figsize = (5, 5),dpi = 100)
    b, TPS_butter= butter(2,0.45) #Output is quite similar to PM 2
    y_but = filtfilt(b,TPS_butter,tps)
    plot1 = fig.add_subplot(111)
    plot1.plot(t,y_but)#,'b--')
    plot1.plot(t,tps,linewidth=2)
    canvas = FigureCanvasTkAgg(fig,master = window)
    canvas.draw() #create and input matplot in canvas
    canvas.get_tk_widget().pack() #put in window
    toolbar = NavigationToolbar2Tk(canvas,window)#toolbar                                   
    toolbar.update()
    canvas.get_tk_widget().pack() #in window





#root.title("Post-race preformance GUI")
#mainframe = ttk.Frame(root, padding=(3,3,12,12))
#mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
#cores = StringVar()
#cores_entry= ttk.Entry(mainframe,width=9,textvariable=cores)
#cores_entry.grid(column=2,row=10,sticky=(E,W))
#ttk.Button(root, text="Plots",command=plot_before).grid()
#root.mainloop()

#methodology =implmentation,theoretical (filter)backround, how u implement 
# how am i writing code (libraies, where you getting it, software flowchart ) why anything and not eg website
# 9trail and error ,why heres pseudo code and how it works 
#chatgpt chat logs

def deadband(row,thresh):# debounce has it be on for 3 samples
    change = np.diff(row,prepend=row[0])
    #change = np.insert(change,0,False,axis=0)
    row_d = row.copy()
    N=0
    #row_d[change<thresh]= np.roll(row_d,1)[change<thresh]
    for i in range(1,len(row_d)):
        if (change[i]<thresh):
            N += 1
        else:N=0
        if(N>3):
            row_d[i]=row_d[i-1]
        else: row_d[i]=row_d[i]
        #if (row_d[(change<thresh)].all()):
            #row_d[(change<thresh)]= np.roll(row,1)[(change<thresh)]
            #return row_d
    return row_d

def plot_after():
    fig = Figure(figsize = (15, 6),dpi = 100)
    b, TPS_butter= butter(2,0.45) #Output is quite similar to PM 2
    tps_d = deadband(tps,0.25)
    y_butd = filtfilt(b,TPS_butter,tps_d)
    plot1 = fig.add_subplot(111)
    #plt.figure(3)
    plot1.plot(t,y_butd)#,'b--')
    plot1.plot(t,tps,linewidth=0.5)
    #plt.plot(t,y_but,linewidth=1)
    #plt.title('2nd Order Butterworth')
    canvas = FigureCanvasTkAgg(fig,master = window)
    canvas.draw() #create and input matplot in canvas
    canvas.get_tk_widget().pack() #put in window
    toolbar = NavigationToolbar2Tk(canvas,window)#toolbar                                   
    toolbar.update()
    canvas.get_tk_widget().pack() #in window
    

plot_before = Button(master = window,
                     height = 2,
                     width = 10,
                     command= plot_before,
                    text = "Plot_before")
plot_after = Button(master = window,
                     height = 2,
                     width = 10,
                     command= plot_after,
                    text = "Plot_after")
#
plot_before.pack(side=LEFT)
plot_after.pack(side=RIGHT)
window.mainloop()




#plt.show()
#Try numpy
#df= np.genfromtxt('TPS1.csv',delimiter=',',filling_values=0,names=cols)
#t = df[:,2]
#t= df[np.take_along_axis(df,1,axis=1)]
#tps=np.take_along_axis(df,2,axis=1)
#temp = np.take_along_axis(df,3,axis=1)
#print(df[cols]) #To test if getting resonable values
#print (df)




#Deadband filter
#tps_d = tps.copy()
#for tps_b in df:
#change = np.abs(np.diff(tps))
  #  if(change < 0.5):
   #     df.loc[tps,]

#thresh = 0.5
#if (any(change <thresh)):
    #tps_d = np.roll(tps,1)
    #tps_d[change < thresh] = np.roll(tps,1)[change < thresh]

#def deadband(df,col,thresh):
    #s_val = []
    #np.diff(val)
   # p_Val
  #  if (np.abs(np.diff(val))<thresh):
    
#else return diff