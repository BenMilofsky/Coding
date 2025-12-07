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

class Tab(ttk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title

def deadband(row,thresh):# debounce has it be on for 3 samples
    change = np.diff(row,prepend=row[0])
    row_d = row.copy()
    N=0
    for i in range(1,len(row_d)):
        if (change[i]<thresh):
            N += 1
        else:N=0 #change it to a more time based thing
        if(N>3):
            row_d[i]=row_d[i-1]
        else: row_d[i]=row_d[i]
    return row_d

class plot_after(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        fig = Figure(figsize = (10, 5),dpi = 100)
        b, TPS_butter= butter(2,0.45) #Output is quite similar to PM 2
        tps_d = deadband(tps,0.25)
        y_butd = filtfilt(b,TPS_butter,tps_d)
        plot1 = fig.add_subplot(111)
        plot1.plot(t,y_butd)#,'b--')
        plot1.plot(t,tps,linewidth=0.5)
        canvas = FigureCanvasTkAgg(fig,master=master)#master = self.master)
        canvas.draw() #create and input matplot in canvas
        #canvas.get_tk_widget().pack() #put in window
        toolbar = NavigationToolbar2Tk(canvas,self)#toolbar                                   
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X) #in window
        canvas.get_tk_widget().pack() #put in window

class plot_before(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        toolbar_frame = ttk.Frame(master)
        toolbar_frame.pack(side=tk.BOTTOM,fill=tk.X)
        canvas_frame = ttk.Frame(master)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.master = master
        fig = Figure()
        b, TPS_butter= butter(2,0.45) #Output is quite similar to PM 2
        y_but = filtfilt(b,TPS_butter,tps)
        plot1 = fig.add_subplot(111)
        plot1.plot(t,y_but)#,'b--')
        plot1.plot(t,tps,linewidth=2)
        canvas = FigureCanvasTkAgg(fig,master=canvas_frame)
        canvas.draw() #create and input matplot in canvas        
        toolbar = NavigationToolbar2Tk(canvas,toolbar_frame)#toolbar                                   
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X) #in window
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) #put in window


class MainFrame(ttk.Frame): #ttk as only one tk per application
    def __init__(self,container,notebook): #as frame needs container 
        super().__init__(container)
        self.notebook= notebook
        self.plot_button = ttk.Button(self, text = 'plot', width = 25, command = self.plot, state=tk.DISABLED)      
        self.label = ttk.Label(self,text='Choose what to plot:').grid(row=1,sticky=W)
        self.plot_button.grid(row=4,sticky=W) 
        self.var_tps = IntVar()
        self.var_tpsf = IntVar()
        self.checktps= tk.Checkbutton(self, text='Unfiltered TPS values', variable=self.var_tps,command=self.checked).grid(row=2, sticky=W)
        #self.checktps['command']=self.checked        
        self.checktpsf= tk.Checkbutton(self,text='Filtered TPS values', variable=self.var_tpsf)
        self.checktpsf['command']=self.checked
        self.checktpsf.grid(row=3, sticky=W)        
        #self.pack()

    def checked(self): #if either were checked show button         
        if self.var_tps.get() == 1 or self.var_tpsf.get() == 1:         
            self.plot_button.config(state=tk.NORMAL)       
        else:self.plot_button.config(state=tk.DISABLED)
    
    def plot(self):
        if self.var_tps.get()==1:            
            frame = self.newTab("Unfiltered plot")
            plot_before(frame)
        if self.var_tpsf.get()==1:
            frame = self.newTab("Filtered plot")
            plot_after(frame)           
    
    def newTab(self,title):
        tab_Frame = Tab(self.notebook, title)
        self.notebook.add(tab_Frame, text=title)
        return tab_Frame     
     
 

class App(tk.Tk): #Class is same as doing home = Tk()
    def __init__(self):
        super().__init__() 
        self.title('Sensor GUI')
        self.notebook= ttk.Notebook(self)
        self.notebook.grid(row=0,sticky=NW)
        self.main_tab = MainFrame(self,self.notebook)
        self.notebook.add(self.main_tab, text="Main")
        


if __name__=="__main__":
    app = App()
    frame= MainFrame(app,app)
    app.mainloop()










"""
menu = Menu(home)
home.config(menu=menu)
filemen = Menu(menu)
menu.add_cascade(label='File', menu=filemen)
filemen.add_command(label='New')
filemen.add_command(label='Open...')
filemen.add_separator()
filemen.add_command(label='Exit', command=home.quit)
#mainloop()





if (any(checked)==True):
    
    print(checked)
    plot = tk.Button(home, text = 'plot', width = 25, command = home.destroy)
    
    plot.grid(row=4,sticky=W)
else:
    checked =[var_tps.get(),var_tpsf.get()]
    print("Hell no")
    print(checked)
    # 
    home.mainloop()


#graph = tk.Tk()
#graph.title('Sensor GUI')

#second = Toplevel()
#second.title('Second screen')

#destroy = tk.Button(home, text = 'plot', width = 25, command = home.destroy)


#graph.mainloop()
#second.mainloop()
"""