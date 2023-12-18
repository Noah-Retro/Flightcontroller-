import tkinter as tk
from tkinter import ttk
 
window = tk.Tk()
window.geometry('600x400')
window.title("Tab Widget")

# Notebook widget
notebook = ttk.Notebook(window)

# tab 1
tab1 = ttk.Frame(notebook)
label1 = ttk.Label(tab1, text = 'Text in tab 1')
label1.pack()
button1 = ttk.Button(tab1, text = 'Button in tab 1')
button1.pack()

# tab 2
tab2 = ttk.Frame(notebook)
label2 = ttk.Label(tab2, text = 'Text in tab 2')
label2.pack()
entry2 = ttk.Entry(tab2)
entry2.pack()

# tab 3
tab3 = ttk.Frame(notebook)
strinput = ttk.Scale(tab3,value=0.1)
strinput.pack()
label3 = ttk.Label(tab3)
label3.pack()

notebook.add(tab1, text = 'Tab 1')
notebook.add(tab2, text = 'Tab 2')
notebook.add(tab3, text = 'Tab 3')
notebook.pack()

# exercise
# add another tab with 2 buttons and one label inside 

tab_exercise = ttk.Frame(notebook)
button_exercise_1 = ttk.Button(tab_exercise, text = 'button 1')
button_exercise_1.pack()

button_exercise_2 = ttk.Button(tab_exercise, text = 'button 2')
button_exercise_2.pack()

label_exercise_2 = ttk.Label(tab_exercise, text = 'Label')
label_exercise_2.pack()

scale_exercise_3 = ttk.Scale(tab3,value=0.1)
scale_exercise_3.pack()


button_exercise_3 = ttk.Button(tab3,command=notebook.update(),text=scale_exercise_3.get())
button_exercise_3.pack()

notebook.add(tab_exercise, text = 'Tab exercise')

# run 
window.mainloop()  