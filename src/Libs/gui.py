import tkinter as tk
from tkinter import ttk
import threading


class App(threading.Thread):             
    def __init__(self):
        super().__init__() 
                
    def callback(self):
        self.root.quit()
        
    def run(self):
        self.root = tk.Tk()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenwidth()
        self.root.geometry(f"{w}x{h}")
        self.root.protocol("WM_DELETE_WINDOW",self.callback)
        
        label = tk.Label(self.root, text="Hello World")
        label.pack()
        
        self.root.mainloop()
        

class ControllerSettings(tk.ttk.Frame):
    pass

if __name__ == "__main__":
    import tkinter as tk					 
    from tkinter import ttk 


    root = tk.Tk() 
    root.title("Tab Widget") 
    tabControl = ttk.Notebook(root) 

    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl) 

    tabControl.add(tab1, text ='Tab 1') 
    tabControl.add(tab2, text ='Tab 2') 
    tabControl.pack(expand = 1, fill ="both") 

    ttk.Label(tab1, 
            text ="""Welcome to  
            GeeksForGeeks""").grid(column = 0, 
                                row = 0, 
                                padx = 30, 
                                pady = 30) 
    ttk.Label(tab2, 
            text ="""Lets dive into the
            world of computers""").grid(column = 0, 
                                        row = 0, 
                                        padx = 30, 
                                        pady = 30) 
    ttk.OptionMenu(tab1,variable=["Hello","Hoi"],default="None")

    root.mainloop() 
