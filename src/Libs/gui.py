import tkinter as tk
import threading


class App(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
                
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
        
    def join(self):
        self.root.quit()




