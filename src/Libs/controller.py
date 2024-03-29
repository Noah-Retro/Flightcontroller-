import queue
import pygame
from queue import Queue
import threading
import time
import json

from src.Libs.tools.paths import CONTROLLER_SETTINGS_PATH

class PS4Controller:
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    
    def __init__(self,setting_path:str=CONTROLLER_SETTINGS_PATH,*args,**kwargs):
        pygame.joystick.init()
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
            self.axis_data = [0,0,0,0,0,0,0,0]

        if self.controller.get_button(8):
            self.controller.quit()
            return
        
        pygame.event.pump()    
        for i in range(self.controller.get_numaxes()):
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
    
    
    
        
    