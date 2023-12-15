from tkinter import *

window = Tk()

width = window.winfo_screenwidth()
height = window.winfo_screenwidth()

window.title("Flightcontroller")
window.geometry(f"{width}x{height}")

window.mainloop()
