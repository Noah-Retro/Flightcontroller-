import tkinter as tk
import threading


class App(threading.Thread):             
    def __init__(self):
        super().__init__() 
        self.is_closed = False
                
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
        if self.is_closed:
            self.root.destroy()
            
        
    #def join(self):
    #    
    #    self.root.destroy()
    #    print("destroyed")
    #    #super().join()
    #    #print("joint")




