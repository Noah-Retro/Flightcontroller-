import queue
import pygame
from queue import Queue
import threading
import time
import json

"""
0:"X"
1:"O"
2:Dreieck
3:Quadrat
4:L1
5:R1
6:L2
7:R2
8:share
9:option
10:PS button
11:L3
12:R3
Axisdata:{
    0:Leftstick -1 = Left
    1:Leftstick -1 = Up
    2:L3 -1 = not pressed 1 = pressed float in between
    3:Rigthstick -1 = Left
    4:Rightstick -1 = Up
    5:R3 -1 = Not pressed 1 = pressed float in between
}
hat_data: Dpad (Left/right,Up/down) Left=-1 Down=-1
"""

class PS4Controller(threading.Thread):
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    
    def __init__(self,controller:pygame.joystick.JoystickType,q:Queue,q1:Queue,setting_path:str="src/settings/controller.json",*args,**kwargs):
        self.q = q
        self.q1 = q1
        self.controller = controller
        self.axis_data = None
        self.button_data = None
        self.hat_data = None
        with open("src/settings/controller.json") as f:
            self.settings = json.load(f)
        super().__init__(*args,**kwargs)

    def run(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {0:0.0,1:0.0,2:0.0,3:0.0,4:0.0,5:0.0}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                if self.settings["inverse_look"]:
                    self.axis_data.update(
                        (key, value * -1) for key, value in self.axis_data.items()
                    )

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                #self.queue.put({**self.button_data,**self.axis_data,**self.hat_data})
                self.q.put_nowait([self.button_data,self.axis_data,self.hat_data])
                self.q1.put_nowait([self.button_data,self.axis_data,self.hat_data])
                #return 
                #os.system('clear')
                #pprint.pprint([self.button_data,self.axis_data,self.hat_data])
                #pprint.pprint(self.axis_data.keys())
                #pprint.pprint(self.hat_data.keys())
    def get_data(self):
        if not self.axis_data:
            self.axis_data = {0:0.0,1:0.0,2:0.0,3:0.0,4:0.0,5:0.0}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)
            
        for i in range(self.controller.get_numaxes()-1):
            print(self.controller.get_axis(i))
        time.sleep(1)


if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()
    j = pygame.joystick.Joystick(0)
    q = queue.Queue()
    q1 = queue.Queue()
    con = PS4Controller(controller=j,q=q,q1=q1)
    while True:
        con.get_data()
    
    
    
        
    