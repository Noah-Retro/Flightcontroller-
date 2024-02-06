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
    
}
hat_data: Dpad (Left/right,Up/down) Left=-1 Down=-1
"""

class PS4Controller:
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    
    def __init__(self,setting_path:str="src/settings/controller.json",*args,**kwargs):
        self.controller = pygame.joystick.Joystick(0)
        self.axis_data = None

        with open(setting_path) as f:
            self.settings = json.load(f)
        

    def get_data(self):
        """
        0:Leftstick -1 = Left
        1:Leftstick -1 = Up
        2:L3 -1 = not pressed 1 = pressed float in between
        3:Rigthstick -1 = Left
        4:Rightstick -1 = Up
        5:R3 -1 = Not pressed 1 = pressed float in between
        6:PS Button
        7:Option Button
        """
        r = []
        if not self.axis_data:
            self.axis_data = {0:0.0,1:0.0,2:0.0,3:0.0,4:0.0,5:0.0}

        pygame.event.pump()    
        for i in range(self.controller.get_numaxes()-1):
            r.append(self.controller.get_axis(i))
        r.append(self.controller.get_button(10))
        r.append(self.controller.get_button(9))
        return r


if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()
    j = pygame.joystick.Joystick(0)
    q = queue.Queue()
    q1 = queue.Queue()
    con = PS4Controller(controller=j,q=q,q1=q1)
    while True:
        con.get_data()
    
    
    
        
    