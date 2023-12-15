import src.Libs.autoupdate as ap
from src.Libs.controller import PS4Controller
from src.Libs.gui import app
import pygame

from sys import platform
import os
from threading import Thread
from queue import Queue
from collections import deque
import time

try:
    if platform == "linux":
        ap.update(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    raise e

pygame.init()
pygame.joystick.init()

controller = pygame.joystick.Joystick(0)
controller.init()

controllerQueue = Queue()

ps4con = PS4Controller(controller=controller,q=controllerQueue)

if __name__ == '__main__':
    ps4con.start()
    controllerData = []
    
    gui = Thread(target= app.mainloop)
    
    while True:
        if not controllerQueue.empty():
            
            for _ in range(controllerQueue.qsize()-1):
                controllerData = controllerQueue.get_nowait()
        
        
        time.sleep(1)
        if controllerData[0][0]:
            print("rumble")
            print(controller.rumble(low_frequency=0.5,high_frequency=1,duration=0))
        else:
            print("stop rumble")
            controller.stop_rumble()
        
        if controllerData[0][9]:
            gui.start()
        
        if controllerData[0][10]:
            gui.join()
                        
        
        
        



    

