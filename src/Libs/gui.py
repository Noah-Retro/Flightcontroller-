import tkinter as tk
from tkinter import *
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

    import json
    file = open("C:/Users/Noah/Desktop/Flightconfold/Flightcontroller-/src/settings/transmitt.json",mode="r")
    data = json.load(file)
    file.close() 

    payload_label = ttk.Label(tab2,text="Payload size")
    payload_label.pack()

    l = [data["tx"]["payload_size"]["value"], * data["tx"]["payload_size"]["options"]]
    payload_var = StringVar()
    payload_var.set(data["tx"]["payload_size"]["value"])
    
    dropdown = ttk.OptionMenu(tab2,payload_var,*l)
    dropdown.pack()

    def save():
        file = open("C:/Users/Noah/Desktop/Flightconfold/Flightcontroller-/src/settings/transmitt.json",mode="w")
        data["tx"]["payload_size"]["value"] = payload_var.get()
        file.write(json.dumps(data,indent=4))
        file.close()

    sub_button = ttk.Button(tab2,text= "Save",command=save)
    sub_button.pack()
    root.mainloop() 
