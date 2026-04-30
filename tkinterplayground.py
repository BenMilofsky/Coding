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
import time

cols = ["timestamps","CAN1.OBD2.S01PID11_ThrottlePosition","CAN1.OBD2.S01PID05_EngineCoolantTemp"]

 #pandas
 #pandas
 #These 2 lines make tps into 1-D array to fit in filtfilt


 #To test if getting resonable values

class Tab(ttk.Frame):
    
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title
    


def deadband(row,thresh):# debounce has it be on for 3 samples
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
                print(start)
        else:
            start = time.time()
            m=0
           
    return row_d

class plot_after(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tps = master.tps
        t = master.t
        toolbar_frame = ttk.Frame(master)
        toolbar_frame.pack(side=tk.BOTTOM,fill=tk.X)
        canvas_frame = ttk.Frame(master)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.master = master
        fig = Figure()
        b, TPS_butter= butter(2,0.45) #Output is quite similar to PM 2
        tps_d = deadband(tps,0.25)#0.25
        y_butd = filtfilt(b,TPS_butter,tps_d)
        plot1 = fig.add_subplot(111)
        plot1.plot(t,y_butd)#,'b--')
        plot1.plot(t,tps,linewidth=0.5)
        canvas = FigureCanvasTkAgg(fig,master=canvas_frame)#master = self.master)
        canvas.draw() #create and input matplot in canvas
        #canvas.get_tk_widget().pack() #put in window
        toolbar = NavigationToolbar2Tk(canvas,toolbar_frame)#toolbar                                   
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X) #in window
        canvas.get_tk_widget().pack() #put in window

class plot_before(ttk.Frame):
    def __init__(self,master,notebook):
        super().__init__(master)
        t = MainFrame(self,notebook).imported().t
        tps = master.tps
        toolbar_frame = ttk.Frame(master)
        toolbar_frame.pack(side=tk.BOTTOM,fill=tk.X)
        canvas_frame = ttk.Frame(master)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.master = master
        fig = Figure()
        tps_d = deadband(tps,0.25) #Output is quite similar to PM 2
        plot1 = fig.add_subplot(111)
        plot1.plot(t,tps_d)#,'b--')
        #plot1.plot(t,tps,linewidth=2)
        canvas = FigureCanvasTkAgg(fig,master=canvas_frame)
        canvas.draw() #create and input matplot in canvas        
        toolbar = NavigationToolbar2Tk(canvas,toolbar_frame)#toolbar                                   
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X) #in window
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True) #put in window

class plot_graph(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        t= master.t
        tps = master.tps
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
class filter_frame(ttk.Frame):
    def __init__(self,master,notebook):
        super().__init__(master)
        self.notebook= notebook
        self.var_tps = IntVar()
        self.var_tpsf = IntVar()
        self.plot_button = ttk.Button(master, text = 'plot', width = 25, command = self.plot,state=tk.DISABLED)      
        self.label = ttk.Label(master,text='Choose what to plot:').grid(row=1,sticky=W)
        self.plot_button.grid(row=4,sticky=W) 
        
        self.checktps= ttk.Checkbutton(master, text='Unfiltered TPS values', variable=self.var_tps,command=self.checked).grid(row=2,sticky=W)
        #self.checktps['command']=self.checked        
        self.checktpsf= ttk.Checkbutton(master,text='Filtered TPS values', variable=self.var_tpsf, command=self.checked).grid(row=3,sticky=W)
        #self.checktpsf['command']=self.checked

    def checked(self): #if either were checked show button         
        if self.var_tps.get() == 1 or self.var_tpsf.get() == 1:         
            self.plot_button.config(state=tk.NORMAL)       
        else:self.plot_button.config(state=tk.DISABLED)

    def plot(self):
        if self.var_tps.get()==1:            
            frame = self.newTab("Unfiltered plot")
            plot_before(frame,self.notebook)
        elif self.var_tpsf.get()==1:
            frame = self.newTab("Filtered plot")
            plot_after(frame) 
    def newTab(self,title):
        tab_Frame = Tab(self.notebook, title)
        self.notebook.add(tab_Frame, text=title)
        return tab_Frame    

    
     
class MainFrame(ttk.Frame): #ttk as only one tk per application
    def __init__(self,container,notebook): #as frame needs container 
        super().__init__(container)
        self.notebook= notebook 
        self.label = ttk.Label(self,text='Choose what to import:').grid(row=0,sticky=W)
        importcheck = pd.read_csv('TPS1.csv',nrows=2)
        cols= importcheck.cols.tolist()
        self.i=1
        for col in cols:
            var=tk.intVar()
            i= self.i
            i+=1
            self.column_checkbox.insert(text=col,variable =var).grid(row=i,sticky=W)
            self.columnvar[col]=var       
        self.import_button= ttk.Button(self, text = 'import', width = 25, command = self.imported, state=tk.DISABLED)
        self.label = ttk.Label(self,text='Choose what to import:').grid(row=6,sticky=W) 
        self.import_button.grid(row=10,sticky=W)
        self.var_tps= IntVar()
        self.var_temp= IntVar()
        self.checktpsimport=tk.Checkbutton(self, text='Tps', variable=self.var_tps,command=self.checked).grid(row=8,sticky=W)
        self.checktpsimport=tk.Checkbutton(self, text='Temp', variable=self.var_temp,command=self.checked).grid(row=9,sticky=W)

    def checked(self): #if either were checked show button         
        if self.var_tps.get() == 1 or self.var_tpsf.get() == 1:         
            self.import_button.config(state=tk.NORMAL)       
        else:self.import_button.config(state=tk.DISABLED)
    
    def imported(self):

        time= pd.read_csv('TPS1.csv', usecols=['timestamps']) #only faster with over 500k values with 50k or less numpy is better
        self.t= time[('timestamps')].values
        self.t =np.array(self.t)
        if self.var_tps.get()==1:
            tps= pd.read_csv('TPS1.csv',usecols=["CAN1.OBD2.S01PID11_ThrottlePosition"]).values 
            tps= np.asarray(tps).flatten()
            self.tps = np.ascontiguousarray(tps)           
            self.import_button.config(state=tk.NORMAL)
            frame = self.newTab("Choose filter")
            filter_frame(frame,self.notebook)

        if self.var_temp.get()==1:            
            temp= pd.read_csv('TPS1.csv',usecols=["CAN1.OBD2.S01PID05_EngineCoolantTemp"]).values
            temp = np.asarray(temp).flatten()
            self.temp = np.ascontiguousarray(temp)
            self.import_button.config(state=tk.NORMAL)

        else:return self.t

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

    if (change[i]<thresh):
            end= time.time()
            if((end-start)>0.0003):
                row_d[i]=row_d[m]#row_d[i-1]
            else: 
                
                m=i
        else:            
            start= time.time()
            row_d[i]=row_d[i]
            m=i

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