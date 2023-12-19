import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

window = tk.Tk()
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry(f"{w}x{h}")

window.title("Fligth controller")

# Notebook widget
notebook = ttk.Notebook(window)

# Airplane Settings Frame
airplainSettingsFrame = ttk.Frame(notebook)

# Controller Settings Frame
controllerSettingsFrame = ttk.Frame(notebook)

# data Transfer Frame
dataTransferFrame = ttk.Frame(notebook)

#Controller Frame
controllerFrame = ttk.Frame(notebook)

motorSettingsFrame = ttk.Frame(controllerSettingsFrame)
l = ttk.Label(motorSettingsFrame,text='empty')
l.pack()
def print_selection(v):
    l.config(text='you have selected ' + v)
    motorSettingsFrame.update()

s = tk.Scale(motorSettingsFrame, label='try me', from_=0, to=10, orient=tk.HORIZONTAL, length=200, showvalue=0,tickinterval=2, resolution=0.01, command=print_selection)
s.pack()
motorSettingsFrame.pack()

notebook.add(controllerFrame, text = 'Controller View')
notebook.add(airplainSettingsFrame, text = 'Airplane Settings')
notebook.add(controllerSettingsFrame, text = 'Controller Settings')
notebook.add(dataTransferFrame, text = 'Data transfer Settings')
notebook.pack()



lmain= ttk.Label(controllerFrame)
lmain.grid()

def video_stream(video_stream_in):
    img = Image.frombytes(mode='RGBA',data= video_stream_in,size=(320,240)).resize((640,480))
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream_in) 
    return video_stream

from video import video
video_stream(video())
lmain.bind(func=video_stream)
# run 
window.mainloop()  

