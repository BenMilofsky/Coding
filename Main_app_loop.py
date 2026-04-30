import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Menu
import pandas as pd

class MainFrame(ttk.Frame): #ttk as only one tk per application
    def __init__(self,container,notebook): #as frame needs container 
        super().__init__(container)
        self.notebook= notebook
        self.label = ttk.Label(self,text='Choose what to import:').grid(row=0,sticky=W)
        importcheck = pd.read_csv('TPS1.csv',nrows=2)
        cols= importcheck.columns.tolist()
        self.i=1
        self.columnvar ={}
        for col in cols:
            var=tk.IntVar()
            self.i+=1
            tk.Checkbutton(self,text=col,variable =var).grid(row=self.i,sticky=W)
            self.columnvar[col]=var
        self.import_button= ttk.Button(self, text = 'import', width = 25, command = self.imported).grid(row=self.i+1,sticky=W)
    
    def imported(self):  
        import_checked =[]
        for col,var in self.columnvar.items():
            if var.get()==1:
                import_checked.append(col)
        values= pd.read_csv('TPS1.csv', usecols=import_checked).values
        self.imported_vals = values
        self.frame = self.newTab("Choose what to filter")
        Filter(frame)
        return self.frame

    def newTab(self,title):
        tab_Frame = Tab(self.notebook, title)
        self.notebook.add(tab_Frame, text=title)
        return tab_Frame  

class Tab(ttk.Frame):
    
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title

class Filter(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        
        print()

class Menu(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)
        #self.add_command(label='Exit',command=App.destroy)

class App(tk.Tk): #Class is same as doing home = Tk()
    def __init__(self):
        super().__init__() 
        self.title('Sensor GUI')
        self.menubar = Menu(self)
        
        self.notebook= ttk.Notebook(self)
        self.notebook.grid(row=1,sticky=NW)
        self.main_tab = MainFrame(self,self.notebook)
        self.notebook.add(self.main_tab, text="Main")



if __name__=="__main__":
    app = App()
    frame= MainFrame(app,app)
    app.mainloop()

