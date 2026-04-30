import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from Filter_draft import * #imports all functions can change to import specific
#from Filter_draft import second_order_butterworth

#Input your file here
File = 'TPS1_Dirty.csv' 


class MainFrame(ttk.Frame): #ttk as only one tk per application
    def __init__(self,container,app): #as frame needs container 
        super().__init__(container)
        self.app = app
        #self.headers = pd.read_csv(File,nrows=0)
        self.headers = list(pd.read_csv(File, nrows=0).columns)
        
        self.label = ttk.Label(self,text='Choose what to import:').grid(row=0,sticky=W)
        self.import_button= ttk.Button(self, text = 'import', width = 25, command = self.imported, state=tk.DISABLED)
        self.i=2
        self.var={}
        self.var["timestamps"] = tk.IntVar(value=1)
        for cols in self.headers:
            if cols != ("timestamps"):
                self.var[cols]=tk.IntVar()
                          
                ttk.Checkbutton(self,text=cols,command=self.checked,variable=self.var[cols]).grid(row=self.i,sticky=W)
                self.i+=1
        self.import_button.grid(row=self.i+1,sticky=W)
    def checked(self):
        self.chosen=[]
        for cols in self.headers:            
            if self.var[cols].get()==1:            
                self.chosen.append(cols) 
            else:
                try:
                    self.chosen.remove(cols)
                except:
                    pass              
        if len(self.chosen)==0:
            self.import_button.config(state=tk.DISABLED)
        else: self.import_button.config(state=tk.NORMAL)
        
    def imported(self):
        #Headers = list(self.chosen)

        Imported_data= pd.read_csv(File,usecols=self.chosen)
          
        self.app.NewTab(FilterTab,"Filter",self.chosen,Imported_data)
        
        

class FilterTab(ttk.Frame):
    def __init__(self,container,app,names,data):
        super().__init__(container)
        self.app = app
        self.Deadbanded={}
        self.Butterworthed={}
        self.imported =names
        self.data=data
        self.label = ttk.Label(self,text='Filter options to apply:').grid(row=0,sticky=W)
        self.label = ttk.Label(self,text="Debounce").grid(row=0,column=1,padx=20)
        self.label = ttk.Label(self,text="Butterworth").grid(row=0,column=3,padx=20)        
        #self.label = ttk.Label(self,text="Apply Moving Average").grid(row=0,column=25)
        #self.label = ttk.Label(self,text="Open advanced menu").grid(row=0,column=25)
        self.Threshold_var={}
        self.Butterworth_order={}
        self.Butterworth_Wn={}
        self.i=2
        self.var={}
        self.d_filter={}
        self.b_filter={}
        self.Ma_filter={}
        self.advanced_filter={}
        
        for cols in self.imported:
            if cols != ("timestamps"):
                self.grid_columnconfigure(self.i, pad=30)
                

                self.grid_rowconfigure(self.i, pad=20)
                
                self.Threshold_var[cols]=tk.StringVar()
                self.Butterworth_order[cols]=tk.StringVar()
                self.Butterworth_Wn[cols]=tk.StringVar()
                self.Butterworth_order[cols].set("2")
                self.Threshold_var[cols].set("0.45")
                self.Butterworth_Wn[cols].set("0.1")
                self.var[cols]= tk.IntVar() 
                self.d_filter[cols]= tk.IntVar()
                self.b_filter[cols]= tk.IntVar()
                #self.Ma_filter[cols]= tk.IntVar()
                self.advanced_filter[cols]= tk.IntVar()          
                tk.Label(self,text=cols).grid(row=self.i,sticky=W)
                ttk.Checkbutton(self,text="Threshold:",variable=self.d_filter[cols]).grid(row=self.i,column=1)
                #tk.Label(self,text='').grid(row = self.i,column=2)
                ttk.Entry(self,textvariable= self.Threshold_var[cols]).grid(row = self.i,column=2)
                ttk.Checkbutton(self,text="Order:",variable=self.b_filter[cols]).grid(row=self.i,column=3)
                #tk.Label(self,text='').grid(row = self.i,column=16)
                tk.Label(self,text='    Crit_frequency').grid(row = self.i+1,column=3)
                ttk.Entry(self,textvariable= self.Butterworth_order[cols]).grid(row = self.i,column=4)
                ttk.Entry(self,textvariable= self.Butterworth_Wn[cols]).grid(row = self.i+1,column=4)            
                #ttk.Checkbutton(self,text="",variable=self.Ma_filter[cols]).grid(row=self.i,column=26)
                #ttk.Checkbutton(self,text="",variable=self.advanced_filter[cols]).grid(row=self.i,column=30)
                self.i+=2

        
        #self.plot_pages= ttk.Button(self, text = 'Plot', width = 25, command = self.plotpage, state=tk.NORMAL).grid(row=self.i+2)
        #self.advanced_pages= ttk.Button(self, text = 'Advanced menu', width = 25, command = self.advanced_page, state=tk.NORMAL).grid(row=self.i+3)
        ttk.Button(self, text = 'Plot', width = 25, command =  self.Deadbandfilter, state=tk.NORMAL).grid(row=self.i+4) #If breaks add back self.plot_pages= """lambda:[,self.butterfilter]"""

    
    def advanced_page(self):
        self.chosen=[]
        for cols in self.imported:
            if self.advanced_filter[cols].get()==1:            
                self.chosen.append(cols) 
            else:
                try:
                    self.chosen.remove(cols)
                except:
                    pass              
        if len(self.chosen)==0:
           self.label=tk.Label(self, text="Oops! select advanced menu button next to filters you want to change!").grid(row=self.i+4)
        else: pass#self.app.NewTab(filtersettings,"Filter Settings",self.chosen,self.data)
            
    

    def Deadbandfilter(self):        
        self.Deadbanded={}
        self.Butterworthed={}
        self.d_headers=[col for col in self.var if self.d_filter[col].get()==1 ]
        self.b_headers=[col for col in self.var if self.b_filter[col].get()==1 ]
        datas = self.data
        datas=datas.iloc[1:]
        datas= datas.apply(pd.to_numeric, errors="coerce")
        for cols in self.imported:
            if cols != ("timestamps"):
                if self.d_filter[cols].get()==1:                
                    try:
                        thresh =float(self.Threshold_var[cols].get())
                        result = deadband(datas[cols], thresh)
                        self.Deadbanded[cols] = result 
                    except: print("Only enter numbers")
                
                
                if self.b_filter[cols].get()==1:
                
                    try:
                        order = float(self.Butterworth_order[cols].get())
                        wn = float(self.Butterworth_Wn[cols].get())
                        result = butterworth(datas[cols], order, wn)
                        self.Butterworthed[cols] = result
                        
                    except: print("Only enter numbers") 
                
        Rawplotheaders= []
        Rawplotheaders = [col for col in self.imported if col != "timestamps" ]    #if self.var[col].get()==1  
        self.app.NewTab(plot_page,"Plot",Rawplotheaders,self.data,self.Deadbanded,self.Butterworthed,self.d_headers)
        #return self.Deadbanded,self.Butterworthed

class plot_page(ttk.Frame):
    def __init__(self,container,app,header,data,deadband,butterworth,d_headers):
        super().__init__(container) 
        self.deadband=deadband
        self.butterworth= butterworth
        self.app=app 
        self.header = [col for col in header if col != "timestamps"] 
        self.d_headers= d_headers
        self.data=data
        self.var={}
        self.choosedeadband={}
        self.choosebutterworth={}
        self.master = app
        self.chosen=[]
        fig= Figure(figsize=(7,5),dpi=100)
        self.plot1= fig.add_subplot(111)
        self.chosendata=[]
        optionframe = Frame(self)
        optionframe.grid(row=0,column=0)
        graphframe=ttk.Frame(self)
        graphframe.grid(row=0,column=5)
        toolbarframe =ttk.Frame(self)
        toolbarframe.grid(row=1,column=5)
        
        self.canvas = FigureCanvasTkAgg(fig,master=graphframe)#master = self.master)
        self.canvas.get_tk_widget().grid()
        
        NavigationToolbar2Tk(self.canvas, toolbarframe)
        self.units = self.data.iloc[0]   # store unit row
        self.data = self.data.iloc[1:]   # remove units

        self.data = self.data.apply(pd.to_numeric, errors="coerce")
        self.y = self.data['timestamps'].to_numpy()
        
        
        self.i=0
        
        for cols in self.header:
            self.var[cols]= tk.IntVar()
            self.choosedeadband[cols]=tk.IntVar()
            self.choosebutterworth[cols]= tk.IntVar()
            ttk.Checkbutton(optionframe,text=cols,command=self.plot, variable=self.var[cols]).grid()
            
            
            if cols in self.deadband:
               
                ttk.Checkbutton(optionframe,text="Deadbanded  "+cols,command=self.plot, variable=self.choosedeadband[cols]).grid()
            if cols in self.butterworth:
                ttk.Checkbutton(optionframe,text="Butterwoth  "+cols,command=self.plot, variable=self.choosebutterworth[cols]).grid()
        
            
        self.update_button= ttk.Button(optionframe, text = 'Update plot', width = 25, command = self.plot_page, state=tk.NORMAL).grid()
        
   
        
        
    def plot(self):
        
        self.chosen = [col for col in self.header if self.var[col].get() == 1]
        self.chosen_D= [col for col in self.deadband if self.choosedeadband[col].get() == 1]
        self.chosen_B= [col for col in self.butterworth if self.choosebutterworth[col].get() == 1]
        

    def plot_page(self):
        
        self.plot1.clear()
        y = self.data['timestamps'].to_numpy()
        plotted = False #tracks if anything has been plotted
        for cols in self.chosen_D:
            deadband= self.deadband[cols]
            
            if len(y)== len(deadband):
                self.plot1.plot(y,deadband, label="Deadbanded"+cols)
                plotted = True 
        for cols in self.chosen:         
                 
            x = self.data[cols].to_numpy()
            if len(x) == len(y):
                self.plot1.plot(y, x, label=cols)
                plotted = True
               
        for cols in self.chosen_B:
            butterworth= self.butterworth.get(cols)
            if len(y) == len(butterworth):
                self.plot1.plot(y,butterworth, label="Butterworth"+cols)
                plotted = True

        if plotted:
            self.plot1.legend()
        self.plot1.set_xlabel("Time")
        self.plot1.set_ylabel("Value (Logarithmic)")
        self.plot1.set_yscale("log") #remove this line to make y axis linear
        self.plot1.figure.tight_layout()
        self.canvas.draw()
        
    

class App(tk.Tk): #Class is same as doing home = Tk()
    def __init__(self):
        super().__init__() 
        self.title('Sensor GUI')
        self.notebook= ttk.Notebook(self)
        self.notebook.grid(row=0,sticky=NW)
        self.frame=self.NewTab(MainFrame,"Main")
        
        
    def NewTab(self,frameclass,title,*args,**kwargs):
        frame=frameclass(self,self,*args,**kwargs)
        self.notebook.add(frame,text=title)
        self.notebook.select(frame)
        
  
        

if __name__=="__main__":
    app = App()
    frame= MainFrame(app,app)
    app.mainloop()



