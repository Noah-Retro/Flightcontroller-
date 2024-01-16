import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import json
from src.libs.gui.slider import Slider as DobbleSlider

vals={
    "rightUD":None,
    "leftUD":None,
    "leftRight":None,
    "throtleR":None,
    "throtleL":None
}
pins={
    "rightUD":None,
    "leftUD":None,
    "leftRight":None,
    "throtleR":None,
    "throtleL":None
}

def storePin(val:int,name:str) -> None:
    pins[name]=val


def settings_dropdown(master:ttk.Frame,settings_name:str,label_text:str,data:dict)->StringVar:
    """Packs a Label and a Dropdown Menue in the master frame

    Args:
        master (ttk.Frame): Any Frame
        settings_name (str): Name in the dict
        label_text (str): Text for Label
        data (dict): Dict for Settings

    Returns:
        StringVar: Callback var
    """
    label = ttk.Label(master,text=label_text)
    label.pack()

    options = [data["tx"][settings_name]["value"], * data["tx"][settings_name]["options"]]
    var = StringVar()
    var.set(data["tx"][settings_name]["value"])

    dropdown = ttk.OptionMenu(master,var,*options)
    dropdown.pack()
    return var

def motor_frame(master,motor_data,name:str) -> Frame:
        frame_motor = ttk.Frame(
            master=master
        )
        var = tk.IntVar(value=motor_data[name]["pin"])

        label = Label(frame_motor,text=name)
        label.pack()

        options = [x for x in range(53)]
        dropdown= ttk.OptionMenu(frame_motor,var,*options,command=lambda x:storePin(val=x,name=name))
        dropdown.pack()
        frame_motor.pack()

        label = Label(frame_motor,text=f"{name} clamp")
        label.pack()

        sl = DobbleSlider(frame_motor,
                          max_val=2,
                          show_value=True,
                          init_lis=[motor_data[name]["clamp_min"],motor_data[name]["clamp_max"]])
        sl.pack()
        def getback(val):
            vals[name]=val

        sl.setValueChageCallback(lambda x: getback(x))
        return frame_motor

class App(threading.Thread):             
    def __init__(self,settings_path):
        super().__init__() 
        self.settings_path = settings_path

    def callback(self):
        self.root.quit()
        
    def run(self):
        self.root = tk.Tk()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenwidth()
        self.root.geometry(f"{w}x{h}")
        self.root.protocol("WM_DELETE_WINDOW",self.callback)
        
        #Tabs
        tabControl = ttk.Notebook(self.root)
        
        transmition_settings_tab = ttk.Frame(tabControl)
        tabControl.add(transmition_settings_tab, text = "Transmition")
        
        controller_settings_tab = ttk.Frame(tabControl)
        tabControl.add(controller_settings_tab, text = "Controller")
        
        motor_settings_tab = ttk.Frame(tabControl)
        tabControl.add(motor_settings_tab, text="Motors")

        tabControl.pack()

        with open(self.settings_path + "/transmitt.json") as transmittions_file:
            transmittions_data = json.load(transmittions_file)

        payload_var = settings_dropdown(master=transmition_settings_tab,
                          settings_name="payload_size",
                          label_text="Payload size",
                          data=transmittions_data)

        data_rate_var = settings_dropdown(master=transmition_settings_tab,
                          settings_name="data_rate",
                          label_text="Data rate",
                          data=transmittions_data)
        
        pa_level_var = settings_dropdown(master=transmition_settings_tab,
                          settings_name="pa_level",
                          label_text="Pa level",
                          data=transmittions_data)

        def transmittions_save():
            with open(self.settings_path+"/transmitt.json",mode="w")  as file:
                transmittions_data["tx"]["payload_size"]["value"] = payload_var.get()
                transmittions_data["tx"]["data_rate"]["value"] = data_rate_var.get()
                transmittions_data["tx"]["pa_level"]["value"] = pa_level_var.get()
                transmittions_data["rx"]["payload_size"]["value"] = payload_var.get()
                transmittions_data["rx"]["data_rate"]["value"] = data_rate_var.get()
                transmittions_data["rx"]["pa_level"]["value"] = pa_level_var.get()
                file.write(json.dumps(transmittions_data,indent=4))

        transmition_button_save = ttk.Button(transmition_settings_tab,
                                             command=transmittions_save,
                                             text="Save")
        transmition_button_save.pack()
     

        #Controller settings
        with open(self.settings_path + "/controller.json") as controller_file:
            controller_data = json.load(controller_file)
        

        rumble_var = BooleanVar()
        rumble_var.set(controller_data["rumble"])
        rumble_button = ttk.Checkbutton(controller_settings_tab,
                                        variable=rumble_var,
                                        text="Rumble",
                                        onvalue=True,
                                        offvalue=False)
        rumble_button.pack()
        
        inverse_look_var = BooleanVar()
        inverse_look_var.set(controller_data["inverse_look"])
        inverse_look_button = ttk.Checkbutton(controller_settings_tab,
                                        variable=inverse_look_var,
                                        text="Inverse look",
                                        onvalue=True,
                                        offvalue=False)
        inverse_look_button.pack()

        sens_label = ttk.Label(controller_settings_tab,text="Sensitivity X Axis")
        sens_label.pack()

        sensitivity_x_var = DoubleVar()
        sensitivity_x_var.set(controller_data["sensitivity_x"])
        sensitivity_x = ttk.Scale(controller_settings_tab,
                                       variable=sensitivity_x_var,
                                       from_=1,
                                       to=10,)
        sensitivity_x.pack()

        sens_label = ttk.Label(controller_settings_tab,text="Sensitivity Y Axis")
        sens_label.pack()

        sensitivity_y_var = DoubleVar()
        sensitivity_y_var.set(controller_data["sensitivity_y"])
        sensitivity_y = ttk.Scale(controller_settings_tab,
                                       variable=sensitivity_y_var,
                                       from_=1,
                                       to=10,)
        sensitivity_y.pack()

        def controller_save():
            with open(self.settings_path+"/controller.json",mode="w") as file:
                controller_data["rumble"]=rumble_var.get()
                controller_data["inverse_look"]=inverse_look_var.get()
                controller_data["sensitivity_x"]=sensitivity_x_var.get()
                controller_data["sensitivity_y"]=sensitivity_y_var.get()
                file.write(json.dumps(controller_data,indent=4))

        controller_save_button = ttk.Button(controller_settings_tab,
                                            command=controller_save,
                                            text="Save")
        controller_save_button.pack()


        with open(self.settings_path + "/motors.json") as motors_file:
            motor_data = json.load(motors_file)

        motor_frame(master=motor_settings_tab,motor_data=motor_data,name="rightUD").pack()
        motor_frame(master=motor_settings_tab,motor_data=motor_data,name="leftUD").pack()
        motor_frame(master=motor_settings_tab,motor_data=motor_data,name="leftRight").pack()
        motor_frame(master=motor_settings_tab,motor_data=motor_data,name="throtleR").pack()
        motor_frame(master=motor_settings_tab,motor_data=motor_data,name="throtleL").pack()

        def motor_save():
            for k,v in vals.items():
                if v == None:
                    continue
                motor_data[k]["clamp_min"]=v[0]
                motor_data[k]["clamp_max"]=v[1]
            for k,v in pins.items():
                if v==None:
                    continue
                motor_data[k]["pin"]=v
            with open(self.settings_path+"/motors.json",mode="w")  as file:
                file.write(json.dumps(motor_data,indent=4))

        controller_save_button = ttk.Button(motor_settings_tab,
                                            command=motor_save,
                                            text="Save")
        controller_save_button.pack()

        info_text = ttk.Label(self.root,text="Changes will only be done after a restart of the controller unit.")
        info_text.pack(anchor=tk.S)
        self.root.mainloop()


if __name__ == "__main__":
    test = App("Flightcontroller-/src/settings")
    
    test_thread = threading.Thread(target=test.run)
    test_thread.start()